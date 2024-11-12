#!/usr/bin/env python3

# Import standard libraries
import argparse
import configparser
import datetime
import logging
import nest_asyncio
import queue
import os
from pathlib import Path
import pyshark
import shutil
import signal
import subprocess
import sys
import threading
import time

# Import custom modules
from macros import *

# Global configuration
nest_asyncio.apply()

# Main class that handles everything after arguments are parsed
class Marlin:

    # Static variables
    SNIFFER_FOUND_CELL_TIMEOUT = 20 # 10 seconds to associate with the cell service
    SNIFFER_TOTAL_TIMEOUT = 70 # 1 minute for the sniffer to run
    
    # Initialize class
    def __init__(self, args):

        # Set class variables
        self.threads = []
        self.running = True
        self.sniffer_path = args.sniffer
        self.location_folder = self.create_location_folder(args.location)

        # Class logging settings
        self.logger = logging.getLogger(self.__class__.__name__)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # File logging settings
        file_handler = logging.FileHandler(str(self.location_folder / 'marlin.log'))
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        # Console logging settings
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # Create queues for threads
        self.radio_queue = self.load_radios()
        self.frequency_queue = self.load_frequencies(args.freq)
        self.capture_queue = queue.Queue()

        # Capture interrupt signal for graceful exit
        signal.signal(signal.SIGINT, self.handle_signal)

    # Handle exit signal gracefully
    def handle_signal(self, signum, frame):
        print("Exiting.")
        self.running = False

    # Check for USRP B210s by loading FPGA files
    def load_radios(self):
        radio_queue = queue.Queue()
        command = "uhd_find_devices".split(' ')
        try: proc = subprocess.Popen(command,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.DEVNULL,
                                    text=True)
        except OSError as e: self.logger.critical(f'Unable to execute {command}: {str(e)}')

        # Monitor program output for serial numbers
        while proc.poll() is None:
            line = proc.stdout.readline().strip()
            if line != '':
                if 'serial:' in line:
                    serial = line.split(' ')[1]
                    radio_queue.put(serial)
        
        # Report number of available radios
        num_radios = radio_queue.qsize()
        if num_radios == 0:
            self.logger.critical("Detected no radios.")
            self.running = False
        elif num_radios == 1: self.logger.warning(f"Detected 1 radio.")
        else: self.logger.warning(f"Detected {num_radios} radios.")

        return radio_queue

    # Load list of frequencies
    def load_frequencies(self, file_name):
            try:
                # Read input file containing EARFCNs
                with open(file_name, "r") as in_file:
                    frequency_list = in_file.readlines()
                    frequency_queue = queue.Queue()
                    for i in range(0,len(frequency_list)):
                        frequency_queue.put(frequency_list[i].split(',')[0].strip())
                    # Calculate number of available frequencies
                    num_frequencies = len(frequency_list)
                    if num_frequencies == 0:
                        self.logger.critical("Detected no frequencies.")
                        self.running = False
                    elif num_frequencies == 1: self.logger.warning(f"Detected 1 frequency.")
                    else: self.logger.warning(f"Detected {num_frequencies} frequencies.")
                    return frequency_queue
            except OSError as e:
                self.logger.critical(f"'{file_name}' could not be opened: OSError - {str(e)}")
                self.running = False
                return queue.Queue()

    # Create a location folder if it does not exist
    def create_location_folder(self, location):
        location_folder = Path('./locations')
        format_location = location.replace('.', '').replace(' ', '_').replace(',','').lower()
        location_folder = location_folder / format_location / datetime.datetime.now().strftime("%Y-%m-%d")
        location_folder.mkdir(parents=True, exist_ok=True)
        return location_folder

    # Call LTESniffer
    def run_sniffer(self):

        # Construct program call
        earfcn = self.frequency_queue.get()
        radio = self.radio_queue.get()
        frequency = convert_earfcn_to_freq(earfcn)
        my_command = f'{self.sniffer_path} -f {frequency} -C -m 0 -z 3 -a num_recv_frames=512,serial={radio}'.split(' ')

        # Directory to run sniffer from
        freq_directory = self.location_folder / str(earfcn) / datetime.datetime.now().strftime("%H:%M:%S")
        freq_directory.mkdir(parents=True, exist_ok=True)
        self.logger.warning(f'EARFCN {earfcn}: Searching for cell using radio {radio}.')
    
        # Start process
        try:
            proc = subprocess.Popen(my_command,
                                    cwd=freq_directory,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.DEVNULL,
                                    text=True)
        except OSError as e:
            # Executing non-existent file
            self.logger.critical(f"Unable to execute LTESniffer: {str(e)}")
            self.running = False

        time_start = time.time()
        time_elapsed = 0
        cell_found = False
        full_capture = True

        # Attempt to find base station at target frequency
        while (time_elapsed < Marlin.SNIFFER_FOUND_CELL_TIMEOUT) and (self.running) and (not cell_found):

            # Restart sniffer if it exited
            if (proc.poll() is not None):
                proc = subprocess.Popen(my_command,
                                        cwd=freq_directory,
                                        stdout=subprocess.PIPE,
                                        stderr=subprocess.DEVNULL,
                                        text=True)
                time.sleep(0.5)

            # Monitor output for success condition
            line = proc.stdout.readline().strip()
            if line != '':
                # print(line)
                if "Decoded MIB." in line:
                    cell_found = True
                    self.logger.warning(f"EARFCN {earfcn}: Found cell using radio {radio}.")

            # Recalculate elapsed time
            time_elapsed = time.time() - time_start

        # If a base station is detected, continue monitoring it
        if cell_found:
            while (time_elapsed < Marlin.SNIFFER_TOTAL_TIMEOUT) and (self.running):
                # If sniffer is active and successful, keep going
                if (proc.poll() is None):
                    proc.stdout.flush()
                    time.sleep(0.5)
                else:
                    self.logger.warning(f"EARFCN {earfcn}: Monitoring ended prematurely using radio {radio}.")
                    shutil.rmtree(freq_directory)
                    full_capture = False
                    break
                time_elapsed = time.time() - time_start
            if full_capture and self.running:
                self.logger.warning(f"EARFCN {earfcn}: Finished monitoring cell using radio {radio}.")

        # Quickly end thread if running flag is set False
        if (not self.running) and (proc.poll() is None):
            proc.terminate()
            proc.wait()
            shutil.rmtree(freq_directory)
            return
        
        # Gracefully exit sniffer if it is still active
        if proc.poll() is None:
            proc.stdout.flush()
            os.kill(proc.pid, signal.SIGINT)
            try: proc.wait(timeout=10)
            except subprocess.TimeoutExpired:
                # If sniffer will not gracefully exit, terminate it
                self.logger.warning(f"EARFCN {earfcn}: Sniffer timed out using radio {radio}.")
                proc.terminate()
                proc.wait()
                shutil.rmtree(freq_directory)

        # Log failure to find base station
        if (not cell_found):
            self.logger.warning(f"EARFCN {earfcn}: Unable to find cell using radio {radio}.")
            shutil.rmtree(freq_directory)
        
        # Re-insert radio and frequency into respective queues
        self.radio_queue.put(radio)
        self.frequency_queue.put(earfcn)

        # Add capture to analysis queue if everything was successful
        if cell_found and full_capture and self.running:
                self.capture_queue.put((str(freq_directory / 'ltesniffer_dl_mode.pcap'), earfcn))
        return
        
    # Recover connections from LTE pcap capture
    def analyze_capture(self):

        # Get capture from input queue
        file_name, earfcn = self.capture_queue.get()

        # Get packets from pcap file
        try:
            packets = pyshark.FileCapture(file_name, custom_parameters=my_parameters, display_filter=all_lte)
        except:
            self.logger.warning(f'EARFCN {earfcn}: Repairing PCAP file.')
            os.system(f'pcapfix {file_name} -o {file_name}')
            self.capture_queue.put((file_name, earfcn))
            return
        
        # Track total connections and IMSI-exposed connections
        total_connections = []
        exposed_connections = []
    
        # Iterate through packets
        try:
            for i, packet in enumerate(packets):

                # Stop analyzing if stop flag is raised
                if not self.running: break

                # Convert packet to string
                packet_string = packet.__str__().lower()

                # Get message-agnostic packet information
                try: current_rnti = packet['mac-lte'].rnti
                except KeyError:
                    print(packet_string)
                    continue

                # Convert packet to string
                packet_string = packet.__str__().lower()

                # If message indicates a new connection
                if (current_rnti == '5') or ('rrcconnectionsetup' in packet_string):

                    # Determine C-RNTI based on message type
                    if (current_rnti == '5'):
                        current_message = 'RAR Message'
                        try: current_rnti = packet['mac-lte'].rar_temporary_crnti
                        except AttributeError:
                            print(packet_string)
                            continue
                        except KeyError:
                            print(packet_string)
                            continue
                    else: current_message = 'RRC Connection Setup'
                    
                    # Add connection to total connections list if needed
                    if current_rnti not in total_connections:
                        total_connections.append(current_rnti)

                # If message is IMSI-exposing
                else:
                    # Add connection to exposed connections list if appropriate
                    if (current_rnti not in exposed_connections) and (current_rnti in total_connections):
                        exposed_connections.append(current_rnti)
        except:
            # Attempt to fix the pcap if needed
            os.system(f'pcapfix {file_name} -o {file_name}')
            self.capture_queue.put((file_name, earfcn))
            self.logger.warning(f'EARFCN {earfcn}: tshark crashed during capture analysis.')
            return
        # Calculate IMSI-exposure ratio
        if len(total_connections) > 10:
            imsi_exposure_ratio = int((len(exposed_connections) * 100)/len(total_connections))
            self.logger.warning(f'EARFCN {earfcn}: IMSI-exposing ratio = {imsi_exposure_ratio}%.')
        elif len(total_connections) > 0:
            self.logger.warning(f'EARFCN {earfcn}: Detected too few connections.')
        else:
            self.logger.warning(f'EARFCN {earfcn}: Detected no connections.')
        return

    # Join all threads
    def wait_for_threads(self):
        for thread in self.threads:
            thread.join()
        self.logger.warning("Ended all active threads.")
    
    # Loop through frequencies
    def loop(self):

        # Run continuously until specified
        while(self.running):

            # Start analyzing a base station if a USRP and a frequency are available
            if (not self.radio_queue.empty()) and (not self.frequency_queue.empty()):
                thread = threading.Thread(target=self.run_sniffer)
                thread.start()
                self.threads.append(thread)
            
            # Start analyzing a pcap if one is available
            if (not self.capture_queue.empty()):
                thread = threading.Thread(target=self.analyze_capture)
                thread.start()
                self.threads.append(thread)
            
            else: time.sleep(1)
        
        # Wait for threads to end gracefully
        self.wait_for_threads()

# Parse configuration file
def load_config(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    return config

# Create default configuration file
def create_config(file_name):
    
    # Define default configurations and write contents to file
    config = configparser.ConfigParser()
    config['config'] = {'location': 'Home',
                        'freq': 'frequencies.txt',
                        'sniffer': '/LTESniffer/build/src/LTESniffer'}
    with open(file_name, 'w') as configfile: config.write(configfile)
    print(f'Created new configuration file {file_name}')
    
# Parse arguments from command line or config file
def parse_arguments():

    # Initialize variables
    parser = argparse.ArgumentParser(prog='Marlin',
                                     description='IMSI-Catcher detector based on downlink traffic behavior.')
    parser.add_argument('-l', '--location',
                        metavar='Location',
                        type=str,
                        help='Specify a location in plain text (e.g., "Washington, D.C.").')
    parser.add_argument('-f', '--freq',
                        type=str,
                        metavar='filename.txt',
                        help='Specify a frequency list file.')
    parser.add_argument('-c', '--config',
                        type=str,
                        metavar='filename.ini',
                        help='Specify a configuration file.')
    parser.add_argument('-a', '--add',
                        type=str,
                        metavar='filename.ini',
                        help='Create a default configuration file.')
    parser.add_argument('-s', '--sniffer',
                        type=str,
                        metavar='path',
                        help='Path to sniffer executable.')
    args = parser.parse_args()

    # Create default configuration file
    if args.add:
        create_config(args.add)
        sys.exit()
    
    # Load the config file if specified
    config = {}
    if Path(args.config).is_file(): config = load_config(args.config)

    # Favor console arguments over configuration file arguments
    args.location = args.location or config.get('config', 'location', fallback='Home')
    args.freq = args.freq or config.get('config', 'freq', fallback='frequencies.txt')
    args.sniffer = args.sniffer or config.get('config', 'sniffer', fallback='./sniffers/LTESniffer/build/src/LTESniffer')

    return args

# Main program
def main():

    # Parse user arguments
    args = parse_arguments()

    # Initialize and run main class
    analyzer = Marlin(args)
    analyzer.loop()

    return

if __name__ == '__main__': main()
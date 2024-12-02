# Marlin Tool

Our tool enables downlink traffic analysis using USRP B210 software-defined radios. This program takes as input a text file of EARFCN values to analyze and automatically searches for your radios using the `uhd_find_devices` command. At this point, the program creates a radio queue and a frequency queue.

During program execution, the marlin script cycles through frequencies using as many available radios as it detects. By default, the script spends one minute on each frequency before cycling to the next. After monitoring each frequency, the code adds the resulting pcap file to a queue of capture files that it analyzes. All information is logged to the terminal and to a log file. The only required argument is `-c <filename>.ini` as the program expects a configuration file. By default, the configuration file is called `marlin.ini`. 

```text
python3 marlin.py
usage: Marlin [-h] [-l Location] [-f filename.txt] [-c filename.ini] [-a filename.ini] [-s path]

IMSI-Catcher detector based on downlink traffic behavior.

options:
  -h, --help            show this help message and exit
  -l Location, --location Location
                        Specify a location in plain text (e.g., "Washington, D.C.").
  -f filename.txt, --freq filename.txt
                        Specify a frequency list file.
  -c filename.ini, --config filename.ini
                        Specify a configuration file.
  -a filename.ini, --add filename.ini
                        Create a default configuration file.
  -s path, --sniffer path
                        Path to sniffer executable.
```
Output from the program is sent to console and to a log file which is located in `./locations/<location>/<date>/marlin.log`. This output will resemble the following lines:

```text
EARFCN <#>: Searching for cell using radio <#>.
EARFCN <#>: Found cell using radio <#>.
EARFCN <#>: IMSI-exposing ratio = <#>%.
```

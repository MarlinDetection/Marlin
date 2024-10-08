# Import libraries
from datetime import datetime
from macros import *
import nest_asyncio
import numpy as np
import os
import pyshark
import pandas as pd
import sys

# Library settings
nest_asyncio.apply()
np.seterr(divide='ignore', invalid='ignore')

# pcap filters
lte_rar_filter = '(mac-lte.rnti-type == 2)'
lte_setup_filter = '(lte-rrc.c1 == 3 and lte-rrc.c1 == 0 and mac-lte.dlsch.lcid == 0x00)'
identity_request_filter = '(nas_eps.nas_msg_emm_type == 0x55 and nas_eps.emm.id_type2 == 1)'
tau_reject_filter = '(nas_eps.nas_msg_emm_type == 0x4b and (nas_eps.emm.cause == 3 or nas_eps.emm.cause == 6 or nas_eps.emm.cause == 7 or nas_eps.emm.cause == 8 or nas_eps.emm.cause == 12 or nas_eps.emm.cause == 14 or nas_eps.emm.cause == 35))'
detach_request_filter = '(nas_eps.nas_msg_emm_type == 0x45 and !(nas_eps.emm.detach_type_dl == 3))'
attach_reject_filter = '(nas_eps.nas_msg_emm_type == 0x44 and (nas_eps.emm.cause == 3 or nas_eps.emm.cause == 6 or nas_eps.emm.cause == 7 or nas_eps.emm.cause == 8 or nas_eps.emm.cause == 11 or nas_eps.emm.cause == 12 or nas_eps.emm.cause == 13 or nas_eps.emm.cause == 14 or nas_eps.emm.cause == 15 or nas_eps.emm.cause == 35))'
service_reject_filter = '(nas_eps.nas_msg_emm_type == 0x4e and (nas_eps.emm.cause == 3 or nas_eps.emm.cause == 6 or nas_eps.emm.cause == 7 or nas_eps.emm.cause == 9 or nas_eps.emm.cause == 12 or nas_eps.emm.cause == 14 or nas_eps.emm.cause == 35))'
imsi_exposing_filter_lte = f'({identity_request_filter} or {tau_reject_filter} or {detach_request_filter} or {attach_reject_filter} or {service_reject_filter})'
all_lte = f'({lte_rar_filter} or {lte_setup_filter} or {imsi_exposing_filter_lte})'

# Recover connections from LTE pcap capture
def get_lte_connections(file_name, display_filter):

    # Get packets from pcap file
    packets = pyshark.FileCapture(file_name, custom_parameters=my_parameters, display_filter=display_filter)

    # Create dataframe to track connections
    connections_df = pd.DataFrame(columns=['RNTI', 'Timestamp', 'IMSI-Exposing Message'])
 
    # Iterate through packets
    for i, packet in enumerate(packets):

         # Convert packet to string
        packet_string = packet.__str__().lower()

        # Get message-agnostic packet information
        epoch = float(packet.frame_info.time_epoch)
        try: current_rnti = packet['mac-lte'].rnti
        except KeyError:
            print(packet_string)
            continue
        current_message = ''

        # Only consider connections originating in the past minute
        relevant_messages = connections_df.loc[connections_df['Timestamp'] >= (epoch - 60)]

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
            
            # Add connection to dataframe if it does not exist
            if current_rnti not in relevant_messages['RNTI'].values:
                connections_df.loc[len(connections_df)] = [current_rnti, epoch, '']

        # If message is IMSI-exposing
        else:

            # Only consider messages which have an associated connection start
            if current_rnti in relevant_messages['RNTI'].values:

                # Get message type from packet contents
                if 'identity request' in packet_string: current_message = 'Identity Request'
                elif 'service reject' in packet_string: current_message = 'Service Reject'
                elif 'attach reject' in packet_string: current_message = 'Attach Reject'
                elif 'detach request' in packet_string: current_message = 'Detach Request'
                elif 'tracking area update reject' in packet_string: current_message = 'Tracking Area Update Reject'
                else: 
                    print(packet_string)
                    continue
                
                # Add message type to dataframe
                connections_df.at[connections_df.index[connections_df['RNTI'] == current_rnti][0], 'IMSI-Exposing Message'] = current_message

    print(connections_df)
    # Save dataframe to a pkl file
    return connections_df

# Main Function
def main():

    # Pull out connections from LTE packet captures
    get_lte_connections(sys.argv[1], all_lte).to_pickle('output.pkl')

# Call main function
if __name__ == '__main__': main()
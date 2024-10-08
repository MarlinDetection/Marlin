# Import libraries
import pyshark
import pandas as pd
import os
import nest_asyncio
import numpy as np
from macros import *
import sys

# Library settings
nest_asyncio.apply()
np.seterr(divide='ignore', invalid='ignore')

# pcap filters
downlink_gsm = '(gsmtap.uplink == 0)'
gsm_immediate_assignment = '(gsm_a.dtap.msg_rr_type == 0x3f)'
gsm_location_updating_request = '(gsm_a.dtap.msg_mm_type == 0x08)'
gsm_identity_request = '(gsm_a.dtap.msg_mm_type == 0x18 and gsm_a.dtap.type_of_identity == 1)'
gsm_authentication_reject = '(gsm_a.dtap.msg_mm_type == 0x11)'
gsm_location_updating_reject = '(gsm_a.dtap.msg_mm_type == 0x04 and (gsm_a.dtap.rej_cause == 2 or gsm_a.dtap.rej_cause == 3 or gsm_a.dtap.rej_cause == 6 or gsm_a.dtap.rej_cause == 11 or gsm_a.dtap.rej_cause == 12 or gsm_a.dtap.rej_cause == 13))'
gsm_cm_service_reject = '(gsm_a.dtap.msg_mm_type == 0x22 and (gsm_a.dtap.rej_cause == 4 or gsm_a.dtap.rej_cause == 6))'
gsm_all = f'{downlink_gsm} and ({gsm_location_updating_request} or {gsm_identity_request} or {gsm_authentication_reject} or {gsm_location_updating_reject} or {gsm_cm_service_reject})'

# Recover connections from LTE pcap capture
def get_connections(file_name, display_filter):

    # Get packets from pcap file
    packets = pyshark.FileCapture(file_name, custom_parameters=my_parameters, display_filter=display_filter)

    # Create variables to track connections
    connections_df = pd.DataFrame(columns=['Identifier', 'Timestamp', 'IMSI-Exposing Message'])
    counter = 0
    current_message = ''

    # Iterate through packets
    for i, packet in enumerate(packets):

        # Get message-agnostic packet information
        epoch = float(packet.frame_info.time_epoch)

        # Only consider connections originating in the past minute
        relevant_messages = connections_df.loc[connections_df['Timestamp'] >= ((epoch % 86400) - 60)]

        # Convert packet to string
        packet_string = packet.__str__().lower()

        # If message indicates a new connection
        if ('location updating request' in packet_string):

            counter += 1
            
            # Add connection to dataframe if it does not exist
            if counter not in relevant_messages['Identifier'].values:
                connections_df.loc[len(connections_df)] = [counter, epoch % 86400, '']

        # If message is IMSI-exposing
        else:

            # Only consider messages which have an associated connection start
            if counter in relevant_messages['Identifier'].values:

                # Get message type from packet contents
                if 'identity request' in packet_string: current_message = 'Identity Request'
                elif 'authentication reject' in packet_string: current_message = 'Authentication Reject'
                elif 'location updating reject' in packet_string: current_message = 'Location Updating Reject'
                elif 'cm service reject' in packet_string: current_message = 'CM Service Reject'
                else:
                    print(packet_string)
                    continue
                
                # Add message type to dataframe
                connections_df.at[connections_df.index[connections_df['Identifier'] == counter][0], 'IMSI-Exposing Message'] = current_message

    # Save dataframe to a pkl file
    print(connections_df)
    return connections_df

# Main Function
def main():
    # Pull out connections from LTE packet captures
    file_name = sys.argv[1]
    get_connections(file_name, gsm_all).to_pickle('output.pkl')

# Call main function
if __name__ == '__main__': main()
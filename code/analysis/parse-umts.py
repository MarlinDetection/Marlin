# Import libraries
import sys
import pyshark
import pandas as pd
import nest_asyncio
import numpy as np
from macros import *

# Library settings
nest_asyncio.apply()
np.seterr(divide='ignore', invalid='ignore')

# pcap filters
umts_connection_setup = 'rrc.rrcConnectionSetup == 0'
umts_identity_request = '(gsm_a.dtap.msg_mm_type == 0x18 and gsm_a.dtap.type_of_identity == 1)'
umts_authentication_reject = '(gsm_a.dtap.msg_mm_type == 0x11)'
umts_location_updating_reject = '(gsm_a.dtap.msg_mm_type == 0x04 and (gsm_a.dtap.rej_cause == 2 or gsm_a.dtap.rej_cause == 3 or gsm_a.dtap.rej_cause == 6 or gsm_a.dtap.rej_cause == 11 or gsm_a.dtap.rej_cause == 12))'
umts_cm_service_reject = '(gsm_a.dtap.msg_mm_type == 0x22 and (gsm_a.dtap.rej_cause == 4 or gsm_a.dtap.rej_cause == 6))'
umts_attach_reject = '(gsm_a.dtap.msg_mm_type == 0x04 and (gsm_a.gm.gmm.cause == 3 or gsm_a.gm.gmm.cause == 6 or gsm_a.gm.gmm.cause == 7 or gsm_a.gm.gmm.cause == 8 or gsm_a.gm.gmm.cause == 11 or gsm_a.gm.gmm.cause == 12 or gsm_a.gm.gmm.cause == 13 or gsm_a.gm.gmm.cause == 14 or gsm_a.gm.gmm.cause == 15))'
umts_detach_request = '(gsm_a.dtap.msg_mm_type == 0x05 and gsm_a.gm.gmm.type_of_detach == 0x02 and (gsm_a.gm.gmm.cause == 2 or gsm_a.gm.gmm.cause == 3 or gsm_a.gm.gmm.cause == 6 or gsm_a.gm.gmm.cause == 8 or gsm_a.gm.gmm.cause == 11 or gsm_a.gm.gmm.cause == 12 or gsm_a.gm.gmm.cause == 13 or gsm_a.gm.gmm.cause == 14 or gsm_a.gm.gmm.cause == 15))'
umts_rau_reject = '(gsm_a.dtap.msg_gmm_type == 0x0b and (gsm_a.gm.gmm.cause == 3 or gsm_a.gm.gmm.cause == 6 or gsm_a.gm.gmm.cause == 7 or gsm_a.gm.gmm.cause == 9 or gsm_a.gm.gmm.cause == 11 or gsm_a.gm.gmm.cause == 12 or gsm_a.gm.gmm.cause == 14))'
umts_auth_cipher_reject = '(gsm_a.dtap.msg_mm_type == 0x14)'
umts_service_reject = '(gsm_a.dtap.msg_mm_type == 0x0e and (gsm_a.gm.gmm.cause == 3 or gsm_a.gm.gmm.cause == 6 or gsm_a.gm.gmm.cause == 7 or gsm_a.gm.gmm.cause == 9 or gsm_a.gm.gmm.cause == 11 or gsm_a.gm.gmm.cause == 12))'
umts_all = f'{umts_connection_setup} or {umts_identity_request} or {umts_authentication_reject} or {umts_location_updating_reject} or {umts_cm_service_reject} or {umts_attach_reject} or {umts_detach_request} or {umts_rau_reject} or {umts_auth_cipher_reject} or {umts_service_reject}'

umts_separate_dict = {'Connection Setup':               umts_connection_setup,
                      'Identity Request':               umts_identity_request,
                      'Authentication Reject':          umts_authentication_reject,
                      'Location Updating Reject':       umts_location_updating_reject,
                      'CM Service Reject':              umts_cm_service_reject,
                      'Attach Reject':                  umts_attach_reject,
                      'Detach Request':                 umts_detach_request,
                      'RAU Reject':                     umts_rau_reject,
                      'Authentication Cipher Reject':   umts_auth_cipher_reject,
                      'Service Reject':                 umts_service_reject}

# Recover connections from UMTS pcap capture
def get_connections(file_name, display_filter):

    # Create variables to track connections
    connections_df = pd.DataFrame(columns=['Timestamp', 'Message'])
    for message in umts_separate_dict.keys():
        # Get packets from pcap file
        packets = pyshark.FileCapture(file_name, custom_parameters=my_parameters, display_filter=umts_separate_dict[message])
        # Iterate through packets
        for i, packet in enumerate(packets):
            # Get message-agnostic packet information
            epoch = float(packet.frame_info.time_epoch)
            connections_df.loc[len(connections_df)] = [epoch, message]
    sorted_messages = connections_df.sort_values(by='Timestamp')

    # Save bins and percentages as lists
    identifiers = []
    timestamps = []
    ie_messages = []

    # Iterate through IMSI-exposing messages
    epoch = sorted_messages.iloc[0]['Timestamp']
    start = epoch - (epoch % 60)
    open = start
    close = start + 60
    end = sorted_messages.iloc[-1]['Timestamp']
    while close < (end + 60):
        active = -1
        written = False
        relevant_df = sorted_messages.loc[(sorted_messages['Timestamp'] >= open) & (sorted_messages['Timestamp'] < close)]
        for entry in relevant_df.iterrows():
            if entry[1]['Message'] == 'Connection Setup': 
                active = entry[1]['Timestamp'] % 86400
                identifiers.append(active)
                timestamps.append(active)
                written = False
            else:
                if active != -1 and not written:
                    identifiers.append(active)
                    timestamps.append(entry[1]['Timestamp'] % 86400)
                    ie_messages.append(entry[1]['Message'])
                    written = True
        open += 60
        close += 60

    # Convert lists to a dataframe
    return pd.DataFrame(list(zip(identifiers, timestamps, ie_messages)),
                columns =['Identifier', 'Timestamp', 'IMSI-Exposing Message'])

# Main Function
def main(arguments):

    # Pull out connections from LTE packet captures
    get_connections(sys.argv[1], umts_all).to_pickle('output.pkl')

# Call main function
if __name__ == '__main__': main(sys.argv)
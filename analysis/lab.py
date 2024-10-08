# Import libraries
import numpy as np
import os
import pandas as pd
from pathlib import Path

# Iterate through all log files in directory
def calculate_ratios(connections_folder):

    file_dict = {
        'gsm-imsi-catcher.pkl': 'GSM IMSI-Catcher',
        'umts-imsi-catcher.pkl': 'UMTS IMSI-Catcher',
        'lte-imsi-catcher.pkl': 'LTE IMSI-Catcher'
    }
    for file in os.listdir(connections_folder):

        # Ensure file is in pcap format
        if file.endswith('.pkl'):

            # Read in dataframe
            file_path = str(connections_folder / file)
            connections_df = pd.read_pickle(file_path)

            # Iterate through IMSI-exposing messages
            my_df = connections_df.loc[connections_df['IMSI-Exposing Message'] != '']
            bins = []
            ratios = []
            for exposure in my_df.iterrows():
                epoch = exposure[1]['Timestamp']
                start = float(epoch - (epoch % 60))
                if start not in bins:
                    bins.append(start)
                    end = start + 60
                    relevant_df = connections_df.loc[(connections_df['Timestamp'] >= start) & (connections_df['Timestamp'] < end)]
                    ratio = len(relevant_df.loc[relevant_df['IMSI-Exposing Message'] != '']) / len(relevant_df)
                    ratios.append(ratio)
            print(f'{file_dict[file]}: {np.mean(ratios)*100}%')

calculate_ratios(Path('../data/lab-experiments'))
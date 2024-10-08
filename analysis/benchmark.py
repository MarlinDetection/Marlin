# # Plot Benchmark Captures

# Import all prerequisite packages
from datetime import datetime
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os
import pandas as pd
from pathlib import Path

# Top level directory for your data
data_directory = Path('../data')

# Function to plot capture results on a 24 hour scale
def plot_lte_data(connections_folder, label_dict, color_dict, fig_file_path, title):

    # Pre-plot settings
    matplotlib.rc('font', size=16)
    matplotlib.rc('xtick', labelsize=14)
    matplotlib.rc('ytick', labelsize=14)
    fig, ax = plt.subplots(figsize=(10,2.5))
    plt.grid(visible=True,
             linewidth=0.5,
             alpha=0.5)
    xticks_minutes = np.arange(0, 1441, 240)
    yticks_ratios = np.arange(0, 0.501, 0.1)
    ax.set(xlim=(0, 1440),
        xticks=xticks_minutes,
        xticklabels=[pd.to_datetime(tm, unit='m').strftime('%H:%M') for tm in xticks_minutes],
        xlabel='Time of Day',
        ylim=(0,.5),
        yticks=yticks_ratios,
        yticklabels=['{:.0%}'.format(my_yticklabel).replace('%', r'\%') for my_yticklabel in yticks_ratios],
        ylabel='IE Ratio')
    total_ratios = []

    # Iterate through all log files in directory
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

            total_ratios.extend(ratios)

            # Convert epoch bins to minute bins
            for i in range(0,len(bins)):
                dt = datetime.fromtimestamp(bins[i])
                bins[i] = dt.hour * 60 + dt.minute
            
            # Scatter plot
            plt.bar(bins,
                    ratios,
                    width=3,
                    label=label_dict[file],
                    color=color_dict[label_dict[file]],
                    zorder = 3)
    
    my_handles = []
    for entry in color_dict.keys():
        my_handles.append(mpatches.Patch(color=color_dict[entry], label=entry))
    plt.legend(handles=my_handles)

    plt.savefig(fig_file_path, bbox_inches='tight')
    print(f'Saved file {fig_file_path}.')

    print(f'{title} LTE median= {np.median(total_ratios)*100:.2f}%')

# Plot U.S. LTE data
label_dict = {'2023-11-18-provider-1.pkl': 'LTE Medium Density',
                '2023-11-27-provider-1.pkl': 'LTE Medium Density',
                '2024-03-14-provider-1.pkl': 'LTE Medium Density',
                '2024-03-15-provider-1.pkl': 'LTE Medium Density',
                '2023-11-21-low-density-provider-1.pkl': 'LTE Low Density',
                '2023-11-24-football-game-provider-1.pkl': 'LTE High Density',
                '2023-12-13-basketball-provider-1.pkl': 'LTE High Density',
                '2023-11-18-provider-2.pkl': 'LTE Medium Density',
                '2023-11-27-provider-2.pkl': 'LTE Medium Density',
                '2024-03-14-provider-2.pkl': 'LTE Medium Density',
                '2024-03-15-provider-2.pkl': 'LTE Medium Density',
                '2023-11-21-low-density-provider-2.pkl': 'LTE Low Density',
                '2023-11-24-football-game-provider-2.pkl': 'LTE High Density',
                '2023-12-13-basketball-provider-2.pkl': 'LTE High Density'}
color_dict = {'LTE Medium Density': '#264653',
              'LTE Low Density': '#F4A261',
              'LTE High Density': '#2A9D8F'}
plot_lte_data(data_directory / 'lte/provider-1', label_dict, color_dict, 'benchmark-provider-1.pdf', 'Provider-1')
plot_lte_data(data_directory / 'lte/provider-2', label_dict, color_dict, 'benchmark-provider-2.pdf', 'Provider-2')

# Plot European data
label_dict = {'output.pkl': 'European Provider 1',
                'output_2.pkl': 'European Provider 2',
                'output_3.pkl': 'European Provider 1'}
color_dict = {'European Provider 1': '#264653',
                'European Provider 2': '#F4A261'}
plot_lte_data(data_directory / 'lte/euro', label_dict, color_dict, 'benchmark-euro.pdf', 'European')

# Function to plot capture results on a 24 hour scale
def plot_gsm_data(connections_folder, fig_file_path, title):

    # Pre-plot settings
    matplotlib.rc('font', size=16)
    matplotlib.rc('xtick', labelsize=14)
    matplotlib.rc('ytick', labelsize=14)
    fig, ax = plt.subplots(figsize=(10,2.5))
    plt.grid(visible=True,
             linewidth=0.5,
             alpha=0.5)
    xticks_minutes = np.arange(0, 1441, 240)
    yticks_ratios = np.arange(0, 0.501, 0.1)
    ax.set(xlim=(0, 1440),
        xticks=xticks_minutes,
        xticklabels=[pd.to_datetime(tm, unit='m').strftime('%H:%M') for tm in xticks_minutes],
        xlabel='Time of Day',
        ylim=(0,0.5),
        yticks=yticks_ratios,
        yticklabels=['{:.0%}'.format(my_yticklabel).replace('%', r'\%') for my_yticklabel in yticks_ratios],
        ylabel='IE Ratio')
    
    total_ratios = []

    # Iterate through all log files in directory
    for file in os.listdir(connections_folder):

        # Ensure file is in pcap format
        if file.endswith('.pkl'):

            # Read in dataframe
            connections_df = pd.read_pickle(str(connections_folder / file))

            bins = []
            ratios = []

            # Iterate through IMSI-exposing messages
            my_df = connections_df.loc[connections_df['IMSI-Exposing Message'] != '']
            for exposure in my_df.iterrows():
                epoch = exposure[1]['Timestamp']
                start = float(epoch - (epoch % 60))
                if start not in bins:
                    bins.append(start)
                    end = start + 60
                    relevant_df = connections_df.loc[(connections_df['Timestamp'] >= start) & (connections_df['Timestamp'] < end)]
                    ratio = len(relevant_df.loc[relevant_df['IMSI-Exposing Message'] != '']) / len(relevant_df)
                    ratios.append(ratio)

            total_ratios.extend(ratios)

            # Convert epoch bins to minute bins
            for i in range(0,len(bins)):
                dt = datetime.fromtimestamp(bins[i])
                bins[i] = dt.hour * 60 + dt.minute
            
            # Scatter plot
            plt.bar(bins,
                    ratios,
                    width=3,
                    label=file,
                    color='#264653',
                    zorder = 3)

    plt.savefig(fig_file_path, bbox_inches='tight')
    print(f'Saved file {fig_file_path}.')

    print(f'{title} GSM median= {np.median(total_ratios)*100:.2f}%')

# Plot U.S. GSM data
plot_gsm_data(data_directory / 'gsm/provider-2', 'benchmark-gsm.pdf', 'Provider-2')
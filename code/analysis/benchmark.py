# Plot Benchmark Captures

# Import all prerequisite packages
from datetime import date, datetime, time
import matplotlib
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import os
import pandas as pd
from pathlib import Path
import pytz

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
    yticks_ratios = np.arange(0, 0.501, 0.1)

    # Format x-axis as timestamps and show tick marks at 15 minute intervals
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=4))

    # More settings
    ax.set(
        xlabel='Time',
        xlim=[datetime.strptime('1970-1-1 00:00:00', '%Y-%m-%d %H:%M:%S'), datetime.strptime('1970-1-2 00:00:00', '%Y-%m-%d %H:%M:%S')],
        ylim=(0,0.5),
        yticks=yticks_ratios,
        yticklabels=['{:.0%}'.format(my_yticklabel) for my_yticklabel in yticks_ratios],
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
                cur_date = target_timezone.localize(datetime.fromtimestamp(start))
                cur_time = time(cur_date.hour, cur_date.minute, cur_date.second)
                stripped_date = datetime.combine(date(1970, 1, 1), cur_time)
                if stripped_date not in bins:
                    bins.append(stripped_date)
                    end = start + 60
                    relevant_df = connections_df.loc[(connections_df['Timestamp'] >= start) & (connections_df['Timestamp'] < end)]
                    ratio = len(relevant_df.loc[relevant_df['IMSI-Exposing Message'] != '']) / len(relevant_df)
                    ratios.append(ratio)

            total_ratios.extend(ratios)
            
            # Scatter plot
            plt.bar(bins,
                    ratios,
                    width=0.002,
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
    yticks_ratios = np.arange(0, 0.501, 0.1)
    
    # Format x-axis as timestamps and show tick marks at 15 minute intervals
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=4))

    # More settings
    ax.set(
        xlabel='Time',
        xlim=[datetime.strptime('1970-1-1 00:00:00', '%Y-%m-%d %H:%M:%S'), datetime.strptime('1970-1-2 00:00:00', '%Y-%m-%d %H:%M:%S')],
        ylim=(0,0.5),
        yticks=yticks_ratios,
        yticklabels=['{:.0%}'.format(my_yticklabel) for my_yticklabel in yticks_ratios],
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
                cur_date = target_timezone.localize(datetime.fromtimestamp(start))
                cur_time = time(cur_date.hour, cur_date.minute, cur_date.second)
                stripped_date = datetime.combine(date(1970, 1, 1), cur_time)
                if stripped_date not in bins:
                    bins.append(stripped_date)
                    end = start + 60
                    relevant_df = connections_df.loc[(connections_df['Timestamp'] >= start) & (connections_df['Timestamp'] < end)]
                    ratio = len(relevant_df.loc[relevant_df['IMSI-Exposing Message'] != '']) / len(relevant_df)
                    ratios.append(ratio)

            total_ratios.extend(ratios)
            
            # Scatter plot
            plt.bar(bins,
                    ratios,
                    width=0.002,
                    label=file,
                    color='#264653',
                    zorder = 3)

    plt.savefig(fig_file_path, bbox_inches='tight')
    print(f'Saved file {fig_file_path}.')

    print(f'{title} GSM median= {np.median(total_ratios)*100:.2f}%')

# Ensure Eastern Standard time zone
target_timezone = pytz.timezone('America/New_York')

# Top level directory for your data
data_directory = Path('../../data')

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

# Plot U.S. GSM data
plot_gsm_data(data_directory / 'gsm/provider-2', 'benchmark-gsm.pdf', 'Provider-2')
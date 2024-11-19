# Import libraries
from datetime import datetime, time, timedelta, date
import matplotlib
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path

# matplotlib settings before plotting data
def pre_plot_settings():
    # Pre-plot settings
    matplotlib.rc('font', size=16)
    matplotlib.rc('xtick', labelsize=14)
    matplotlib.rc('ytick', labelsize=14)
    fig, ax = plt.subplots(figsize=(10,10))
    plt.grid(visible=True,
                linewidth=0.5,
                alpha=0.5)

    # Show y-axis tick marks at 10% intervals
    yticks_ratios = np.arange(0, 1.001, 0.1)

    # Format x-axis as timestamps and show tick marks at 15 minute intervals
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=15))

    # More settings
    ax.set(
        xlabel='Time',
        xlim=[datetime.strptime('1970-1-1 1:45:00', '%Y-%m-%d %H:%M:%S'), datetime.strptime('1970-1-1 2:15:00', '%Y-%m-%d %H:%M:%S')],
        ylim=(0,1),
        yticks=yticks_ratios,
        yticklabels=['{:.0%}'.format(my_yticklabel) for my_yticklabel in yticks_ratios],
        ylabel='Security Mode Command Ratio')

# Plot data from a given dataframe
def plot_capture(input_df, color, label, offset):

    # Iterate through IMSI-exposing messages
    my_df = input_df.loc[input_df['IMSI-Exposing Message'] != '']
    bins = []
    ratios = []
    for exposure in my_df.iterrows():

        # Strip date from epoch object
        epoch = exposure[1]['Timestamp']
        start = float(epoch - (epoch % 60))
        cur_date = datetime.fromtimestamp(start)
        cur_time = time(cur_date.hour, cur_date.minute, cur_date.second)
        stripped_date = datetime.combine(date(1970, 1, 1), cur_time)

        # Only process the time bin if it has not been previously seen
        if stripped_date not in bins:
            bins.append(stripped_date)
            end = start + 60
            relevant_df = input_df.loc[(input_df['Timestamp'] >= start) & (input_df['Timestamp'] < end)]
            ratio = len(relevant_df.loc[relevant_df['IMSI-Exposing Message'] != '']) / len(relevant_df)
            ratios.append(ratio)

    # Implement offset for grouped plots
    for i in range(0, len(bins)):
        bins[i] += timedelta(seconds=offset)

    # Scatter plot
    plt.bar(bins,
            ratios,
            width=0.0002,
            color=color,
            edgecolor='black',
            label=label,
            zorder = 3)

# matplotlib settings after plotting data
def post_plot_settings():

    # Show legend and save plot to local file
    plt.legend()
    fig_file_path = 'comparison.pdf'
    plt.savefig(fig_file_path, bbox_inches='tight')
    print(f'Saved file {fig_file_path}.')

# Read in data
data_directory = Path('../../data/lte')
dlprobe_df = pd.read_pickle(data_directory / 'comparison/dlprobe.pkl')
ltesniffer_df = pd.read_pickle(data_directory / 'comparison/ltesniffer.pkl')

# Plot both captures
pre_plot_settings()
plot_capture(dlprobe_df, '#0021A5', 'DlProbe', -10)
plot_capture(ltesniffer_df, '#FA4616', 'LTESniffer', 10)
post_plot_settings()
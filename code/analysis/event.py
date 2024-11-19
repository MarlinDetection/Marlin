# Import all prerequisite packages
from datetime import datetime, time, date
import matplotlib
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path
import pytz

# Function to plot capture results on a 24 hour scale
def plot_data(connections_file, file_path):

    # Message Dict
    message_ratios_dict = {"Identity Request": [],
                           "Attach Reject": [],
                           "TAU Reject": [],
                           "Detach Request": [],
                           "Attach Reject": [],
                           "Service Reject": []}
    # Message color settings
    message_color_dict = {'Identity Request':               '#E9C46A',
                          'Authentication Reject':          '#BB2532',
                          'Location Updating Reject':       '#21A179',
                          'CM Service Reject':              '#D76A03',
                          'Attach Reject':                  '#264653',
                          'Detach Request':                 '#F4A261',
                          'RAU Reject':                     '#BB2532',
                          'Authentication Cipher Reject':   '#21A179',
                          'Service Reject':                 '#E76F51',
                          'TAU Reject':                     '#2A9D8F'}

    # Ensure file is in pcap format
    if not connections_file.endswith('.pkl'): return

    # Read in dataframe
    connections_df = pd.read_pickle(connections_file)

    # Iterate through IMSI-exposing messages
    my_df = connections_df.loc[connections_df['IMSI-Exposing Message'] != '']
    bins = []
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
            for message in message_ratios_dict.keys():
                message_ratios_dict[message].append(len(relevant_df.loc[relevant_df['IMSI-Exposing Message'] == message]) / len(relevant_df))

    # Pre-plot settings
    matplotlib.rc("font", size=16)
    matplotlib.rc("xtick", labelsize=14)
    matplotlib.rc("ytick", labelsize=14)
    fig, ax = plt.subplots(figsize=(10,2.5))
    plt.grid(visible=True,
             linewidth=0.5,
             alpha=0.9)
    
    # Format x-axis as timestamps and show tick marks at 15 minute intervals
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=30))

    yticks_ratios = np.arange(0.1, 0.51, 0.1)
    ax.set(
        xlabel='Time of Day',
        xlim=[datetime.strptime('1970-1-1 14:00:00', '%Y-%m-%d %H:%M:%S'), datetime.strptime('1970-1-1 16:00:00', '%Y-%m-%d %H:%M:%S')],
        ylim=(0,0.5),
        yticks=yticks_ratios,
        yticklabels=["{:.0%}".format(my_yticklabel) for my_yticklabel in yticks_ratios],
        ylabel='IE Ratio')
    
    # Bar plot
    bottom_list = [0] * len(message_ratios_dict['Identity Request'])
    for message in message_ratios_dict.keys():
        if not all(v == 0 for v in message_ratios_dict[message]):
            plt.bar(bins,
                    message_ratios_dict[message],
                    width=0.0006,
                    label=message,
                    bottom=bottom_list,
                    color=message_color_dict[message],
                    edgecolor="black",
                    zorder = 3)
            bottom_list = [sum(x) for x in zip(message_ratios_dict[message], bottom_list)]

    plt.legend()
    plt.savefig(file_path, bbox_inches='tight')

# Ensure Eastern Standard time zone
target_timezone = pytz.timezone('America/New_York')

# Plot Event LTE Data
data_directory = Path("../../data/")
plot_data(str(data_directory / 'lte/event/event.pkl'), 'event.pdf')
plot_data(str(data_directory / "lte/event/provider-2.pkl"), 'event-benchmark.pdf')
# Visualize Cellular Network Captures

# Import all prerequisite packages
from datetime import datetime, date, time
import matplotlib
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys

# matplotlib settings before plotting data
def pre_plot_settings():

    # Pre-plot settings
    matplotlib.rc('font', size=16)
    matplotlib.rc('xtick', labelsize=14)
    matplotlib.rc('ytick', labelsize=14)

# Function to plot capture results on a 24 hour scale
def plot_data(connections_file, file_path):

    # Message dictionary to keep track of individual message types
    message_ratios_dict = {'Identity Request':              [],
                          'Authentication Reject':          [],
                          'Location Updating Reject':       [],
                          'CM Service Reject':              [],
                          'Attach Reject':                  [],
                          'Detach Request':                 [],
                          'RAU Reject':                     [],
                          'Authentication Cipher Reject':   [],
                          'Service Reject':                 [],
                          'TAU Reject':                     []}
    # Message color dictionary to assign a color to each message type
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
    max_ratio = 0
    for exposure in my_df.iterrows():
        epoch = exposure[1]['Timestamp']
        start = float(epoch - (epoch % 60))
        cur_date = datetime.fromtimestamp(start)
        cur_time = time(cur_date.hour, cur_date.minute, cur_date.second)
        stripped_date = datetime.combine(date(1970, 1, 1), cur_time)
        if stripped_date not in bins:
            end = start + 60
            relevant_df = connections_df.loc[(connections_df['Timestamp'] >= start) & (connections_df['Timestamp'] < end)]
            if len(relevant_df) > 10:
                bins.append(stripped_date)
                for message in message_ratios_dict.keys():
                    ratio = len(relevant_df.loc[relevant_df['IMSI-Exposing Message'] == message]) / len(relevant_df)
                    message_ratios_dict[message].append(ratio)
                    if ratio > max_ratio:
                        max_ratio = ratio
    
    # Pre-plot settings
    fig, ax = plt.subplots(figsize=(10,2.5))
    plt.grid(visible=True,
             linewidth=0.5,
             alpha=0.9)
    
    # Format x-axis as timestamps and show tick marks at two hour intervals
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))
    y_lim = max_ratio - (max_ratio % 0.1) + 0.1
    yticks_ratios = np.arange(y_lim / 10, y_lim + 0.01, y_lim / 10)
    
    # Remaining plot settings
    ax.set(
        xlabel='Time',
        xlim=[datetime.strptime('1970-1-1 00:00:00', '%Y-%m-%d %H:%M:%S'), datetime.strptime('1970-1-2 00:00:00', '%Y-%m-%d %H:%M:%S')],
        ylabel='IE Ratio',
        ylim=(0, y_lim),
        yticks=yticks_ratios,
        yticklabels=["{:.0%}".format(my_yticklabel) for my_yticklabel in yticks_ratios],
    )
    
    # Bar plot
    bottom_list = [0] * len(message_ratios_dict['Identity Request'])
    for message in message_ratios_dict.keys():
        if not all(v == 0 for v in message_ratios_dict[message]):
            plt.bar(bins,
                    message_ratios_dict[message],
                    width=0.002,
                    label=message,
                    bottom=bottom_list,
                    color=message_color_dict[message],
                    edgecolor="black",
                    zorder = 3)
            bottom_list = [sum(x) for x in zip(message_ratios_dict[message], bottom_list)]

    plt.legend()
    plt.savefig(file_path, bbox_inches='tight')

# Main Function
def main(arguments):
    # matplotlib settings
    pre_plot_settings()
    # Plot capture
    plot_data(sys.argv[1], 'plot.pdf')

# Call main function
if __name__ == '__main__': main(sys.argv)
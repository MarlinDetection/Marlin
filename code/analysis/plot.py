# Visualize Cellular Network Captures

# Import all prerequisite packages
from datetime import datetime
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path
import sys

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

    # Pre-plot settings
    matplotlib.rc("font", size=16)
    matplotlib.rc("xtick", labelsize=14)
    matplotlib.rc("ytick", labelsize=14)
    fig, ax = plt.subplots(figsize=(10,2.5))
    plt.grid(visible=True,
             linewidth=0.5,
             alpha=0.9)
    xticks_minutes = np.arange(0, 1441, 120)
    yticks_ratios = np.arange(0.1, 1.01, 0.1)
    ax.set(xlim=(0, 1440),
        xticks=xticks_minutes,
        xticklabels=[pd.to_datetime(tm, unit='m').strftime("%H:%M") for tm in xticks_minutes],
        xlabel='Time of Day',
        ylim=(0, 1.0),
        yticks=yticks_ratios,
        yticklabels=["{:.0%}".format(my_yticklabel) for my_yticklabel in yticks_ratios],
        ylabel='IE Ratio')

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
        if start not in bins:
            bins.append(start)
            end = start + 60
            relevant_df = connections_df.loc[(connections_df['Timestamp'] >= start) & (connections_df['Timestamp'] < end)]
            for message in message_ratios_dict.keys():
                message_ratios_dict[message].append(len(relevant_df.loc[relevant_df['IMSI-Exposing Message'] == message]) / len(relevant_df))

    # Convert epoch bins to minute bins
    for i in range(0,len(bins)):
        dt = datetime.fromtimestamp(bins[i])
        bins[i] = dt.hour * 60 + dt.minute
    
    # Scatter plot
    bottom_list = [0] * len(message_ratios_dict['Identity Request'])
    for message in message_ratios_dict.keys():
        if not all(v == 0 for v in message_ratios_dict[message]):
            plt.bar(bins,
                    message_ratios_dict[message],
                    width=1,
                    label=message,
                    bottom=bottom_list,
                    color=message_color_dict[message],
                    linewidth=0.4,
                    edgecolor="black",
                    zorder = 3)
            bottom_list = [sum(x) for x in zip(message_ratios_dict[message], bottom_list)]

    plt.legend()
    plt.savefig(file_path, bbox_inches='tight')

# Plot cellular Data
# Main Function
def main(arguments):

    # Pull out connections from LTE packet captures
    plot_data(sys.argv[1], 'plot.pdf')

# Call main function
if __name__ == '__main__': main(sys.argv)
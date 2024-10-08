# Visualize Cellular Network Captures

# Import all prerequisite packages
from datetime import datetime
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
from pathlib import Path
from scipy import stats

# Top-level directory for your data
data_directory = Path('../data/statistics')

# Calculate data
directory_dict ={
    'Provider 1 Captures':          data_directory / 'provider-1',
    'Provider 2 Captures':          data_directory / 'provider-2',
    'Euro Provider 1 Captures':     data_directory / 'euro-provider-1',
    'Euro Provider 2 Captures':     data_directory / 'euro-provider-2',
    'Provider 1 Football Captures': data_directory / 'provider-1-football',
    'Provider 2 Football Captures': data_directory / 'provider-2-football',
    'Event Benchmark':              data_directory / 'event-benchmark',
    'Event':                        data_directory / 'event'
}
ratio_dict = {}

# Get results from event
for key in directory_dict.keys():
    ratios = []
    for file in os.listdir(directory_dict[key]):

        # Ensure file is in pcap format
        if file.endswith('.pkl'):

            # Read in dataframe
            connections_df = pd.read_pickle(str(directory_dict[key] / file))

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
                    ratio = len(relevant_df.loc[relevant_df['IMSI-Exposing Message'] != '']) / len(relevant_df)
                    ratios.append(ratio)

            # Convert epoch bins to minute bins
            for i in range(0,len(bins)):
                dt = datetime.fromtimestamp(bins[i])
                bins[i] = dt.hour * 60 + dt.minute
            position = 0
    ratio_dict[key] = ratios

# Shaprio-Wilk test
print('Shapiro-Wilk Test Results')
for key in ratio_dict.keys():
    print(f'{key}: {stats.shapiro(ratio_dict[key]).pvalue:.1e}')

# Mann-Whitney Test
print('\nMann-Whitney U-Test Results')
for key in ratio_dict.keys():
    if key != 'Event':
        print(f'{key}: {stats.mannwhitneyu(ratio_dict[key], ratio_dict["Event"])[1]:.1e}')

# Create Violin Plot
matplotlib.rc('font', size=18)
matplotlib.rc('xtick', labelsize=20)
matplotlib.rc('ytick', labelsize=20)
fig, ax = plt.subplots(figsize=(22,7))
colors = ['#264653', '#E76F51', '#FF312E', '#FFC759', '#009B72']
colors = ['#0021A5', '#FA4616']

plt.grid(visible=True,
            linewidth=0.5,
            alpha=0.5)
yticks_ratios = np.arange(0.05, 0.55, 0.05)
ax.set(xlabel='',
    xlim=(0.5,8.5),
    xticks=[1,2,3,4,5,6,7,8],
    xticklabels=['U.S. Cell\nProvider 1', 'U.S. Cell\nProvider 2',
                 'Euro Cell\nProvider 1', 'Euro Cell\nProvider 2',
                 'U.S. P1\nFootball Game', 'U.S. P2\nFootball Game',
                 'Court Location\nBenchmark', 'Court Event'],
    ylim=(0,0.51),
    yticks=yticks_ratios,
    yticklabels=['{:.0%}'.format(my_yticklabel).replace('%', r'\%') for my_yticklabel in yticks_ratios],
    ylabel='IMSI Exposure Ratio')

# Create plots for each dataset
counter = 1
for key in ratio_dict.keys():
    if key != 'Event':
        violin = plt.violinplot(dataset=ratio_dict[key], positions=[counter])
        for patch in violin['bodies']: patch.set_color(colors[0])
        for partname in ('cbars', 'cmins', 'cmaxes'):
            violin[partname].set_edgecolor(colors[0])
        
    else:
        violin = plt.violinplot(dataset=ratio_dict[key], positions=[8])
        for patch in violin['bodies']: patch.set_color(colors[1])
        for partname in ('cbars', 'cmins', 'cmaxes'):
            violin[partname].set_edgecolor(colors[1])
    counter += 1

fig_file_path = 'violin-plot.pdf'
plt.savefig(fig_file_path, bbox_inches='tight')
print(f'\nSaved file {fig_file_path}.')
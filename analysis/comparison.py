# Import libraries
from datetime import datetime
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from pathlib import Path

# Read in data
data_directory = Path('../data/lte')
dlprobe_df = pd.read_pickle(data_directory / 'comparison/dlprobe.pkl')
ltesniffer_df = pd.read_pickle(data_directory / 'comparison/ltesniffer.pkl')

# Pre-plot settings
matplotlib.rc('font', size=16)
matplotlib.rc('xtick', labelsize=14)
matplotlib.rc('ytick', labelsize=14)
fig, ax = plt.subplots(figsize=(10,10))
plt.grid(visible=True,
            linewidth=0.5,
            alpha=0.5)
xticks_minutes = np.arange(105, 136, 15)
yticks_ratios = np.arange(0, 1.001, 0.1)
ax.set(xlim=(105, 135),
    xticks=xticks_minutes,
    xticklabels=[pd.to_datetime(tm, unit='m').strftime('%H:%M') for tm in xticks_minutes],
    xlabel='Time',
    ylim=(0,1),
    yticks=yticks_ratios,
    yticklabels=['{:.0%}'.format(my_yticklabel) for my_yticklabel in yticks_ratios],
    ylabel='Security Mode Command Ratio')
colors = ['#0021A5', '#FA4616']

# Iterate through IMSI-exposing messages
my_df = dlprobe_df.loc[dlprobe_df['IMSI-Exposing Message'] != '']
bins = []
ratios = []
for exposure in my_df.iterrows():
    epoch = exposure[1]['Timestamp']
    start = float(epoch - (epoch % 60))
    if start not in bins:
        bins.append(start)
        end = start + 60
        relevant_df = dlprobe_df.loc[(dlprobe_df['Timestamp'] >= start) & (dlprobe_df['Timestamp'] < end)]
        ratio = len(relevant_df.loc[relevant_df['IMSI-Exposing Message'] != '']) / len(relevant_df)
        ratios.append(ratio)

# Convert epoch bins to minute bins
for i in range(0,len(bins)):
    dt = datetime.fromtimestamp(bins[i])
    bins[i] = dt.hour * 60 + dt.minute

bins = bins[:int(len(bins)/2)]
ratios = ratios[:int(len(ratios)/2)]

# Scatter plot
plt.bar(bins,
        ratios,
        width=0.3,
        color=colors[0],
        linewidth=0.3,
        edgecolor='black',
        label='DlProbe',
        zorder = 3)

# Iterate through IMSI-exposing messages
my_df = ltesniffer_df.loc[ltesniffer_df['IMSI-Exposing Message'] != '']
bins = []
ratios = []
for exposure in my_df.iterrows():
    epoch = exposure[1]['Timestamp']
    start = float(epoch - (epoch % 60))
    if start not in bins:
        bins.append(start)
        end = start + 60
        relevant_df = ltesniffer_df.loc[(ltesniffer_df['Timestamp'] >= start) & (ltesniffer_df['Timestamp'] < end)]
        ratio = len(relevant_df.loc[relevant_df['IMSI-Exposing Message'] != '']) / len(relevant_df)
        ratios.append(ratio)

bins = bins[:int(len(bins)/2)]
ratios = ratios[:int(len(ratios)/2)]

# Convert epoch bins to minute bins
for i in range(0,len(bins)):
    dt = datetime.fromtimestamp(bins[i])
    bins[i] = (dt.hour - 20) * 60 + dt.minute

# Scatter plot
plt.bar([x + 0.3 for x in bins],
        ratios,
        width=0.3,
        color=colors[1],
        linewidth=0.4,
        edgecolor='black',
        label='LTESniffer',
        zorder = 3)

plt.legend()
fig_file_path = 'comparison.pdf'
plt.savefig(fig_file_path, bbox_inches='tight')
print(f'Saved file {fig_file_path}.')
# Analysis Code

This directory contains scripts to analyze our existing captures and analyze new `*.pcap` captures. There are no hardware requirements for any script in this directory.

## Reproducibility

Our scripts regenerate the plots and statistics found in our paper. Run any reproducibilty script using the command `python3 <script-name.py>`.

* `benchmark.py` (see paper, Figure 4) plots the data from our benchmark experiments for GSM and LTE network traffic in pdf format. Generated plots include U.S. experiments on two LTE network providers (`benchmark-provider-1.pdf`, `benchmark-provider-2.pdf`), European experiments on two LTE network providers (`benchmark-euro.pdf`), and U.S. experiments on one GSM network provider (`benchmark-gsm.pdf`). We observe relatively low IMSI-exposing ratios during these benchmark experiments.
* `comparison.py` (see paper, Figure 7) compares the performance of two different LTE network analyzers that we use when collecting data. We perform this comparison by running both detectors simultaneously, then looking for what percentage of connections include the common *Security Mode Command* LTE message. The resulting plot (`comparison.pdf`) shows that each detector produces similar results during a two hour test.
* `event.py` (see paper, Figure 5) plots the data for from our event captures in pdf format. Generated plots include data from the day of the event (`event.py`) and a benchmark capture from the same location on a different day (`event-benchmark.pdf`). We observe significantly different IMSI-exposing ratios between these two days, with notably large spikes appearing during the event; these spikes provide strong evidence of IMSI-Catcher presence.
* `lab.py` (see paper, Section VII.B) analyzes the data from our lab experiments and outputs the average IMSI-exposing ratio during each experiment to console. During these experiments, we operated GSM, UMTS, and LTE IMSI-Catchers in a controlled environment. We found that every test produced IMSI-exposing ratios of 100%. This is unsurprising, as the IMSI-Catchers must ask each device for its IMSI after they attempt to connect using their TMSI.
* `statistics.py` (see paper, Figure 6 and Table VI) performs Shapiro-Wilk and Mann-Whitney statistical tests on our data. Results of these tests are printed to console while all data is plotted in a single violin plot (`violin-plot.pdf`). For the Mann-Whitney tests, each capture is compared to the event capture to test for statistical significance of the LTE network traffic generated during the event compared to LTE network traffic generated in various other settings.

## Analyze New Data

We provide three scripts to analyze new *.pcap* captures and output the connections as a pickle file. Each script expects a command line argument of the path to the input file (`python3 <script-name.py> capture.pcap`) and outputs a Pandas dataframe in pickle format that you can use to plot later. This dataframe contains a list of connections with timestamps for connection initiation and the name of an IMSI-exposing message detected during the connection, if applicable. Please note that these scripts may face significant processing times if given long captures containing several hours of cellular network traffic.

* `parse-gsm.py` analyzes a given packet capture featuring one or more GSM connections.
* `parse-umts.py` analyzes a given packet capture featuring one or more UMTS connections.
* `parse-lte.py` analyzes a given packet capture featuring one or more LTE connections.

Finally, we provide a script to plot data processed by one of the `parse-*.py` scripts. Run the script using the command `python3 plot-data.py <capture.pkl>`.

* `plot-data.py` plots a preprocessed cellular network capture in pickle format. The script outputs a plot (`plot.pdf`) containing the IMSI-exposing ratio at various times throughout the capture.
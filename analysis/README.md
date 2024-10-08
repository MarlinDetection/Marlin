# Analysis Code

This directory contains scripts to analyze our existing captures and analyze new *.pcap* captures.

## Reproducibility

Our scripts regenerate the plots and statistics found in our paper. We share a mapping from paper artifact to Python script below:

* **Figure IV:** benchmark.py
* **Figure V:** event.py
* **Figure VI:** statistics.py
* **Table VI:** statistics.py
* **Figure VII:** comparison.py

## Analyze New Data

We provide three scripts to analyze new *.pcap* captures and output the connections as a pickle file. Each script expects a command line argument of the path to the input file:

* **GSM:** parse-gsm.py *<capture.pcap>*
* **UMTS:** parse-umts.py *<capture.pcap>*
* **LTS:** parse-lte.py *<capture.pcap>*
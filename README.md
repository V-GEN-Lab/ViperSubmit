GISAID Submission Method

This repository contains scripts for the GISAID submission of Influenza viruses (H1N1, H3N2, Vic/Yamagata), Dengue (DENV), and SARS-CoV (COV).
Files in the Code Folder

You can download the desired script by navigating to the CODE tab and clicking the download button in the upper right corner.

# Usage and Installation Guide

## Requirements to Run the Script:
- The script for the desired virus.
- An edited CSV as provided in the example (if possible, edit the example file with your data).
- Python 3.
- The necessary libraries specified in the script.

## Installation Steps:
If you do not have Python or the required libraries, use the following commands:
```sh
sudo apt-get update
sudo apt-get install python
sudo apt-get install python-pip
pip install pandas biopython
```
Usage:

For the usage of each script, refer to the specific guide in the GUIDE folder.

Recommendations
Consistent Folder Usage: Always run the scripts in the same folder to ensure the log file is continuously updated. Running the script in a new folder will create a new log.
Dedicated Folder: Create a dedicated folder to run the scripts. The script combines all FASTA files related to the CSV and outputs the final FASTA. Move the final FASTA to another folder to prevent the script from accidentally deleting it.
In the CSV folder, I have provided 3 CSV files with the necessary columns to run each script. Using these tables, the script should work without any issues. Please fill in the data in these tables using the guide provided for each script as previously mentioned.



> **For any questions or suggestions, please contact the CEVIVAS team or send an email to: iago.lima.esib@esib.butantan.br or iagottlima@gmail.com.**


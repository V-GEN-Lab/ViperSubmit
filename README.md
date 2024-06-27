GISAID Submission Method

This repository contains scripts for the GISAID submission of Influenza viruses (H1N1, H3N2, Vic/Yamagata), Dengue (DENV), and SARS-CoV (COV).
Files in the Code Folder

The Code folder contains three scripts for file manipulation:

    Influenza: subGisaid_FLU.py
    Dengue: subGisaid_DENV.py
    SARS-CoV: subGisaid_COV.py

Script Arguments

Each of the three scripts requires four arguments to function:

    --input: The CSV file (METADATA)
    --output: The desired final file name
    --D: The dynamic number
    --fasta: The complete path to the FASTA files related to the inserted CSV

Log Files

The scripts generate log files containing:

    The types and subtypes of the viruses in the CSV
    The dynamic number
    The date (day, month, year, hour)

Recommendations

    Consistent Folder Usage: Always run the scripts in the same folder to ensure the log file is continuously updated. Running the script in a new folder will create a new log.
    Dedicated Folder: Create a dedicated folder to run the scripts. The script combines all FASTA files related to the CSV and outputs the final FASTA. Move the final FASTA to another folder to prevent the script from accidentally deleting it.

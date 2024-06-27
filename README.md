# SubmissionMode
This is the GISAID submission method for Influenza viruses (H1N1, H3N2, Vic/Yamagata), Dengue (DENV), and SARS-CoV (COV).

The files are in the Code folder, which contains the three scripts for file manipulation:

Influenza

subGisaid_FLU.py

Dengue

subGisaid_DENV.py

SARS-CoV

subGisaid_COV.py

The three scripts require only four arguments to function:

    --input consists of the CSV file (METADATA)
    --output consists of the final file name desired
    --D consists of the dynamic number
    --fasta consists of the path to the FASTA files related to the CSV that was inserted (the path must be complete)

The scripts generate log files containing the types and subtypes of the viruses in the CSV, the dynamic number, and the date (day, month, year, hour).

It is preferable to always run the scripts in the same folder so that the log file is always updated. If the script is executed in a new folder, a new log will be created.

It is recommended to create a dedicated folder to run the scripts because the script combines all FASTA files related to the CSV, and then move the final FASTA to another folder to avoid the script accidentally deleting the final FASTA.

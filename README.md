<details open>
  <summary>README</summary>
  
  ## GISAID Submission Method
  
  This repository contains scripts for the GISAID submission of Influenza viruses (H1N1, H3N2, Vic/Yamagata), Dengue (DENV), and SARS-CoV (COV).
  
  ### Files in the Code Folder
  
  You can download the desired script by navigating to the CODE tab and clicking the download button in the upper right corner.
  
  ## Usage and Installation Guide
  
  ### Requirements to Run the Script:
  - The script for the desired virus.
  - An edited CSV as provided in the example (if possible, edit the example file with your data).
  - Python 3.
  - Pandas and biopython
  
  ### Installation Steps:
  If you do not have Python or the required libraries, use the following commands:
  
  ```sh
  sudo apt-get update
  sudo apt-get install python
  sudo apt-get install python-pip
  pip install pandas biopython
  ```
Recommendations:

Consistent Folder Usage: Always run the scripts in the same folder to ensure the log file is continuously updated. Running the script in a new folder will create a new log.

Dedicated Folder: Create a dedicated folder to run the scripts. The script combines all FASTA files related to the CSV and outputs the final FASTA. Move the final FASTA to another folder to prevent the script from accidentally deleting it. Since the script always stores all FASTA files in the folder as intermediate files, and after using them, they will be deleted, please ALWAYS move the final files to a new folder (e.g., final_files) for better code functionality.

In the Suplementary_files, I have provided a exemple of CSV and fasta files with the necessary columns to run each script. Using these tables, the script should work without any issues. Please fill in the data in these tables using the guide provided for each script as previously mentioned.

For any questions or suggestions, please contact the CEVIVAS team or send an email to: iago.lima.esib@esib.butantan.br or iagottlima@gmail.com.

</details>
<details>
  <summary>README_FLU</summary>
Explanations

This README provides an overview of the data columns and script requirements for the SG-FLU project.
Data Columns

    ID: Sample ID
    Subtype: The subtype of the flu (H1N1, H3N2, VIC, or Yama)
    Genome: The name of the FASTA file
    Collection_Date: Collection date
    Segment_1_Coverage: Coverage of segment 1, only those above 80% will be approved
    Segment_2_Coverage: Coverage of segment 2, only those above 80% will be approved
    Segment_3_Coverage: Coverage of segment 3, only those above 80% will be approved
    Segment_4_Coverage: Coverage of segment 4, only those above 80% will be approved
    Segment_5_Coverage: Coverage of segment 5, only those above 80% will be approved
    Segment_6_Coverage: Coverage of segment 6, only those above 80% will be approved
    Segment_7_Coverage: Coverage of segment 7, only those above 80% will be approved
    Segment_8_Coverage: Coverage of segment 8, only those above 80% will be approved
    PARTNER_PROJECT: Partner's name (if not applicable, just put the name of your lab)

Script Explanation
Genome Column:

In the column Genome, please include the name that is in the sample's FASTA file. Each sample should have a different FASTA file.
</details>

<details>
  <summary>README_COV</summary>
Explanations

This README provides an overview of the data columns and script requirements for the SG-COV project.
Data Columns

    ID: Sample ID
    Type: Sample type
    Genome: The name of the FASTA file
    Passed_QC: Quality control (use 'A' for approved samples; only samples marked 'A' will be used)
    State: The state
    Collection_Date: Collection date
    REQUESTING_UNIT: The name of partner laboratories (if not applicable, put the name of your lab)
    PARTNER_PROJECT: Partner's name (if not applicable, just put the name of your lab)


</details>
<details>
  <summary>README_DENV</summary>
  SG-DENV README
Explanations

This README provides an overview of the data columns and script requirements for the SG-DENV project.
Data Columns

    ID: Sample ID
    Genome: The name of the FASTA file
    Serotype: The serotype of the sample
    Genotype: The genotype of the sample
    Passed_QC: Quality control (use 'A' for approved samples, 'R' for rejected samples; only samples marked 'A' will be used)
    State: The state
    Collection_Date: Collection date
    REQUESTING_UNIT: The name of partner laboratories (if not applicable, put the name of your lab)
    PARTNER_PROJECT: Partner's name (if not applicable, just put the name of your lab)

</details>

<div id="tab-container">
    <div class="tab">
        <button class="tablinks" onclick="openTab(event, 'Tab1')">README</button>
        <button class="tablinks" onclick="openTab(event, 'Tab2')">README_Flu</button>
        <button class="tablinks" onclick="openTab(event, 'Tab3')">README_COV</button>
        <button class="tablinks" onclick="openTab(event, 'Tab4')">README_DENV</button>
  </div>
    <div id="Tab1" class="tabcontent">
        <h2>README<h2>
        <p>GISAID Submission Method<p>
    <!-- This repository contains scripts for the GISAID submission of Influenza viruses (H1N1, H3N2, Vic/Yamagata), Dengue (DENV), and SARS-CoV (COV).
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
    
    
    
    > **For any questions or suggestions, please contact the CEVIVAS team or send an email to: iago.lima.esib@esib.butantan.br or iagottlima@gmail.com.** -->
    </div>


    <div id="Tab2" class="tabcontent">
        </h2>README_FLU</h2>
        <p>Explanations<p>
        <!--
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
    
        Author Information:
            Define the partner_authors dictionary with the names of the authors.
            Example:
    
            python
    
        partner_authors = {
            'LACENPA': "Gabriela, Ribeiro; Alex, Lima; Maria, Elias; Sandra, Vessoni; Gleissy, Borges; Kátia, Furtado; Shirley, Chagas; Patrícia, Costa"
        }
    
        It is necessary to put where these authors are from in the column PARTNER_PROJECT, as the script checks to include other authors based on the lab name. If it is only one lab, put the lab name and the authors.
    
    Country of Origin:
    
        Set the country of origin in the DataFrame as follows:
    
        python
    
            df_final['Location'] = 'country'
    
            Replace 'country' with the actual country of origin.
    
    Contributing
    
    To contribute to this project, please fork the repository, create a new branch for your feature or bug fix, and submit a pull request. Ensure that your code follows the project’s style guidelines and includes appropriate tests.
    License
    
    This project is licensed under the MIT License. See the LICENSE file for details.
-->
    </div>
</div>

For questions or suggestions, please open an issue or contact the project maintainers: iago.lima.esib@esib.butantan.gov.br or iagottlima@gmail.com

Feel free to customize the script according to your project's specific requirements and guidelines.

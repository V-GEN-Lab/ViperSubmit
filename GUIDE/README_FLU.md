SG-FLU README
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
Contact

For questions or suggestions, please open an issue or contact the project maintainers: iago.lima.esib@esib.butantan.gov.br or iagottlima@gmail.com

Feel free to customize the script according to your project's specific requirements and guidelines.

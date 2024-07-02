SG-COV README
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

Script Explanation

    Author Names:
        Define the partner_authors dictionary with the names of the authors.

    partner_authors = {
        # Example:
        # 'LabName': "Author1, LastName; Author2, LastName; ..."
    }

State Abbreviations:

    Define the abbreviations dictionary with the state names and their corresponding abbreviations.


    abbreviations = {
        # Example:
        # 'StateName': 'Abbreviation'
    }

Sequence Naming:

    In the df_exchange['Seqs'] column, replace 'country' with your actual country and use the appropriate state abbreviation from the abbreviations dictionary.

    python

    df_exchange['Seqs'] = df_passed_qc.apply(lambda row: f"hCoV-19/country/{abbreviations.get(row['state'], '')}-IB_{row['ID']}/{row['Collection_Date'].year}", axis=1)

Location Column:

    In the df_final['Location'] column, replace 'continent' and 'country' with the actual continent and country of origin.

    python

    df_final['Location'] = df_passed_qc.apply(lambda row: f"continent / country / {row['state']}", axis=1)

Sequencing Technology:

    Set the sequencing technology used. By default, it is 'Illumina'. Replace 'Illumina' with your sequencer if different.

    python

        df_final['Sequencing technology'] = 'Illumina'

Contributing

To contribute to this project, please fork the repository, create a new branch for your feature or bug fix, and submit a pull request. Ensure that your code follows the project’s style guidelines and includes appropriate tests.
License

This project is licensed under the MIT License. See the LICENSE file for details.
Contact

For questions or suggestions, please open an issue or contact the project maintainers.

Feel free to customize this README according to your project's specific requirements and guidelines.

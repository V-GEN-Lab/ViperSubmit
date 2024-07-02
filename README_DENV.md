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

Script Explanation

    Location Column:
        In the df_final['Location'] column, replace 'continent' and 'country' with the actual continent and country of origin.

        python

    df_final['Location'] = df_passed_qc.apply(lambda row: f"continent / country / {row['state']}", axis=1)

Sequence Naming:

    In the df_troca['Seqs'] column, replace 'country' with the actual country of origin and use the appropriate state abbreviation from the siglas dictionary.

    python

    df_troca['Seqs'] = df_passed_qc.apply(lambda row: f"hDenV{row['Serotype']}/country/{siglas.get(row['state'], '')}-{row['ID']}/{row['Collection_Date'].year}", axis=1)

Virus Naming:

    Similarly, for the df_final['Virus name'] column, replace 'country' with the actual country of origin and use the appropriate state abbreviation from the siglas dictionary.

    python

    df_final['Virus name'] = df_passed_qc.apply(lambda row: f"hDenV{row['Serotype']}/country/{siglas.get(row['state'], '')}-{row['ID']}/{row['Collection_Date'].year}", axis=1)

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

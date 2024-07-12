import pandas as pd  # Import pandas library for data manipulation
from datetime import datetime  # Import datetime class to work with dates
import getpass  # Import getpass library to get current username
import argparse  # Import argparse library for command-line argument parsing
import os  # Import os library for operating system interactions
from Bio import SeqIO  # Import Bio.SeqIO library for FASTA file handling
import re  # Import re library for regular expressions
import sys  # Import sys library to exit the program

def main(input_file, output_file, Dynamic, fasta, country, continent):
    # Load the TSV file into a Pandas DataFrame
    df = pd.read_csv(input_file, encoding='latin-1')
    
    # Filter rows where the 'Passed_QC' column is 'A'
    df_passed_qc = df[df['Passed_QC'] == 'A']
    
    # Assertion check to ensure all rows were filtered correctly
    assert len(df_passed_qc) == len(df[df['Passed_QC'] == 'A']), "Not all rows were filtered correctly"
    print("All rows with 'A' in 'Passed QC?' were filtered correctly.")

    # Convert 'Collection_Date' column to datetime type
    df_passed_qc['Collection_Date'] = pd.to_datetime(df_passed_qc['Collection_Date'])

    # Initialize DataFrames for final result and genome exchange
    df_final = pd.DataFrame() 
    df_exchange = pd.DataFrame()
    
    # Create 'Seqs' column with formatted data from existing columns
    df_exchange['Genome'] = df_passed_qc['Genome']
    df_exchange['Seqs'] = df_passed_qc.apply(lambda row: f"hDenV{row['Serotype']}/{country}/{(row['Abbreviations'])}-{row['ID']}/{row['Collection_Date'].year}", axis=1)
    
    # Populate other columns of the final DataFrame
    df_final['Submitter'] = ''
    df_final['FASTA filename'] = f'{output_file}_{Dynamic}.fasta'
    df_final['Virus name'] = df_passed_qc.apply(lambda row: f"hDenV{row['Serotype']}/{country}/{(row['Abbreviations'])}-{row['ID']}/{row['Collection_Date'].year}", axis=1)
    df_final['type'] = 'Dengue Virus'
    df_final['Serotype'] = df_passed_qc.apply(lambda row: f"DENV{row['Serotype']}", axis=1)
    df_final['Host'] = 'Human'
    df_final['Passage details/history'] = 'Original'
    df_final['Collection_Date'] = df_passed_qc['Collection_Date'].dt.date
    df_final['Location'] = df_passed_qc.apply(lambda row: f"{continent} / {country} / {row['REQUESTING_STATE']}", axis=1)
    df_final['Additional location information'] = ''
    df_final['Additional host information'] = ''
    df_final['Sampling Strategy'] = ''
    df_final['Gender'] = 'Unknown'
    df_final['Patient age'] = 'Unknown'
    df_final['Patient status'] = 'Unknown'
    df_final['Disease manifestation'] = ''
    df_final['Specific clinical symptoms'] = ''
    df_final['Specimen source'] = ''
    df_final['Outbreak'] = ''
    df_final['Vaccination History'] = ''
    df_final['Last vaccination date'] = ''
    df_final['Treatment'] = ''
    df_final['Sequencing technology'] = 'Illumina'
    df_final['Assembly method'] = ''
    df_final['Depth of coverage'] = ''
    df_final['Publications'] = ''
    df_final['Originating lab'] = df_passed_qc['REQUESTING_UNIT'] 
    df_final['Address'] = df_passed_qc.apply(lambda row: f"{row['state']},{(row['Abbreviations'])}", axis=1)
    df_final['Sample ID given by the sample provider'] = ''
    df_final['Submitting lab'] = ''
    df_final['Address1'] = ''
    df_final['Sample ID given by the submitting laboratory'] = ''
    df_final['Authors'] = df_passed_qc['Authors']
    df_final['Comment'] = ''
    df_final['Comment Icon'] = ''
    
    # Generate log with subtype information and user details
    Serptype_info = df['Genotype'].unique()
    subtype_log = f'Subtypes: {", ".join(map(str, Serptype_info))}\n'
    log = f'File generated at {datetime.now()} by {getpass.getuser()}\n{subtype_log}Dynamic number: {Dynamic}\n'

    # Save the log to a text file (append mode)
    with open(f'Sub_DENV_log.txt', 'a') as f:
        f.write(log)

    # Save the final DataFrame to a new TSV file
    df_final.to_csv(f'{output_file}_{Dynamic}.tsv', sep='\t', index=False)
    
    # Read the saved file and add/rename necessary columns
    df_gisaid = pd.read_csv(f'{output_file}_{Dynamic}.tsv', sep='\t')
    df_gisaid['Submitter'] = ''
    df_gisaid.rename(columns={'Address1': 'Address'}, inplace=True)
    df_gisaid['FASTA filename'] = f'{output_file}_{Dynamic}.fasta'

    # Remove the old TSV file
    os.remove(f'{output_file}_{Dynamic}.tsv')

    # Define desired columns for the DataFrame
    desired_columns = [
        'submitter', 'fn', 'arbo_virus_name', 'arbo_type', 'arbo_subtype', 
        'arbo_host', 'arbo_passage', 'arbo_collection_date', 'arbo_location', 
        'arbo_add_location', 'arbo_add_host_info', 'arbo_sampling_strategy', 
        'arbo_gender', 'arbo_patient_age', 'arbo_patient_status', 
        'arbo_disease_manifestation', 'arbo_clinical_symptoms', 'arbo_specimen', 
        'arbo_outbreak', 'arbo_last_vaccinated', 'covv_last_vaccination_date', 
        'arbo_treatment', 'arbo_seq_technology', 'arbo_assembly_method', 
        'arbo_coverage', 'arbo_publications', 'arbo_orig_lab', 'arbo_orig_lab_addr', 
        'arbo_provider_sample_id', 'arbo_subm_lab', 'arbo_subm_lab_addr', 
        'arbo_subm_sample_id', 'arbo_authors', 'arbo_comment', 'comment_type'
    ]

    # Transpose and reset the index of the DataFrame
    df_gisaid = df_gisaid.T.reset_index().T 
    df_gisaid.columns = desired_columns

    # Save the final DataFrame to an Excel file
    df_gisaid.to_excel(f'{output_file}_{Dynamic}.xlsx', engine='openpyxl', index=False)

    # Print the log
    print(log)

    
    import subprocess  # Import subprocess library to execute system commands

    # Generate a list with the contents of the "Genoma" column
    genomas = df['Genoma']

    # Get the current directory path
    pwd_output = os.getcwd()
    project_path = fasta

    # Save the list of genomes to a text file
    genomas.to_csv('list.txt', index=False, header=False)

    # Full path to the list file
    list_path = os.path.join(pwd_output, 'list.txt')

    # Destination directory path
    destination_path = pwd_output

    # Change to the project directory
    os.chdir(project_path)

    # Command to copy the files
    command = f"while read value1; do cp */*/$value1 {destination_path}; done < {list_path}"

    # Execute the command to copy the files
    os.system(command)

    # Return to the original directory
    os.chdir(pwd_output)

    # Name of the resulting FASTA file
    fas_file = f'{output_file}_{Dynamic}_RAW.fas'

    # List of FASTA files in the output directory
    fasta_files = [file for file in os.listdir(pwd_output) if file.endswith('.fasta')]

    # List to store all modified records
    all_records = []

    # Iterate over each FASTA file
    for fasta_file in fasta_files:
        # Read the FASTA file
        records = SeqIO.parse(os.path.join(pwd_output, fasta_file), "fasta")
        
        # Modify the header of each record and store in all_records
        for record in records:
            original_header = record.id  # Original header
            new_header = fasta_file  # New header based on the file name
            
            # Update the record header
            record.id = new_header
            record.name = ""  # Clear name
            record.description = ''  # Clear description
            
            # Add the modified record to the list
            all_records.append(record)

    # Write all modified records to the output multi-FASTA file
    print(f"Writing all modified records to {output_file}")
    SeqIO.write(all_records, os.path.join(pwd_output, fas_file), "fasta")

    print("Processing completed.")

    # Remove the original FASTA files
    for fasta_file in fasta_files:
        os.remove(os.path.join(pwd_output, fasta_file))

    print(f"Successfully created single multi-FASTA file {fas_file} in {pwd_output}.")

        # Generate lists from DataFrame columns
    valores_genoma = df_exchange['Genoma'].tolist()
    valores_virus_name = df_exchange['Seqs'].tolist()

    # List to store corresponding sequences
    sequencias_correspondentes = []

    # Iterate over sequences in the multi-FASTA file
    for record in SeqIO.parse(f'{output_file}_{Dynamic}_RAW.fas', "fasta"):
        # Remove ">" from the FASTA header
        fasta_header = record.id.replace(">", "")
        
        # Check if the header matches any value in the Genoma list
        if fasta_header in valores_genoma:
            # Find the index corresponding to the header in the DataFrame
            index = valores_genoma.index(fasta_header)
            
            # Get the new header from the "Seqs" column in the DataFrame
            novo_cabecalho = valores_virus_name[index]
            
            # Replace the original header with the new header
            record.id = novo_cabecalho
            record.name = ""  # Clear name
            record.description = ""  # Clear description
            
            # Add the modified sequence to the list of corresponding sequences
            sequencias_correspondentes.append(record)

    # Write the corresponding sequences to the output FASTA file
    with open(f'{output_file}_{Dynamic}.fasta', "w") as output_handle:
        SeqIO.write(sequencias_correspondentes, output_handle, "fasta")

    # Remove temporary files
    os.remove('list.txt')
    os.remove(f'{output_file}_{Dynamic}_RAW.fas')

    # Análise de argumentos da linha de comando
    parser = argparse.ArgumentParser(description='Processa um arquivo TSV.')
    parser.add_argument('--input', type=str, required=True, help='Caminho para o arquivo de entrada TSV')
    parser.add_argument('--output', type=str, required=True, help='Nome do arquivo de saída TSV')
    parser.add_argument('--D', type=str, required=True, help='Número de dinâmica')
    parser.add_argument('--fasta', type=str, required=True, help='caminho para a pastas dos fastas')
    parser.add_argument('--country', type=str, required=True, help='Número de dinâmica')
    parser.add_argument('--continent', type=str, required=True, help='Número de dinâmica')
    args = parser.parse_args()
   
    main(args.input, args.output, args.D, args.fasta, args.country, args.continent)
   

import pandas as pd  # type: ignore
from datetime import datetime
import getpass
import argparse
import os
from Bio import SeqIO  # type: ignore
import re 
import sys

def main(input_file, output_file, dinamica, fasta):
    # Dictionary of partners
    partner_authors = {}

    # Dictionary of abbreviations
    abbreviations = {}
    
    # Load the TSV file into a Pandas DataFrame
    df = pd.read_csv(input_file)
    
    df['DATA_DA_COLETA'] = pd.to_datetime(df['DATA_DA_COLETA'])
    
    df_passed_qc = df[df['Passed_QC'] == 'A']
    
    assert len(df_passed_qc) == len(df[df['Passed_QC'] == 'A']), "Not all rows were filtered correctly"

    print("All rows with 'A' in 'Passed_QC' were filtered correctly.")
    
    # Open main DataFrame
    df_final = pd.DataFrame() 
    df_exchange = pd.DataFrame()
    df_exchange['Genome'] = df_passed_qc['Genoma']
    df_exchange['Seqs'] = df_passed_qc.apply(lambda row: f"hCoV-19/Brazil/{abbreviations.get(row['UNIDADE_REQUISITANTE_ESTADO'], '')}-IB_{row['CEVIVAS_ID']}/{row['DATA_DA_COLETA'].year}", axis=1)
    
    # Fill other columns of the main DataFrame
    df_final['Submitter'] = ''
    df_final['FASTA filename'] = ''
    df_final['Virus name'] = df_passed_qc.apply(lambda row: f"hCoV-19/Brazil/{abbreviations.get(row['UNIDADE_REQUISITANTE_ESTADO'], '')}-IB_{row['CEVIVAS_ID']}/{row['DATA_DA_COLETA'].year}", axis=1)
    df_final['type'] = 'betacoronavirus'
    df_final['Passage_History'] = 'Original'
    df_final['Collection_Date'] = df_passed_qc['DATA_DA_COLETA']
    df_final['Location'] = df_passed_qc.apply(lambda row: f"South America / Brazil / {row['UNIDADE_REQUISITANTE_ESTADO']}", axis=1)
    df_final['Additional location information'] = ''
    df_final['Host'] = 'Human'
    df_final['Additional host information'] = ''
    df_final['Sampling Strategy'] = ''
    df_final['Gender'] = 'Unknown'
    df_final['Patient age'] = 'Unknown'
    df_final['Patient status'] = 'Unknown'
    df_final['Specimen source'] = ''
    df_final['Outbreak'] = ''
    df_final['Last vaccination'] = ''
    df_final['Treatment'] = ''
    df_final['Sequencing technology'] = 'Illumina'
    df_final['Assembly method'] = ''
    df_final['Coverage'] = ''
    df_final['Originating lab'] = df_passed_qc['UNIDADE_REQUISITANTE']
    df_final['Address'] = df_passed_qc.apply(lambda row: f"{row['UNIDADE_REQUISITANTE_ESTADO']}, {abbreviations.get(row['UNIDADE_REQUISITANTE_ESTADO'], '')}", axis=1)
    df_final['Sample ID given by the sample provider'] = ''
    df_final['Submitting lab'] = 'Instituto Butantan'
    df_final['Address1'] = 'Sao Paulo, SP'
    df_final['Sample ID given by the submitting laboratory'] = ''
    df_final['Authors'] = df_passed_qc.apply(lambda row: partner_authors.get(row['PARCEIRO_PROJETO'], ''), axis=1)
    df_final['Comment'] = ''
    df_final['Comment Icon'] = ''
    
    # Generate the log
    # Print the number of dynamics and the virus type
    Serptype_info = df_final['type'].unique()
    subtype_log = f'Subtypes: {", ".join(map(str, Serptype_info))}\n'
    log = f'File generated on {datetime.now()} by {getpass.getuser()}\n{subtype_log}Number of dynamics: {dinamica}\n'

    # Save the log in a text file (append mode)
    with open(f'Sub_COV_log.txt', 'a') as f:
        f.write(log)

    # Add the extra columns requested by GISAID and arrange the other columns
    desired_columns = [
    'submitter1', 'fn', 'covv_virus_name', 'covv_type', 'covv_passage', 'covv_collection_date',
    'covv_location', 'covv_add_location', 'covv_host', 'covv_add_host_info', 'covv_sampling_strategy',
    'covv_gender', 'covv_patient_age', 'covv_patient_status', 'covv_specimen', 'covv_outbreak',
    'covv_last_vaccinated', 'covv_treatment', 'covv_seq_technology', 'covv_assembly_method', 
    'covv_coverage', 'covv_orig_lab', 'covv_orig_lab_addr', 'covv_provider_sample_id', 'covv_subm_lab',
    'covv_subm_lab_addr', 'covv_subm_sample_id', 'covv_authors', 'covv_comment', 'comment_type'
    ]
    
    df_final.to_csv(f'{output_file}_{dinamica}.tsv', sep='\t', index=False)
    df_gabi = pd.read_csv(f'{output_file}_{dinamica}.tsv', sep='\t')
    df_gabi['Submitter'] = 'gabriela.rribeiro'
    df_gabi.rename(columns={'Address1': 'Address'}, inplace=True)
    df_gabi['FASTA filename'] = f'{output_file}_{dinamica}.fasta'
    
    # Transform the file into Excel and remove temporary files
    df_gabi = df_gabi.T.reset_index().T 

    df_gabi.columns = desired_columns

    df_gabi.to_excel(f'{output_file}_{dinamica}.xlsx', engine='openpyxl', index=False)

    os.remove(f'{output_file}_{dinamica}.tsv')

    
    print(log)
    import subprocess

    # Generate a list with the contents of the "Genoma" column
    genomes = df['Genoma']

    # Get the current directory path and the fasta project path
    pwd_output = os.getcwd()
    project_path = fasta

    # Save genomes to a text file
    genomes.to_csv('list.txt', index=False, header=False)

    # Path to the file containing the list of files to be copied
    list_path = os.path.join(pwd_output, 'list.txt')  # Change to the actual filename

    # Destination directory path
    destination_path = pwd_output  

    # Change directory to the project path
    os.chdir(project_path)

    # Command to copy the files
    command = f"while read value1; do cp */*/$value1 {destination_path}; done < {list_path}"

    # Execute the command
    os.system(command)

    # Change back to the original directory
    os.chdir(pwd_output)

    # Create the FASTA file path
    fas_file = f'{output_file}_{dinamica}_RAW.fas'

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
            
            # Update the record's header
            record.id = new_header
            record.name = ""  # Clear the name
            record.description = ''  # Clear the description (optional)
            
            # Append the modified record to the list
            all_records.append(record)

    # Write all modified records to the output multi-FASTA file
    print(f"Writing all modified records to {output_file}")
    SeqIO.write(all_records, os.path.join(pwd_output, fas_file), "fasta")

    print("Processing completed.")

    # Remove the original FASTA files
    for fasta_file in fasta_files:
        os.remove(os.path.join(pwd_output, fasta_file))

    print(f"Single multi-FASTA file {output_file} successfully created in {pwd_output}.")

    #PART-3
     # Transform columns into lists
    valores_genoma = df_exchange['Genoma'].tolist()
    valores_virus_name = df_exchange['Seqs'].tolist()

    # List to store corresponding sequences
    sequencias_correspondentes = []

    # Iterate over sequences in the multi-FASTA file
    for record in SeqIO.parse(f'{output_file}_{dinamica}_RAW.fas', "fasta"):
        # Remove ">" from the FASTA file header
        fasta_header = record.id.replace(">", "")

        # Check if the header matches any value in the Genome list
        if fasta_header in valores_genoma:
            # Find the index corresponding to the header in the DataFrame
            index = valores_genoma.index(fasta_header)
            
            # Get the new header from the "Virus name" column in the DataFrame
            novo_cabecalho = valores_virus_name[index]
            
            # Replace the original header with the new header
            record.id = novo_cabecalho
            record.name = ""  # Clear the name
            record.description = ""  # Clear the description
            
            # Append the modified record to the corresponding sequences list
            sequencias_correspondentes.append(record)

    # Write the modified FASTA file
    with open(f'{output_file}_{dinamica}.fasta', "w") as output_handle:
        SeqIO.write(sequencias_correspondentes, output_handle, "fasta")

    # Remove temporary files
    os.remove('list.txt')
    os.remove(f'{output_file}_{dinamica}_RAW.fas')

    print(f'Dynamics {dinamica} completed.')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Processa um arquivo TSV.')
    parser.add_argument('--input', type=str, required=True, help='Caminho para o arquivo de entrada TSV')
    parser.add_argument('--output', type=str, required=True, help='Nome do arquivo de saída TSV')
    parser.add_argument('--D', type=str, required=True, help='Número de dinâmica')
    parser.add_argument('--fasta', type=str, required=True, help='Número de dinâmica')
    args = parser.parse_args()
   
    main(args.input, args.output, args.D, args.fasta)



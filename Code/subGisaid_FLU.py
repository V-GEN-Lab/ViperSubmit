import pandas as pd # type: ignore # Library for data manipulation
from datetime import datetime # Library for date manipulation
import getpass # Library to get the current user's name
import argparse # Library for command-line argument parsing
import os # Library for operating system interactions
from Bio import SeqIO # type: ignore # Library for biological sequence manipulation
import re # Library for regular expression operations
import sys # Library for Python system interactions
import subprocess # Library for executing system commands

def main(input_file, output_file, Dynamic, fasta):
    # Dictionary for segment mapping
    segments_mapping = {
        'segment_1_Coverage':'PB2',
        'segment_2_Coverage':'PB1',
        'segment_3_Coverage':'PA',
        'segment_4_Coverage':'HA',
        'segment_5_Coverage':'NP',
        'segment_6_Coverage':'NA',
        'segment_7_Coverage':'MP',
        'segment_8_Coverage':'NS'
    }
    
    # Another dictionary for segment mapping
    segments_mapping77 = {
        'PB2': 'segment1',
        'PB1': 'segment2',
        'PA': 'segment3',
        'HA': 'segment4',
        'NP': 'segment5',
        'NA': 'segment6',
        'MP': 'segment7',
        'NS': 'segment8'
    }

    # Dictionary of authors by partner
    autores_por_parceiro = {}

    # Load the TSV file into a Pandas DataFrame
    df = pd.read_csv(input_file, encoding='latin-1')
    
    # Filter the DataFrame
    df = df[df['LABORATORIO_SEQUENCIADOR'] == 'INSTITUTO BUTANTAN']
    df = df[df['PassedQC'] == 'A']
    
    # Convert columns to numeric values
    df[['segment_1_Coverage', 'segment_2_Coverage', 'segment_3_Coverage',
        'segment_4_Coverage', 'segment_5_Coverage', 'segment_6_Coverage',
        'segment_7_Coverage', 'segment_8_Coverage']] = df[['segment_1_Coverage', 'segment_2_Coverage', 'segment_3_Coverage',
                                                           'segment_4_Coverage', 'segment_5_Coverage', 'segment_6_Coverage',
                                                           'segment_7_Coverage', 'segment_8_Coverage']].apply(pd.to_numeric, errors='coerce')

    # Create the final DataFrame with all rows and blank columns
    df_final = pd.DataFrame(index=df.index, columns=['Isolate_Id', 'Segment_Ids', 'Isolate_Name', 'Subtype', 'Lineage', 'Passage_History', 
                                                      'Location', 'province', 'sub_province', 'Location_Additional_info', 'Host', 
                                                      'Host_Additional_info', 'Seq_Id (HA)', 'Seq_Id (NA)', 'Seq_Id (PB1)', 'Seq_Id (PB2)', 
                                                      'Seq_Id (PA)', 'Seq_Id (MP)', 'Seq_Id (NS)', 'Seq_Id (NP)', 'Seq_Id (HE)', 'Seq_Id (P3)', 
                                                      'Submitting_Sample_Id', 'Authors', 'Originating_Lab_Id', 'Originating_Sample_Id', 
                                                      'Collection_Month', 'Collection_Year', 'Collection_Date', 'Antigen_Character', 
                                                      'Adamantanes_Resistance_geno', 'Oseltamivir_Resistance_geno', 'Zanamivir_Resistance_geno', 
                                                      'Peramivir_Resistance_geno', 'Other_Resistance_geno', 'Adamantanes_Resistance_pheno', 
                                                      'Oseltamivir_Resistance_pheno', 'Zanamivir_Resistance_pheno', 'Peramivir_Resistance_pheno', 
                                                      'Other_Resistance_pheno', 'Host_Age', 'Host_Age_Unit', 'Host_Gender', 'Health_Status', 
                                                      'Note', 'PMID'])
    
    colunas_selecionadas = []
    dados_lista_troca = [] 
    df['Collection_Date'] = pd.to_datetime(df['Collection_Date'])
    
    # Create an empty DataFrame to store the results
    df_gen_rename = pd.DataFrame(columns=['Index', 'segment', 'Valor', 'Seq_Id (HA)', 'Seq_Id (NA)', 'Seq_Id (PB1)', 'Seq_Id (PB2)', 'Seq_Id (PA)', 'Seq_Id (MP)', 'Seq_Id (NS)', 'Seq_Id (NP)', 'Seq_Id (HE)', 'Seq_Id (P3)'])

    # Iterate over each row in the DataFrame
    for index, row in df.iterrows():
        # Check if the coverage of each segment is greater than 80%
        segments_above_80 = [seg for seg, cov in row.items() if seg.startswith('segment_') and cov > 80.0]
        # Fill in the segments above 80% in the final DataFrame
        genome_value = row['Genome']
        for segment in segments_above_80:
            # Get the real name of the segment from the mapping dictionary
            segment_name = segments_mapping.get(segment, '')
            if segment not in colunas_selecionadas:
                colunas_selecionadas.append(segment)
            
        # Fill in the segments above 80% in the final DataFrame and in df_gen_rename
        for segment in segments_above_80:
            # Get the real name of the segment from the mapping dictionary
            segment_name = segments_mapping.get(segment, '')
            if segment_name:
                # Create the value to be inserted into the cell
                cell_value = f'A/{row["state"]}/{row["ID"]}/{row["Collection_Date"].year}_{segment_name}'
                
                # Fill in the cell corresponding to the segment with the created value in df_final
                df_final.at[index, f'Seq_Id ({segment_name})'] = cell_value
                
                # Fill in the cell corresponding to the segment with the created value in df_gen_rename
                df_gen_rename.at[index, f'Seq_Id ({segment_name})'] = cell_value
                dados_lista_troca.append({'Genome': genome_value, f'Seq_Id_{segment_name}': cell_value})

    # Create the Lista4Troca DataFrame from the collected data
    df_lista_troca = pd.DataFrame(dados_lista_troca)
    
    colunas_selecionadas.append('Genome')
    # Initialize the new 'Genome_rename' column with empty values in the df_gen DataFrame

    for index, row in df_lista_troca.iterrows():
        genome = row['Genome']
        seqs = []
        segment = None
        
        # Look for the segment in the "Seq_Id_X" columns and concatenate them
        for column in df_lista_troca.columns:
            if column.startswith("Seq_Id_"):
                column_value = row[column]
                if not pd.isnull(column_value):
                    seqs.append(column_value)
                    if segment is None:
                        segment = column_value.split("_")[-1]  # Get the last argument of the cell
        
        # Combine all sequences into a single string, separated by "_"
        seqs_combined = "_".join(seqs)
        
        # Update the "Seqs" column
        df_lista_troca.at[index, 'Seqs'] = seqs_combined
        
        # Rename the segment in the Genome
        if segment is not None:
            if segment in segments_mapping77:
                genome_split = genome.split("_")
                genome_split[0] = segments_mapping77[segment]
                genome = "_".join(genome_split)
        
        # Update the "Genome" column
        df_lista_troca.at[index, 'Genome'] = genome

    # Remove "Seq_Id_X" columns
    df_lista_troca = df_lista_troca.drop(columns=[col for col in df_lista_troca if col.startswith("Seq_Id_")])
    
    # Fill in other columns of the final DataFrame
    df_final['Isolate_Id'] = ''
    df_final['Segment_Ids'] = ''
    df_final['Isolate_Name'] = df.apply(lambda row: f"{row['Type']}/{row['state']}/{row['ID']}/{row['Collection_Date'].year}", axis=1)
    df_final['Subtype'] = df['Subtype']
    df_final.loc[df_final['Subtype'] == 'Victoria', 'Lineage'] = 'Victoria'
    df_final.loc[df_final['Subtype'] == 'Victoria', 'Subtype'] = ''
    df_final['Passage_History'] = 'Original'
    df_final['Location'] = 'country'
    df_final['province'] = ''
    df_final['sub_province'] = ''
    df_final['Location_Additional_info'] = ''
    df_final['Host'] = 'Human'
    df_final['Host_Additional_info'] = ''
    df_final['Authors'] = df.apply(lambda row: autores_por_parceiro.get(row['PARTNER_PROJECT'], ''), axis=1)
    df_final['Originating_Lab_Id'] = ""
    df_final['Collection_Date'] = df['Collection_Date'].dt.date
    
    # Generate the log
    subtype_info = df['Subtype'].unique()
    subtype_log = f'Subtypes: {", ".join(subtype_info)}\n'
    log = f'File generated on {datetime.now()} by {getpass.getuser()}\n{subtype_log}Dynamics number: {Dynamic}\n'

    
    # Save the log to a text file (append mode)
    with open(f'Sub_FLU_log.txt', 'a') as f:
        f.write(log)

    # Save the final DataFrame to a new TSV file
    df_final.to_excel(f'{output_file}_{Dynamic}.xlsx', engine='openpyxl', index=False)
    
    # Print the Dynamic number and virus type
    print(log)

    
    # PART 2 - FASTA File Processing

    # Generate a list with the contents of the "Genome" column
    Genomes = df['Genome']

    # Get the current directory path
    pwd_output = os.getcwd()
    project_path = fasta

    # Save the genomes to a text file called 'list.txt'
    Genomes.to_csv('list.txt', index=False, header=False)

    # Full path to the list
    list_path = os.path.join(pwd_output, 'list.txt')  # Path to the file containing the list of files to be copied

    # Path to the destination directory
    destination_path = pwd_output  # Directory where the files will be copied

    # Change to the project directory
    os.chdir(project_path)

    # Command to copy the files listed in 'list.txt' to the destination directory
    command = f"while read value1; do cp */*/$value1 {destination_path}; done < {list_path}"

    # Execute the copy command
    os.system(command)

    # Return to the original directory
    os.chdir(pwd_output)

    # List all .fasta files in the current directory
    fasta_files = [file for file in os.listdir(pwd_output) if file.endswith('.fasta')]

    # Open the output file in write mode
    with open(f'{output_file}_{Dynamic}_RAW.fas', 'w') as output_handle:
        # Iterate over each FASTA file
        for fasta_file in fasta_files:
            # Open each FASTA file in read mode
            with open(os.path.join(pwd_output, fasta_file), 'r') as input_handle:
                # Write the content of the FASTA file to the output file
                output_handle.write(input_handle.read())

    # Remove the original FASTA files after being concatenated
    for fasta_file in fasta_files:
        os.remove(os.path.join(pwd_output, fasta_file))

    # Print success message
    print(f"Single multi-fasta file subGisaidFLU.fasta successfully created in {pwd_output}.")


   # PART 3 - Rename Headers in Multi-FASTA File

    # Extract the values from the 'Genome' column and remove the ">" from the FASTA headers
    valores_tsv = df_lista_troca['Genome'].tolist()
    valores_tsv = [header.replace(">", "") for header in valores_tsv]

    # List to store the corresponding sequences
    sequencias_correspondentes = []

    # Iterate over the sequences in the multi-FASTA file
    for record in SeqIO.parse(f'{output_file}_{Dynamic}_RAW.fas', "fasta"):
        # Remove the ">" from the FASTA header
        fasta_header = record.id.replace(">", "")
        
        # Check if the header matches any value in the TSV list
        if fasta_header in valores_tsv:
            # Find the corresponding index for the header in the DataFrame
            index = valores_tsv.index(fasta_header)
            
            # Get the new header from the "Seqs" column in the DataFrame
            novo_cabecalho = df_lista_troca.at[index, 'Seqs']
            
            # Replace the original header with the new header
            record.id = novo_cabecalho
            record.name = ""  # Clear the name
            record.description = ""  # Clear the description
            
            # Add the sequence with the new header to the list
            sequencias_correspondentes.append(record)

    # Write the corresponding sequences to a new multi-FASTA file
    with open(f'{output_file}_{Dynamic}.fasta', "w") as output_handle:
        SeqIO.write(sequencias_correspondentes, output_handle, "fasta")

    # Remove the temporary files used in the process
    os.remove('list.txt')
    os.remove(f'{output_file}_{Dynamic}_RAW.fas')



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Processa um arquivo TSV.')
    parser.add_argument('--input', type=str, help='Caminho para o arquivo de entrada TSV')
    parser.add_argument('--output', type=str, help='Nome do arquivo de saída TSV')
    parser.add_argument('--D', type=str, help='Número de Dynamic')
    parser.add_argument('--fasta', type=str, required=True, help='caminho para a pastas dos fastas')
    args = parser.parse_args()
   
    main(args.input, args.output, args.D)




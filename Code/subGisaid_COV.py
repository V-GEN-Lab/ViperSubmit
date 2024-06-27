import pandas as pd # type: ignore
from datetime import datetime
import getpass
import argparse
import os
from Bio import SeqIO # type: ignore
import re 
import sys

def main(input_file, output_file, dinamica):
    # Dicionário de parceiros
    autores_por_parceiro = {}

    #dicionario de siglas
    siglas = {}
    
    # Carregar o arquivo TSV em um DataFrame do Pandas
    df = pd.read_csv(input_file)
    
    df['DATA_DA_COLETA'] = pd.to_datetime(df['DATA_DA_COLETA'])
    
    df_passed_qc = df[df['Passed_QC'] == 'A']
    
    assert len(df_passed_qc) == len(df[df['Passed_QC'] == 'A']), "Nem todas as linhas foram filtradas corretamente"

    print("Todas as linhas com 'A' em 'Passed_QC' foram filtradas corretamente.")


    
    



    #Abrir DataFrame principal
    df_final = pd.DataFrame() 
    df_troca = pd.DataFrame()
    df_troca['Genoma'] = df_passed_qc['Genoma']
    df_troca['Seqs'] = df_passed_qc.apply(lambda row: f"hCoV-19/Brazil/{siglas.get(row['UNIDADE_REQUISITANTE_ESTADO'], '')}-IB_{row['CEVIVAS_ID']}/{row['DATA_DA_COLETA'].year}", axis=1)

    
    # Preencher outras colunas do DataFrame principal
    df_final['Submitter'] = ''
    df_final['FASTA filename'] = ''
    df_final['Virus name'] = df_passed_qc.apply(lambda row: f"hCoV-19/Brazil/{siglas.get(row['UNIDADE_REQUISITANTE_ESTADO'], '')}-IB_{row['CEVIVAS_ID']}/{row['DATA_DA_COLETA'].year}", axis=1)
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
    df_final['Address'] = df_passed_qc.apply(lambda row: f"{row['UNIDADE_REQUISITANTE_ESTADO']}, {siglas.get(row['UNIDADE_REQUISITANTE_ESTADO'], '')}", axis=1)
    df_final['Sample ID given by the sample provider'] = ''
    df_final['Submitting lab'] = 'Instituto Butantan'
    df_final['Address1'] = 'Sao Paulo, SP'
    df_final['Sample ID given by the submitting laboratory'] = ''
    df_final['Authors'] = df_passed_qc.apply(lambda row: autores_por_parceiro.get(row['PARCEIRO_PROJETO'], ''), axis=1)
    df_final['Comment'] = ''
    df_final['Comment Icon'] = ''
    
    # Gerar o log
    # Imprimir o número de dinâmica e o tipo do vírus
    Serptype_info = df_final['type'].unique()
    subtype_log = f'Subtypes: {", ".join(map(str, Serptype_info))}\n'
    log = f'Arquivo gerado em {datetime.now()} por {getpass.getuser()}\n{subtype_log}Número de dinâmica: {dinamica}\n'


    # Salvar o log em um arquivo de texto (modo de adição)
    with open(f'Sub_COV_log.txt', 'a') as f:
        f.write(log)

   
 
    #Adicionar as colunas extras solicitadas pelo gisaid e arrumar as outras colunas
    colunas_desejadas = [
    'submitter1', 'fn', 'covv_virus_name', 'covv_type', 'covv_passage', 'covv_collection_date',
    'covv_location', 'covv_add_location', 'covv_host', 'covv_add_host_info', 'covv_sampling_strategy',
    'covv_gender', 'covv_patient_age', 'covv_patient_status', 'covv_specimen', 'covv_outbreak',
    'covv_last_vaccinated', 'covv_treatment', 'covv_seq_technology', 'covv_assembly_method', 
    'covv_coverage', 'covv_orig_lab', 'covv_orig_lab_addr', 'covv_provider_sample_id', 'covv_subm_lab',
    'covv_subm_lab_addr', 'covv_subm_sample_id', 'covv_authors', 'covv_comment', 'comment_type'
    ]
    
    df_final.to_csv(f'{output_file}_{dinamica}.tsv', sep='\t', index=False)
    df_gisaid = pd.read_csv(f'{output_file}_{dinamica}.tsv', sep='\t')
    df_gisaid['Submitter'] = 'gabriela.rribeiro'
    df_gisaid.rename(columns={'Address1': 'Address'}, inplace=True)
    df_gisaid['FASTA filename'] = f'{output_file}_{dinamica}.fasta'
    
    #trasformar o arquivo em excel e remoção de arquivos temporarios
    df_gisaid = df_gisaid.T.reset_index().T 

    df_gisaid.columns=colunas_desejadas

    df_gisaid.to_excel(f'{output_file}_{dinamica}.xlsx', engine='openpyxl', index=False)

    os.remove(f'{output_file}_{dinamica}.tsv')
  

    
    print(log)
    #PARTE2---------------------------------------------------------------------------------FASTAFILE
  
    import subprocess

    # Gerar uma lista com o conteúdo da coluna "Genoma"
    genomas = df['Genoma']

    # Obter o caminho do diretório atual e dos fastas
    pwd_output = os.getcwd()
    project_path = '/storage/zuleika/volume1/project/carol/sarsCov2/CeVIVAS/project'
    
    genomas.to_csv('list.txt', index=False, header=False)

    # Caminho para o arquivo contendo a lista de arquivos a serem copiados
    list_path = os.path.join(pwd_output, 'list.txt')  # Altere para o nome real do arquivo

    # Caminho para o diretório de destino
    destination_path = pwd_output  

    os.chdir(project_path)

    # Comando para copiar os arquivos
    command = f"while read value1; do cp */*/$value1 {destination_path}; done < {list_path}"

    # Executa o comando
    os.system(command)
    os.chdir(pwd_output)
    fas_file = f'{output_file}_{dinamica}_RAW.fas'

# Lista de arquivos FASTA no diretório de saída
    fasta_files = [file for file in os.listdir(pwd_output) if file.endswith('.fasta')]

    # Lista para armazenar todos os registros modificados
    all_records = []

    # Itera sobre cada arquivo FASTA
    for fasta_file in fasta_files:
        
        
        # Lê o arquivo FASTA
        records = SeqIO.parse(os.path.join(pwd_output, fasta_file), "fasta")
        
        # Modifica o cabeçalho de cada registro e armazena em all_records
        for record in records:
            original_header = record.id  # Cabeçalho original
            new_header = fasta_file  # Novo cabeçalho baseado no nome do arquivo
            
            # Atualiza o cabeçalho do registro
            record.id = new_header
            record.name = ""  # Limpar o nome
            record.description = ''  # Limpa a descrição (opcional)
            
            # Adiciona o registro modificado à lista
            all_records.append(record)
            
            # Imprime os cabeçalhos original e novo
            

    # Escreve todos os registros modificados no arquivo multifasta de saída
    print(f"Escrevendo todos os registros modificados em {output_file}")
    SeqIO.write(all_records, os.path.join(pwd_output, fas_file), "fasta")

    print("Processamento concluído.")

    

    # Remove os arquivos FASTA originais
    for fasta_file in fasta_files:
        os.remove(os.path.join(pwd_output, fasta_file))

    print(f"Arquivo multi-fasta único subGisaidFLU.fasta criado com sucesso em {pwd_output}.")

    
    #Parte3-------------------------------------------------------------------------------- Arrumar os fastas
   
    #trasformar as colunas em listas 
    valores_genoma = df_troca['Genoma'].tolist()
    valores_virus_name = df_troca['Seqs'].tolist()
    
    sequencias_correspondentes = []

# Iterar sobre as sequências no arquivo multi-FASTA
    for record in SeqIO.parse(f'{output_file}_{dinamica}_RAW.fas', "fasta"):
    # Remover o ">" do cabeçalho do arquivo FASTA
        fasta_header = record.id.replace(">", "")
    
        # Verificar se o cabeçalho corresponde a algum valor na lista do Genoma
        if fasta_header in valores_genoma:
            # Encontrar o índice correspondente ao cabeçalho no DataFrame
            index = valores_genoma.index(fasta_header)
            
            # Obter o novo cabeçalho da coluna "Virus name" no DataFrame
            novo_cabecalho = valores_virus_name[index]
            
            # Substituir o cabeçalho original pelo novo cabeçalho
            record.id = novo_cabecalho
            record.name = ""  # Limpar o nome
            record.description = ""  # Limpar a descrição
            
            
            sequencias_correspondentes.append(record)
            #print(sequencias_correspondentes)
    
    #escreve o fasta
    with open(f'{output_file}_{dinamica}.fasta', "w") as output_handle:
        SeqIO.write(sequencias_correspondentes, output_handle, "fasta")
    
    
    #remove os arquivos temporarios
    os.remove('list.txt')
    os.remove(f'{output_file}_{dinamica}_RAW.fas')
    print(f'Dinamica {dinamica} concluida ')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Processa um arquivo TSV.')
    parser.add_argument('--input', type=str, required=True, help='Caminho para o arquivo de entrada TSV')
    parser.add_argument('--output', type=str, required=True, help='Nome do arquivo de saída TSV')
    parser.add_argument('--D', type=str, required=True, help='Número de dinâmica')
    args = parser.parse_args()
   
    main(args.input, args.output, args.D)



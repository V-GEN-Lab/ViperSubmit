import pandas as pd  # Importa a biblioteca pandas para manipulação de dados
from datetime import datetime  # Importa a classe datetime para trabalhar com datas
import getpass  # Importa a biblioteca getpass para obter o nome do usuário atual
import argparse  # Importa a biblioteca argparse para análise de argumentos da linha de comando
import os  # Importa a biblioteca os para interações com o sistema operacional
from Bio import SeqIO  # Importa a biblioteca Bio.SeqIO para manipulação de arquivos FASTA
import re  # Importa a biblioteca re para expressões regulares
import sys  # Importa a biblioteca sys para encerrar o programa

def main(input_file, output_file, dinamica, fasta):
    # Dicionário de mapeamento de autores por parceiro
    autores_por_parceiro = {
        'LACENPA': "Gabriela, Ribeiro; Alex, Lima; Maria, Elias; Sandra, Vessoni; Gleissy, Borges; Kátia, Furtado; Shirley, Chagas; Patrícia, Costa",
        'LACENAL': "Gabriela, Ribeiro; Alex, Lima; Maria, Elias; Sandra, Vessoni; Hazerral, Santos; Eladja, Mendes",
        'LACENMT': "Gabriela, Ribeiro; Alex, Lima; Maria, Elias; Sandra, Vessoni; Stephanni, Silva; Luana, Silva; Julia, Almeida; Elaine, Oliveira",
        'LACENDF': "Gabriela, Ribeiro; Alex, Lima; Maria, Elias; Sandra, Vessoni",
        'LACENPR': "Gabriela, Ribeiro; Alex, Lima; Maria, Elias; Sandra, Vessoni; Guilherme, Becker; Aline, Freund; Irina, Riediger; Leticia, Santos",
        'PMPSP': "Gabriela, Ribeiro; Alex, Lima; Maria, Elias; Sandra, Vessoni; Luciano, Oliveira; Sumire, Hibi; Isabelle, Ferreira; Melissa, Palmieri; Eduardo, Mais",
        'FB': "Gabriela, Ribeiro; Alex, Lima; Maria, Elias; Sandra, Vessoni",
        'HRPSP': "Gabriela, Ribeiro; Alex, Lima; Maria, Elias; Sandra, Vessoni; Elaine, Santos; Debora, La-Roque; Mariane, Evaristo; Evandra, Rodrigues; Simone, Kashima",
        'SBC': "Gabriela, Ribeiro; Alex, Lima; Maria, Elias; Sandra, Vessoni; Tancredo, Santos; Sheila, Costa",
        'ZOOSP': "Gabriela, Ribeiro; Alex, Lima; Maria, Elias; Sandra, Vessoni; Luciano, Oliveira; Sumire, Hibi; Isabelle, Ferreira; Melissa, Palmieri; Eduardo, Mais",
        'VEB': "Gabriela, Ribeiro; Alex, Lima; Maria, Elias; Sandra, Vessoni; Ezequiel Aparecido, dos Santos; Rita, Altino; Carlos, dos Santos; Thiago, Dionísio"
    }

    # Dicionário de siglas dos estados
    siglas = {
        "SAO PAULO": "SP",
        "ALAGOAS": "AL",
        "PARANA": "PR",
        "PARA": "PA",
        "MATO GROSSO": "MT",
        "MINAS GERAIS": "MG"
    }

    # Carregar o arquivo TSV em um DataFrame do Pandas
    df = pd.read_csv(input_file, encoding='latin-1')
    
    # Filtrar as linhas onde a coluna 'Passed_QC' é 'A'
    df_passed_qc = df[df['Passed_QC'] == 'A']
    
    # Verificação de assertiva para garantir que todas as linhas foram filtradas corretamente
    assert len(df_passed_qc) == len(df[df['Passed_QC'] == 'A']), "Nem todas as linhas foram filtradas corretamente"
    print("Todas as linhas com 'A' em 'Passed QC?' foram filtradas corretamente.")

    # Converter a coluna 'DATA_DA_COLETA' para o tipo datetime
    df_passed_qc['DATA_DA_COLETA'] = pd.to_datetime(df_passed_qc['DATA_DA_COLETA'])

    # Inicializar DataFrames para o resultado final e troca de genomas
    df_final = pd.DataFrame() 
    df_troca = pd.DataFrame()
    
    # Criar coluna 'Seqs' com os dados formatados a partir das colunas existentes
    df_troca['Genoma'] = df_passed_qc['Genoma']
    df_troca['Seqs'] = df_passed_qc.apply(lambda row: f"hDenV{row['Serotype']}/Brazil/{siglas.get(row['UNIDADE_REQUISITANTE_ESTADO'], '')}-{row['CEVIVAS_ID_NEW']}/{row['DATA_DA_COLETA'].year}", axis=1)
    
    # Preencher outras colunas do DataFrame final
    df_final['Submitter'] = ''
    df_final['FASTA filename'] = f'{output_file}_{dinamica}.fasta'
    df_final['Virus name'] = df_passed_qc.apply(lambda row: f"hDenV{row['Serotype']}/Brazil/{siglas.get(row['UNIDADE_REQUISITANTE_ESTADO'], '')}-{row['CEVIVAS_ID_NEW']}/{row['DATA_DA_COLETA'].year}", axis=1)
    df_final['type'] = 'Dengue Virus'
    df_final['Serotype'] = df_passed_qc.apply(lambda row: f"DENV{row['Serotype']}", axis=1)
    df_final['Host'] = 'Human'
    df_final['Passage details/history'] = 'Original'
    df_final['Collection_Date'] = df_passed_qc['DATA_DA_COLETA'].dt.date
    df_final['Location'] = df_passed_qc.apply(lambda row: f"South America / Brazil / {row['UNIDADE_REQUISITANTE_ESTADO']}", axis=1)
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
    df_final['Originating lab'] = df_passed_qc['UNIDADE_REQUISITANTE']
    df_final['Address'] = df_passed_qc.apply(lambda row: f"{row['UNIDADE_REQUISITANTE_ESTADO']}, {siglas.get(row['UNIDADE_REQUISITANTE_ESTADO'], '')}", axis=1)
    df_final['Sample ID given by the sample provider'] = ''
    df_final['Submitting lab'] = 'Instituto Butantan'
    df_final['Address1'] = 'Sao Paulo, SP'
    df_final['Sample ID given by the submitting laboratory'] = ''
    df_final['Authors'] = df_passed_qc.apply(lambda row: autores_por_parceiro.get(row['PARCEIRO_PROJETO'], ''), axis=1)
    df_final['Comment'] = ''
    df_final['Comment Icon'] = ''
    
    # Gerar o log com informações sobre os subtipos e o usuário
    Serptype_info = df['Genotype'].unique()
    subtype_log = f'Subtypes: {", ".join(map(str, Serptype_info))}\n'
    log = f'Arquivo gerado em {datetime.now()} por {getpass.getuser()}\n{subtype_log}Número de dinâmica: {dinamica}\n'

    # Salvar o log em um arquivo de texto (modo de adição)
    with open(f'Sub_DENV_log.txt', 'a') as f:
        f.write(log)

    # Salvar o DataFrame final em um novo arquivo TSV
    df_final.to_csv(f'{output_file}_{dinamica}.tsv', sep='\t', index=False)
    
    # Ler o arquivo salvo e adicionar/renomear colunas necessárias
    df_gisaid = pd.read_csv(f'{output_file}_{dinamica}.tsv', sep='\t')
    df_gisaid['Submitter'] = 'gabriela.rribeiro'
    df_gisaid.rename(columns={'Address1': 'Address'}, inplace=True)
    df_gisaid['FASTA filename'] = f'{output_file}_{dinamica}.fasta'

    # Remover o arquivo TSV antigo
    os.remove(f'{output_file}_{dinamica}.tsv')

    # Definir colunas desejadas para o DataFrame
    colunas_desejadas = [
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

    # Transpor e redefinir o índice do DataFrame
    df_gisaid = df_gisaid.T.reset_index().T 
    df_gisaid.columns = colunas_desejadas

    # Salvar o DataFrame final em um arquivo Excel
    df_gisaid.to_excel(f'{output_file}_{dinamica}.xlsx', engine='openpyxl', index=False)

    # Imprimir o log
    print(log)
    
    
    # PARTE 2 - Processamento de arquivos FASTA
    import subprocess  # Importa a biblioteca subprocess para executar comandos do sistema

    # Gerar uma lista com o conteúdo da coluna "Genoma"
    genomas = df['Genoma']

    # Obter o caminho do diretório atual
    pwd_output = os.getcwd()
    project_path = fasta
    
    # Salvar a lista de genomas em um arquivo de texto
    genomas.to_csv('list.txt', index=False, header=False)

    # Caminho completo para a lista
    list_path = os.path.join(pwd_output, 'list.txt')

    # Caminho para o diretório de destino
    destination_path = pwd_output

    # Mudar para o diretório do projeto
    os.chdir(project_path)

    # Comando para copiar os arquivos
    command = f"while read value1; do cp */*/$value1 {destination_path}; done < {list_path}"

    # Executa o comando para copiar os arquivos
    os.system(command)

    # Voltar para o diretório original
    os.chdir(pwd_output)

    # Nome do arquivo FASTA resultante
    fas_file = f'{output_file}_{dinamica}_RAW.fas'

    # Lista de arquivos FASTA no diretório de saída
    fasta_files = [file for file in os.listdir(pwd_output) if file.endswith('.fasta')]

    # Lista para armazenar todos os registros modificados
    all_records = []

    # Iterar sobre cada arquivo FASTA
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
            record.description = ''  # Limpar a descrição
            
            # Adiciona o registro modificado à lista
            all_records.append(record)

    # Escreve todos os registros modificados no arquivo multifasta de saída
    print(f"Escrevendo todos os registros modificados em {output_file}")
    SeqIO.write(all_records, os.path.join(pwd_output, fas_file), "fasta")

    print("Processamento concluído.")

    # Remove os arquivos FASTA originais
    for fasta_file in fasta_files:
        os.remove(os.path.join(pwd_output, fasta_file))

    print(f"Arquivo multi-fasta único subGisaidFLU.fasta criado com sucesso em {pwd_output}.")

    # Parte 3 - Renomear cabeçalhos no arquivo multifasta
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
            
            # Adicionar a sequência modificada à lista de sequências correspondentes
            sequencias_correspondentes.append(record)
    
    # Escrever as sequências correspondentes no arquivo FASTA de saída
    with open(f'{output_file}_{dinamica}.fasta', "w") as output_handle:
        SeqIO.write(sequencias_correspondentes, output_handle, "fasta")
    
    # Remover arquivos temporários
    os.remove('list.txt')
    os.remove(f'{output_file}_{dinamica}_RAW.fas')

if __name__ == "__main__":
    # Análise de argumentos da linha de comando
    parser = argparse.ArgumentParser(description='Processa um arquivo TSV.')
    parser.add_argument('--input', type=str, required=True, help='Caminho para o arquivo de entrada TSV')
    parser.add_argument('--output', type=str, required=True, help='Nome do arquivo de saída TSV')
    parser.add_argument('--D', type=str, required=True, help='Número de dinâmica')
    parser.add_argument('--fasta', type=str, required=True, help='caminho para a pastas dos fastas')
    args = parser.parse_args()
   
    # Chama a função principal com os argumentos fornecidos
    main(args.input, args.output, args.D)

import pandas as pd # type: ignore # Biblioteca para manipulação de dados
from datetime import datetime # Biblioteca para manipulação de datas
import getpass # Biblioteca para obter o nome do usuário atual
import argparse # Biblioteca para análise de argumentos da linha de comando
import os # Biblioteca para interações com o sistema operacional
from Bio import SeqIO # type: ignore # Biblioteca para manipulação de sequências biológicas
import re # Biblioteca para operações com expressões regulares
import sys # Biblioteca para interações com o sistema Python
import subprocess # Biblioteca para execução de comandos do sistema

def main(input_file, output_file, dinamica, fasta):
    # Dicionário de mapeamento de segments
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
    
    # Outro dicionário de mapeamento de segments
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

    # Dicionário de autores por parceiro
    autores_por_parceiro = {
        'LACENPA': "Gabriela, Ribeiro; Alex, Lima; Maria, Elias; Sandra, Vessoni; Gleissy, Borges; Kátia, Furtado; Shirley, Chagas; Patrícia, Costa",
        'LACENAL': "Gabriela, Ribeiro; Alex, Lima; Maria, Elias; Sandra, Vessoni; Hazerral, Santos; Eladja, Mendes",
        'LACENMT': "Gabriela, Ribeiro; Alex, Lima; Maria, Elias; Sandra, Vessoni; Stephanni, Silva; Luana, Silva; Julia, Almeida; Elaine, Oliveira",
        'LACENDF': "Gabriela, Ribeiro; Alex, Lima; Maria, Elias; Sandra, Vessoni",
        'LACENPR': "Gabriela, Ribeiro; Alex, Lima; Maria, Elias; Sandra, Vessoni; Guilherme, Becker;  Aline, Freund; Irina, Riediger; Leticia, Santos",
        'PMPSP': "Gabriela, Ribeiro; Alex, Lima; Maria, Elias; Sandra, Vessoni; Luciano, Oliveira; Sumire, Hibi; Isabelle, Ferreira; Melissa, Palmieri; Eduardo, Mais",
        'FB': "Gabriela, Ribeiro; Alex, Lima; Maria, Elias; Sandra, Vessoni",
        'HRPSP': "Gabriela, Ribeiro; Alex, Lima; Maria, Elias; Sandra, Vessoni; Elaine, Santos; Debora, La-Roque; Mariane, Evaristo; Evandra, Rodrigues; Simone, Kashima",
        'SBC': "Gabriela, Ribeiro; Alex, Lima; Maria, Elias; Sandra, Vessoni; Tancredo, Santos; Sheila, Costa"
    }

    # Carregar o arquivo TSV em um DataFrame do Pandas
    df = pd.read_csv(input_file, encoding='latin-1')
    
    # Filtrar o DataFrame
    df = df[df['LABORATORIO_SEQUENCIADOR'] == 'INSTITUTO BUTANTAN']
    df = df[df['PassedQC'] == 'A']
    
    # Converter as colunas para valores numéricos
    df[['segment_1_Coverage', 'segment_2_Coverage', 'segment_3_Coverage',
        'segment_4_Coverage', 'segment_5_Coverage', 'segment_6_Coverage',
        'segment_7_Coverage', 'segment_8_Coverage']] = df[['segment_1_Coverage', 'segment_2_Coverage', 'segment_3_Coverage',
                                                           'segment_4_Coverage', 'segment_5_Coverage', 'segment_6_Coverage',
                                                           'segment_7_Coverage', 'segment_8_Coverage']].apply(pd.to_numeric, errors='coerce')

    # Criar DataFrame final com todas as linhas e colunas em branco
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
    df['DATA_DA_COLETA'] = pd.to_datetime(df['DATA_DA_COLETA'])
    
    # Criar um DataFrame vazio para armazenar os resultados
    df_gen_rename = pd.DataFrame(columns=['Index', 'segment', 'Valor', 'Seq_Id (HA)', 'Seq_Id (NA)', 'Seq_Id (PB1)', 'Seq_Id (PB2)', 'Seq_Id (PA)', 'Seq_Id (MP)', 'Seq_Id (NS)', 'Seq_Id (NP)', 'Seq_Id (HE)', 'Seq_Id (P3)'])

    # Iterar sobre cada linha do DataFrame
    for index, row in df.iterrows():
        # Verificar se a cobertura de cada segment é superior a 80%
        segments_acima_80 = [seg for seg, cov in row.items() if seg.startswith('segment_') and cov > 80.0]
        # Preencher os segments acima de 80% no DataFrame final
        valor_genoma = row['Genoma']
        for segment in segments_acima_80:
            # Obter o nome real do segment a partir do dicionário de mapeamento
            nome_segment = segments_mapping.get(segment, '')
            if segment not in colunas_selecionadas:
                colunas_selecionadas.append(segment)
            
        # Preencher os segments acima de 80% no DataFrame final e em df_gen_rename
        for segment in segments_acima_80:
            # Obter o nome real do segmento a partir do dicionário de mapeamento
            nome_segment = segments_mapping.get(segment, '')
            if nome_segment:
                # Criar o valor a ser inserido na célula
                valor_celula = f'A/{row["UNIDADE_REQUISITANTE_ESTADO"]}/{row["CEVIVAS_ID"]}/{row["DATA_DA_COLETA"].year}_{nome_segment}'
                
                # Preencher a célula correspondente ao segment com o valor criado em df_final
                df_final.at[index, f'Seq_Id ({nome_segment})'] = valor_celula
                
                # Preencher a célula correspondente ao segment com o valor criado em df_gen_rename
                df_gen_rename.at[index, f'Seq_Id ({nome_segment})'] = valor_celula
                dados_lista_troca.append({'Genoma': valor_genoma, f'Seq_Id_{nome_segment}': valor_celula})

    # Criar o DataFrame Lista4Troca a partir dos dados coletados
    df_lista_troca = pd.DataFrame(dados_lista_troca)
    
    colunas_selecionadas.append('Genoma')
    # Inicializar a nova coluna 'Genoma_rename' com valores vazios no DataFrame df_gen

    for index, row in df_lista_troca.iterrows():
        genoma = row['Genoma']
        seqs = []
        segmento = None
        
        # Procurar o segmento nas colunas "Seq_Id_X" e concatená-las
        for coluna in df_lista_troca.columns:
            if coluna.startswith("Seq_Id_"):
                valor_coluna = row[coluna]
                if not pd.isnull(valor_coluna):
                    seqs.append(valor_coluna)
                    if segmento is None:
                        segmento = valor_coluna.split("_")[-1]  # Obtém o último argumento da célula
        
        # Combina todas as sequências em uma única string, separadas por "_"
        seqs_combined = "_".join(seqs)
        
        # Atualizar a coluna "Seqs"
        df_lista_troca.at[index, 'Seqs'] = seqs_combined
        
        # Renomear o segmento no Genoma
        if segmento is not None:
            if segmento in segments_mapping77:
                genoma_split = genoma.split("_")
                genoma_split[0] = segments_mapping77[segmento]
                genoma = "_".join(genoma_split)
        
        # Atualizar a coluna "Genoma"
        df_lista_troca.at[index, 'Genoma'] = genoma

    # Remover colunas "Seq_Id_X"
    df_lista_troca = df_lista_troca.drop(columns=[col for col in df_lista_troca if col.startswith("Seq_Id_")])
    
    # Preencher outras colunas do DataFrame final
    df_final['Isolate_Id'] = ''
    df_final['Segment_Ids'] = ''
    df_final['Isolate_Name'] = df.apply(lambda row: f"{row['Type']}/{row['UNIDADE_REQUISITANTE_ESTADO']}/{row['CEVIVAS_ID']}/{row['DATA_DA_COLETA'].year}", axis=1)
    df_final['Subtype'] = df['Subtype']
    df_final.loc[df_final['Subtype'] == 'Victoria', 'Lineage'] = 'Victoria'
    df_final.loc[df_final['Subtype'] == 'Victoria', 'Subtype'] = ''
    df_final['Passage_History'] = 'Original'
    df_final['Location'] = 'Brazil'
    df_final['province'] = ''
    df_final['sub_province'] = ''
    df_final['Location_Additional_info'] = ''
    df_final['Host'] = 'Human'
    df_final['Host_Additional_info'] = ''
    df_final['Authors'] = df.apply(lambda row: autores_por_parceiro.get(row['PARCEIRO_PROJETO'], ''), axis=1)
    df_final['Originating_Lab_Id'] = "3483"
    df_final['Collection_Date'] = df['DATA_DA_COLETA'].dt.date
    
    # Gerar o log
    subtype_info = df['Subtype'].unique()
    subtype_log = f'Subtypes: {", ".join(subtype_info)}\n'
    log = f'Arquivo gerado em {datetime.now()} por {getpass.getuser()}\n{subtype_log}Número de dinâmica: {dinamica}\n'

    
    # Salvar o log em um arquivo de texto (modo de adição)
    with open(f'Sub_FLU_log.txt', 'a') as f:
        f.write(log)

    # Salvar o DataFrame final em um novo arquivo TSV
    df_final.to_excel(f'{output_file}_{dinamica}.xlsx', engine='openpyxl', index=False)
    
    # Imprimir o número de dinâmica e o tipo do vírus
    print(log)
    
    # PARTE 2 - Processamento de arquivos FASTA

    # Gerar uma lista com o conteúdo da coluna "Genoma"
    genomas = df['Genoma']

    # Obter o caminho do diretório atual
    pwd_output = os.getcwd()
    project_path = fasta

    # Salvar os genomas em um arquivo de texto chamado 'list.txt'
    genomas.to_csv('list.txt', index=False, header=False)

    # Caminho completo para a lista
    list_path = os.path.join(pwd_output, 'list.txt')  # Caminho para o arquivo contendo a lista de arquivos a serem copiados

    # Caminho para o diretório de destino
    destination_path = pwd_output  # Diretório onde os arquivos serão copiados

    # Mudar para o diretório do projeto
    os.chdir(project_path)

    # Comando para copiar os arquivos listados em 'list.txt' para o diretório de destino
    command = f"while read value1; do cp */*/$value1 {destination_path}; done < {list_path}"

    # Executar o comando de cópia
    os.system(command)

    # Voltar para o diretório original
    os.chdir(pwd_output)

    # Listar todos os arquivos .fasta no diretório atual
    fasta_files = [file for file in os.listdir(pwd_output) if file.endswith('.fasta')]

    # Abrir o arquivo de saída em modo de escrita
    with open(f'{output_file}_{dinamica}_RAW.fas', 'w') as output_handle:
        # Iterar sobre cada arquivo FASTA
        for fasta_file in fasta_files:
            # Abrir cada arquivo FASTA em modo de leitura
            with open(os.path.join(pwd_output, fasta_file), 'r') as input_handle:
                # Escrever o conteúdo do arquivo FASTA no arquivo de saída
                output_handle.write(input_handle.read())

    # Remover os arquivos FASTA originais após serem concatenados
    for fasta_file in fasta_files:
        os.remove(os.path.join(pwd_output, fasta_file))

    # Imprimir mensagem de sucesso
    print(f"Arquivo multi-fasta único subGisaidFLU.fasta criado com sucesso em {pwd_output}.")

    

    # Parte 3 - Renomear cabeçalhos no arquivo multifasta

    # Extrair os valores da coluna 'Genoma' e removendo o ">" dos cabeçalhos do arquivo FASTA
    valores_tsv = df_lista_troca['Genoma'].tolist()
    valores_tsv = [header.replace(">", "") for header in valores_tsv]

    # Lista para armazenar as sequências correspondentes
    sequencias_correspondentes = []

    # Iterar sobre as sequências no arquivo multi-FASTA
    for record in SeqIO.parse(f'{output_file}_{dinamica}_RAW.fas', "fasta"):
        # Remover o ">" do cabeçalho do arquivo FASTA
        fasta_header = record.id.replace(">", "")
        
        # Verificar se o cabeçalho corresponde a algum valor na lista do TSV
        if fasta_header in valores_tsv:
            # Encontrar o índice correspondente ao cabeçalho no DataFrame
            index = valores_tsv.index(fasta_header)
            
            # Obter o novo cabeçalho da coluna "Seqs" no DataFrame
            novo_cabecalho = df_lista_troca.at[index, 'Seqs']
            
            # Substituir o cabeçalho original pelo novo cabeçalho
            record.id = novo_cabecalho
            record.name = ""  # Limpar o nome
            record.description = ""  # Limpar a descrição
            
            # Adicionar a sequência com o novo cabeçalho à lista
            sequencias_correspondentes.append(record)

    # Escrever as sequências correspondentes em um novo arquivo multi-FASTA
    with open(f'{output_file}_{dinamica}.fasta', "w") as output_handle:
        SeqIO.write(sequencias_correspondentes, output_handle, "fasta")

    # Remover os arquivos temporários usados no processo
    os.remove('list.txt')
    os.remove(f'{output_file}_{dinamica}_RAW.fas')



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Processa um arquivo TSV.')
    parser.add_argument('--input', type=str, help='Caminho para o arquivo de entrada TSV')
    parser.add_argument('--output', type=str, help='Nome do arquivo de saída TSV')
    parser.add_argument('--D', type=str, help='Número de dinâmica')
    parser.add_argument('--fasta', type=str, required=True, help='caminho para a pastas dos fastas')
    args = parser.parse_args()
   
    main(args.input, args.output, args.D)




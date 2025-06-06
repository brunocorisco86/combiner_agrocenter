import pandas as pd
import sqlite3
import os
import glob
import logging
import re

# Define o caminho base do repositório (relativo ao diretório do script)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Define os caminhos para entrada e saída
INPUT_FOLDER = os.path.join(BASE_DIR, 'assets', 'dados_sensores')
OUTPUT_FOLDER = os.path.join(BASE_DIR, 'outputs')
DATABASE_FOLDER = os.path.join(BASE_DIR, 'database')

# Garante que os diretórios de saída e banco existem
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(DATABASE_FOLDER, exist_ok=True)

# Define os caminhos dos arquivos de saída
OUTPUT_CSV = os.path.join(OUTPUT_FOLDER, 'dados_combinados.csv')
OUTPUT_NULOS_CSV = os.path.join(OUTPUT_FOLDER, 'nulos_data.csv')
OUTPUT_LOG = os.path.join(OUTPUT_FOLDER, 'processamento_nulos.log')
OUTPUT_DB = os.path.join(DATABASE_FOLDER, 'dados_sensores.db')

# Configura logging para salvar informações sobre valores nulos
logging.basicConfig(
    filename=OUTPUT_LOG,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Lista para armazenar todos os DataFrames e linhas com data nula/inválida
all_dataframes = []
nulos_dataframes = []

# Percorre todas as planilhas .xlsx na pasta de entrada
files = glob.glob(os.path.join(INPUT_FOLDER, "*.xlsx"))
if not files:
    print(f"Nenhum arquivo .xlsx encontrado na pasta: {INPUT_FOLDER}")
    logging.error(f"Nenhum arquivo .xlsx encontrado na pasta: {INPUT_FOLDER}")
else:
    print("Arquivos encontrados:", files)
    logging.info(f"Arquivos encontrados: {files}")
    for file in files:
        file_name = os.path.basename(file)
        print(f"Processando arquivo: {file_name}")
        logging.info(f"Processando arquivo: {file_name}")
        
        # Carrega o arquivo Excel
        try:
            xls = pd.ExcelFile(file)
        except Exception as e:
            print(f"Erro ao ler {file_name}: {e}")
            logging.error(f"Erro ao ler {file_name}: {e}")
            continue
        
        # Percorre todas as abas do arquivo
        for sheet_name in xls.sheet_names:
            print(f"  Lendo aba: {sheet_name}")
            logging.info(f"Lendo aba: {sheet_name} de {file_name}")
            try:
                df = pd.read_excel(file, sheet_name=sheet_name)
                logging.info(f"  {len(df)} linhas lidas na aba {sheet_name} de {file_name}")
                
                # Padroniza nomes das colunas
                df.columns = (df.columns.str.lower()
                            .str.strip()
                            .str.replace(' ', '_')
                            .str.normalize('NFKD')
                            .str.encode('ascii', errors='ignore')
                            .str.decode('ascii'))
                
                # Verifica se a coluna 'data' existe
                if 'data' not in df.columns:
                    print(f"Coluna 'data' não encontrada em {file_name}, aba {sheet_name}. Colunas disponíveis: {list(df.columns)}")
                    logging.error(f"Coluna 'data' não encontrada em {file_name}, aba {sheet_name}. Colunas disponíveis: {list(df.columns)}")
                    continue
                
                # Identifica linhas com 'data' nula ou vazia antes da conversão
                nulos_antes = df[df['data'].isna() | df['data'].eq('') | df['data'].str.strip().eq('')]
                if not nulos_antes.empty:
                    print(f"Valores nulos ou vazios encontrados na coluna 'data' em {file_name}, aba {sheet_name}: {len(nulos_antes)} linhas")
                    logging.warning(f"Valores nulos ou vazios na coluna 'data' em {file_name}, aba {sheet_name}: {len(nulos_antes)} linhas")
                    nulos_antes = nulos_antes.copy()
                    nulos_antes['nome_arquivo'] = file_name
                    nulos_antes['tipo_de_evento'] = sheet_name
                    nulos_dataframes.append(nulos_antes)
                    for idx, row in nulos_antes.iterrows():
                        logging.warning(f"Linha {idx} com data nula/vazia: {row.to_dict()}")
                
                # Remove linhas com 'data' nula ou vazia
                df = df[~(df['data'].isna() | df['data'].eq('') | df['data'].str.strip().eq(''))]
                if df.empty:
                    print(f"Nenhuma linha válida após filtrar 'data' em {file_name}, aba {sheet_name}")
                    logging.warning(f"Nenhuma linha válida após filtrar 'data' em {file_name}, aba {sheet_name}")
                    continue
                
                # Converte a coluna 'data' para datetime com formato explícito
                df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y %H:%M:%S', errors='coerce')
                
                # Identifica linhas com 'data' NaT após conversão
                nulos_apos = df[df['data'].isna()]
                if not nulos_apos.empty:
                    print(f"Valores inválidos na coluna 'data' após conversão em {file_name}, aba {sheet_name}: {len(nulos_apos)} linhas")
                    logging.warning(f"Valores inválidos na coluna 'data' após conversão em {file_name}, aba {sheet_name}: {len(nulos_apos)} linhas")
                    nulos_apos = nulos_apos.copy()
                    nulos_apos['nome_arquivo'] = file_name
                    nulos_apos['tipo_de_evento'] = sheet_name
                    nulos_dataframes.append(nulos_apos)
                    for idx, row in nulos_apos.iterrows():
                        logging.warning(f"Linha {idx} com data inválida após conversão: {row.to_dict()}")
                
                # Remove linhas com 'data' NaT
                df = df[~df['data'].isna()]
                if df.empty:
                    print(f"Nenhuma linha válida após filtrar 'data' NaT em {file_name}, aba {sheet_name}")
                    logging.warning(f"Nenhuma linha válida após filtrar 'data' NaT em {file_name}, aba {sheet_name}")
                    continue
                
                # Converte 'data' de volta para string no formato DD/MM/YYYY HH:MM:SS
                df['data'] = df['data'].dt.strftime('%d/%m/%Y %H:%M:%S')
                
                # Extrai apenas dígitos de 'nome_do_aviario'
                if 'nome_do_aviario' in df.columns:
                    df['nome_do_aviario'] = df['nome_do_aviario'].astype(str).str.extract(r'(\d+)')
                    # Registra linhas onde 'nome_do_aviario' não contém dígitos
                    nulos_aviario = df[df['nome_do_aviario'].isna()]
                    if not nulos_aviario.empty:
                        print(f"Valores sem dígitos em 'nome_do_aviario' em {file_name}, aba {sheet_name}: {len(nulos_aviario)} linhas")
                        logging.warning(f"Valores sem dígitos em 'nome_do_aviario' em {file_name}, aba {sheet_name}: {len(nulos_aviario)} linhas")
                        nulos_aviario = nulos_aviario.copy()
                        nulos_aviario['nome_arquivo'] = file_name
                        nulos_aviario['tipo_de_evento'] = sheet_name
                        nulos_dataframes.append(nulos_aviario)
                        df = df[~df['nome_do_aviario'].isna()]
                        if df.empty:
                            print(f"Nenhuma linha válida após filtrar 'nome_do_aviario' em {file_name}, aba {sheet_name}")
                            logging.warning(f"Nenhuma linha válida após filtrar 'nome_do_aviario' em {file_name}, aba {sheet_name}")
                            continue
                
                # Adiciona a coluna 'tipo_de_evento' baseado no nome da aba
                df['tipo_de_evento'] = sheet_name
                
                all_dataframes.append(df)
            except Exception as e:
                print(f"Erro ao processar aba {sheet_name} em {file_name}: {e}")
                logging.error(f"Erro ao processar aba {sheet_name} em {file_name}: {e}")

# Combina todos os DataFrames
if all_dataframes:
    combined_df = pd.concat(all_dataframes, ignore_index=True)
    
    # Salva linhas com 'data' ou 'nome_do_aviario' nula/inválida em nulos_data.csv
    if nulos_dataframes:
        nulos_combined = pd.concat(nulos_dataframes, ignore_index=True)
        nulos_combined.to_csv(OUTPUT_NULOS_CSV, index=False)
        print(f"Linhas com data ou nome_do_aviario nula/inválida salvas em {OUTPUT_NULOS_CSV}")
        logging.info(f"Linhas com data ou nome_do_aviario nula/inválida salvas em {OUTPUT_NULOS_CSV}")
    
    # Salva como CSV
    combined_df.to_csv(OUTPUT_CSV, index=False, encoding='utf-8')
    print(f"Arquivo CSV salvo: {OUTPUT_CSV}")
    logging.info(f"Arquivo CSV salvo: {OUTPUT_CSV}")
    
    # Cria conexão com o banco SQLite
    conn = sqlite3.connect(OUTPUT_DB)
    cursor = conn.cursor()
    
    # Cria a tabela dados_sensores inicial sem 'nome_arquivo'
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS dados_sensores (
        data TEXT NOT NULL,
        tipo_de_evento TEXT,
        valor REAL,
        unidade TEXT,
        nome_do_aviario TEXT,
        nome_da_fazenda TEXT,
        nome_do_produtor TEXT,
        idade_do_lote INTEGER,
        numero_do_lote INTEGER,
        id_do_sensor TEXT,
        posicao_do_sensor TEXT
    )
    '''
    cursor.execute(create_table_query)
    
    # Insere os dados na tabela
    combined_df.to_sql('dados_sensores', conn, if_exists='append', index=False)
    
    # Aplica a transformação para manter apenas 'nome_do_aviario' com dígitos
    transform_table_query = '''
    -- Cria a tabela temporária com a estrutura desejada
    CREATE TABLE temp_dados (
        data TEXT NOT NULL,
        tipo_de_evento TEXT,
        valor REAL,
        unidade TEXT,
        nome_do_aviario TEXT,
        nome_da_fazenda TEXT,
        nome_do_produtor TEXT,
        idade_do_lote INTEGER,
        numero_do_lote INTEGER,
        id_do_sensor TEXT,
        posicao_do_sensor TEXT
    );

    -- Copia os dados com 'nome_do_aviario' já processado
    INSERT INTO temp_dados
    SELECT
        data,
        tipo_de_evento,
        valor,
        unidade,
        nome_do_aviario,
        nome_da_fazenda,
        nome_do_produtor,
        idade_do_lote,
        numero_do_lote,
        id_do_sensor,
        posicao_do_sensor
    FROM dados_sensores;

    -- Exclui a tabela original
    DROP TABLE dados_sensores;

    -- Renomeia a tabela temporária
    ALTER TABLE temp_dados RENAME TO dados_sensores;
    '''
    cursor.executescript(transform_table_query)
    
    # Confirma as alterações e fecha a conexão
    conn.commit()
    conn.close()
    
    print(f"Banco de dados SQLite criado: {OUTPUT_DB}")
    logging.info(f"Banco de dados SQLite criado: {OUTPUT_DB}")
else:
    print("Nenhum dado encontrado nas planilhas após filtragem.")
    logging.error("Nenhum dado encontrado nas planilhas após filtragem.")

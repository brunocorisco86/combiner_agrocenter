# Combiner Agrocenter

Este projeto é designado a combinar dados de sensores provenientes da Agrocenter e armazená-los em uma base de dados unificada.

## Propósito

O objetivo principal deste projeto é consolidar os dados de diversos sensores, provenientes de arquivos Excel da Agrocenter, em formatos padronizados e acessíveis (CSV e banco de dados SQLite). Isso facilita a análise e visualização das informações coletadas, permitindo um melhor entendimento das condições monitoradas e auxiliando na tomada de decisões.

## Funcionalidades

* Leitura de dados de múltiplos arquivos Excel (`.xlsx`) localizados na pasta `assets/dados_sensores/`.
* Processamento de dados em cada aba dos arquivos Excel.
* **Padronização de Nomes de Colunas:** Converte para minúsculas, remove espaços e acentos.
* **Limpeza da Coluna 'data':**
    * Espera o formato `dd/mm/aaaa HH:MM:SS`.
    * Identifica e remove linhas com datas nulas, vazias ou em formato inválido.
    * Registra informações sobre linhas com datas problemáticas em `outputs/processamento_nulos.log` e `outputs/nulos_data.csv`.
* **Limpeza da Coluna 'nome_do_aviario':**
    * Extrai apenas os dígitos do nome do aviário.
    * Registra informações sobre linhas onde 'nome_do_aviario' não contém dígitos.
* **Adição da Coluna 'tipo_de_evento':** Preenchida com o nome da aba do arquivo Excel de origem.
* **Saída de Dados:**
    * Salva os dados combinados e processados em `outputs/dados_combinados.csv`.
    * Salva as linhas com dados problemáticos (datas ou nomes de aviário inválidos) em `outputs/nulos_data.csv`.
    * Armazena os dados consolidados em um banco de dados SQLite em `database/dados_sensores.db`.
    * Registra o processo e erros em `outputs/processamento_nulos.log`.
* Criação automática das pastas `outputs` e `database` se não existirem.
* Geração de relatórios e visualizações (funcionalidade futura).

## Como Instalar e Executar

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/seu-usuario/combiner_agrocenter.git
   cd combiner_agrocenter
   ```

2. **Crie e ative um ambiente virtual (recomendado):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # No Windows use `venv\Scripts\activate`
   ```

3. **Instale as dependências:**
   O projeto utiliza a biblioteca `pandas` para manipulação de dados. Certifique-se de que ela esteja instalada. Se houver um arquivo `requirements.txt`, instale as dependências com:
   ```bash
   pip install -r requirements.txt
   ```
   Caso contrário, instale o `pandas` manualmente se necessário:
   ```bash
   pip install pandas
   ```
   O script também utiliza `sqlite3`, `os`, `glob`, `logging`, e `re`, que são parte da biblioteca padrão do Python.

4. **Prepare os dados dos sensores:**
   - Certifique-se de que a pasta `assets/dados_sensores/` exista na raiz do projeto. Crie-a se necessário.
   - Coloque os arquivos Excel (`.xlsx`) dos sensores nesta pasta. Cada arquivo pode conter múltiplas abas.
   - Veja a seção "Formato dos Dados de Entrada" para detalhes sobre as colunas esperadas.

5. **Execute o script principal:**
   O script principal para processar os dados é o `src/combine_sheets.py`. Para executá-lo:
   ```bash
   python src/combine_sheets.py
   ```
   O script criará automaticamente as pastas `outputs/` e `database/` na raiz do projeto para armazenar os arquivos de saída, caso elas não existam.

## Formato dos Dados de Entrada e Saída

### Dados de Entrada (Arquivos Excel `.xlsx`)

Os arquivos de entrada devem ser planilhas Excel (`.xlsx`) localizadas em `assets/dados_sensores/`. O script processará todas as abas de cada arquivo.

As colunas importantes que o script procura e processa especificamente são:

*   **`data`**: Essencial. Data e hora da leitura do sensor.
    *   **Formato esperado:** `dd/mm/aaaa HH:MM:SS` (ex: `25/10/2023 10:00:00`). Linhas com formatos diferentes, datas nulas ou vazias serão removidas e registradas nos arquivos de log/nulos.
*   **`nome_do_aviario`**: O script tentará extrair apenas os dígitos desta coluna. Linhas onde não for possível extrair dígitos serão removidas e registradas.
*   Outras colunas presentes nas abas (como `valor`, `unidade`, `nome_da_fazenda`, `nome_do_produtor`, `idade_do_lote`, `numero_do_lote`, `id_do_sensor`, `posicao_do_sensor`, etc.) serão incluídas nos dados combinados, mas sem processamento específico além da padronização do nome da coluna.

**Estrutura Geral Esperada (Exemplo de uma aba):**

| data                | nome_do_aviario | valor | unidade | id_do_sensor | ... |
| ------------------- | --------------- | ----- | ------- | ------------ | --- |
| 29/09/2023 08:00:00 | Aviario 01      | 25.5  | °C      | temp_sensor1 | ... |
| 29/09/2023 08:00:00 | Aviario 01      | 60.2  | %       | umid_sensor1 | ... |

**Importante:**
*   A primeira linha de cada aba é considerada o cabeçalho.
*   Os nomes das colunas serão padronizados (minúsculas, sem acentos, espaços substituídos por `_`).

### Dados de Saída

1.  **`outputs/dados_combinados.csv`**: Arquivo CSV contendo todos os dados processados e combinados de todas as abas de todos os arquivos Excel de entrada.
2.  **`outputs/nulos_data.csv`**: Arquivo CSV contendo as linhas que foram removidas durante o processamento devido a problemas com a coluna `data` (nula, vazia, formato incorreto) ou `nome_do_aviario` (sem dígitos). Inclui colunas adicionais `nome_arquivo` e `tipo_de_evento` para rastreamento.
3.  **`outputs/processamento_nulos.log`**: Arquivo de log detalhando o processamento, incluindo informações sobre arquivos lidos, abas processadas, e linhas com dados nulos/inválidos encontrados.
4.  **`database/dados_sensores.db`**: Banco de dados SQLite. Contém a tabela `dados_sensores` com os dados combinados.

**Schema da Tabela `dados_sensores` no SQLite:**

*   `data` (TEXT NOT NULL): Data e hora no formato `dd/mm/aaaa HH:MM:SS`.
*   `tipo_de_evento` (TEXT): Nome da aba do arquivo Excel de origem.
*   `valor` (REAL): Valor da leitura do sensor.
*   `unidade` (TEXT): Unidade de medida do valor.
*   `nome_do_aviario` (TEXT): Dígitos extraídos do nome do aviário.
*   `nome_da_fazenda` (TEXT): Nome da fazenda.
*   `nome_do_produtor` (TEXT): Nome do produtor.
*   `idade_do_lote` (INTEGER): Idade do lote.
*   `numero_do_lote` (INTEGER): Número do lote.
*   `id_do_sensor` (TEXT): Identificador do sensor.
*   `posicao_do_sensor` (TEXT): Posição do sensor.

*(As colunas de `valor` até `posicao_do_sensor` são exemplos; a tabela incluirá todas as colunas padronizadas encontradas nos arquivos de origem).*

## Como Contribuir

Contribuições são bem-vindas! Se você deseja contribuir para o projeto, siga estas etapas:

1. **Faça um fork do repositório.**
2. **Crie uma nova branch para sua feature ou correção:**
   ```bash
   git checkout -b minha-nova-feature
   ```
3. **Faça suas alterações e commit:**
   ```bash
   git commit -am 'Adiciona nova feature incrível'
   ```
4. **Envie para o seu fork:**
   ```bash
   git push origin minha-nova-feature
   ```
5. **Abra um Pull Request** detalhando suas alterações.

## Licença

Este projeto é licenciado sob a Licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

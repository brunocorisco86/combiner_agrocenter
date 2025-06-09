import sqlite3
import os

# Conectar ao banco SQLite
script_dir = os.path.dirname(__file__)  # Diretório do script (src)
db_file = os.path.join(script_dir, '..', 'database', 'dados_sensores.db')
conn = sqlite3.connect(db_file)
cursor = conn.cursor()

# Caminho relativo para o arquivo SQL
sql_file = os.path.join(script_dir, '..', 'scripts', 'create_views.sql')

# Verificar se o arquivo existe
if not os.path.exists(sql_file):
    print(f"Error: File {sql_file} not found. Ensure 'create_views.sql' is in the 'scripts' folder.")
    exit(1)

# Lista de views a serem criadas
views = [
        'vw_event_tipos', 'vw_daily_wtemp', 'vw_daily_atemp', 'vw_daily_btemp',
        'vw_daily_humidity', 'vw_daily_light', 'vw_daily_electricity', 'vw_daily_feed', 
        'vw_daily_water', 'vw_daily_wind', 'vw_age_segment_wtemp', 'vw_age_segment_atemp',
        'vw_age_segment_btemp', 'vw_age_segment_humidity', 'vw_age_segment_light',
        'vw_age_segment_electricity', 'vw_age_segment_feed', 'vw_age_segment_water',
        'vw_age_segment_wind', 'vw_report_atemp_by_days', 'vw_report_btemp_by_days',
        'vw_report_electricity_by_days', 'vw_report_feed_by_days', 'vw_report_humidity_by_days',
        'vw_report_light_by_days', 'vw_report_water_by_days', 'vw_report_wind_by_days',
        'vw_report_wtemp_by_days'
        ]

# Dropar views existentes
for view in views:
    cursor.execute(f"DROP VIEW IF EXISTS {view};")

# Ler e executar SQL com codificação UTF-8
try:
    with open(sql_file, 'r', encoding='utf-8') as file:
        sql_script = file.read()
    cursor.executescript(sql_script)
except sqlite3.OperationalError as e:
    print(f"SQL Error: {e}")
    print("SQL Script Content:")
    print(sql_script)
    exit(1)

# Commit e fechar
conn.commit()
conn.close()
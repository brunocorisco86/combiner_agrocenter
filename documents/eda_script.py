
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df_feed = pd.read_csv("database_feed.csv", encoding="utf-8", sep=";", on_bad_lines="skip", dtype=str)
df_sensors = pd.read_csv("dados_combinados.csv", encoding="utf-8", sep=",", on_bad_lines="skip", dtype=str)

# Data Cleaning and Type Conversion for df_feed
df_feed.drop(columns=["index"], inplace=True)
colunas_para_float = ["mortalidade", "mort_inicial", "caaj", "peso_medio", "idade", "fator.fb"]
for col in colunas_para_float:
    df_feed[col] = df_feed[col].str.replace(",", ".", regex=False).astype(float)
colunas_int = [
    "fb.pre_inicial", "fb.inicial_1", "fb.inicial_2", "fb.crescimento", "fb.abate", "fb.total",
    "fb.tot_ajustado",
    "gmd", "iep", "vazio",
    "classificacao"
]
for col in colunas_int:
    df_feed[col] = df_feed[col].astype(str).str.replace(",", ".", regex=False).astype(float).astype(int)
df_feed["fazenda"] = df_feed["fazenda"].astype(str)

# Data Cleaning and Type Conversion for df_sensors
df_sensors["data"] = pd.to_datetime(df_sensors["data"], format="%d/%m/%Y %H:%M:%S")
df_sensors["valor"] = pd.to_numeric(df_sensors["valor"], errors="coerce")

# EDA for df_sensors
print("\nUnique sensor types:")
print(df_sensors["tipo_de_evento"].unique())

print("\nValue counts for each sensor type:")
print(df_sensors.groupby("tipo_de_evento")["valor"].describe())

# Aggregate sensor data by aviario and date (daily average for simplicity)
df_sensors["data_dia"] = df_sensors["data"].dt.date
df_sensors_agg = df_sensors.groupby(["nome_do_aviario", "data_dia", "tipo_de_evento"])["valor"].mean().unstack(fill_value=0)
df_sensors_agg.reset_index(inplace=True)
df_sensors_agg.rename(columns={
    "nome_do_aviario": "fazenda",
    "data_dia": "data_sensor"
}, inplace=True)

# Convert 'fazenda' in df_feed to int for merging if it's numeric-like
# Assuming 'fazenda' in df_feed is actually numeric IDs, convert it to int for proper merging
df_feed["fazenda_int"] = pd.to_numeric(df_feed["fazenda"], errors='coerce').astype(pd.Int64Dtype())

# Merge df_feed with aggregated sensor data
# This merge is tricky as df_feed is aggregated per batch/farm, not daily.
# For now, let's try to merge based on 'fazenda' and assume a general relationship.
# A more accurate merge would require a common time/batch identifier in df_feed.

# Let's consider a simplified merge for initial EDA: average sensor values per aviario over all time
df_sensors_avg_per_aviario = df_sensors.groupby("nome_do_aviario")["valor"].mean().reset_index()
df_sensors_avg_per_aviario.rename(columns={
    "nome_do_aviario": "fazenda",
    "valor": "avg_sensor_value"
}, inplace=True)

# Merge df_feed with average sensor values per aviario
df_merged = pd.merge(df_feed, df_sensors_avg_per_aviario, on="fazenda", how="left")

print("\nMerged DataFrame head:")
print(df_merged.head())

# Further correlation analysis with sensor data (if merge is successful)
if "avg_sensor_value" in df_merged.columns:
    correlation_fator_fb_avg_sensor = df_merged["fator.fb"].corr(df_merged["avg_sensor_value"])
    print(f"\nCorrelação entre fator.fb e média de valor do sensor: {correlation_fator_fb_avg_sensor:.2f}")

# Visualizations
# Distribution of 'fator.fb' (already done in previous script, but keeping for completeness)
plt.figure(figsize=(8, 6))
sns.histplot(df_feed["fator.fb"], kde=True)
plt.title("Distribuição do Fator de Correção (fator.fb)")
plt.xlabel("Fator de Correção")
plt.ylabel("Frequência")
plt.savefig("fator_fb_distribution.png")
plt.close()

# Scatter plot of 'fator.fb' vs 'fb.total' (already done)
plt.figure(figsize=(10, 7))
sns.scatterplot(x="fb.total", y="fator.fb", data=df_feed)
plt.title("Fator de Correção vs. Consumo Total de Ração")
plt.xlabel("Consumo Total de Ração (fb.total)")
plt.ylabel("Fator de Correção (fator.fb)")
plt.savefig("fator_fb_vs_fb_total_scatter.png")
plt.close()

# Correlation matrix of numerical columns in df_feed (already done)
colunas_numericas = df_feed.select_dtypes(include=["int64", "float64"]).columns.tolist()
plt.figure(figsize=(12, 10))
sns.heatmap(df_feed[colunas_numericas].corr(), annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Matriz de Correlação - Dados de Ração")
plt.savefig("df_feed_correlation_heatmap.png")
plt.close()

# New visualization: Box plot of sensor values by sensor type
plt.figure(figsize=(12, 8))
sns.boxplot(x="tipo_de_evento", y="valor", data=df_sensors)
plt.title("Distribuição dos Valores dos Sensores por Tipo de Evento")
plt.xlabel("Tipo de Evento")
plt.ylabel("Valor do Sensor")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()
plt.savefig("sensor_value_distribution_by_type.png")
plt.close()

# New visualization: Time series plot of a specific sensor type for a few aviarios
# Select a few aviarios for demonstration
sample_aviarios = df_sensors["nome_do_aviario"].unique()[:10]

# Temperatura da Água
plt.figure(figsize=(15, 7))
for aviario in sample_aviarios:
    df_temp = df_sensors[(df_sensors["nome_do_aviario"] == aviario) & (df_sensors["tipo_de_evento"] == "Temperatura da Água")]
    if not df_temp.empty:
        df_temp = df_temp.set_index("data").resample("H")["valor"].mean().reset_index()
        sns.lineplot(x="data", y="valor", data=df_temp, label=f"Aviário {aviario}")

plt.title("Variação de Temperatura da Água ao Longo do Tempo em Aviários Selecionados")
plt.xlabel("Data")
plt.ylabel("Temperatura da Água (lux)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("temp_agua_time_series.png")
plt.close()

# Luminosidade
plt.figure(figsize=(15, 7))
for aviario in sample_aviarios:
    df_temp = df_sensors[(df_sensors["nome_do_aviario"] == aviario) & (df_sensors["tipo_de_evento"] == "Luminosidade")]
    if not df_temp.empty:
        df_temp = df_temp.set_index("data").resample("H")["valor"].mean().reset_index()
        sns.lineplot(x="data", y="valor", data=df_temp, label=f"Aviário {aviario}")

plt.title("Variação de Luminosidade ao Longo do Tempo em Aviários Selecionados")
plt.xlabel("Data")
plt.ylabel("Luminosidade (lux)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("luminosidade_time_series.png")
plt.close()

# Consumo de ração
plt.figure(figsize=(15, 7))
for aviario in sample_aviarios:
    df_temp = df_sensors[(df_sensors["nome_do_aviario"] == aviario) & (df_sensors["tipo_de_evento"] == "Consumo de ração")]
    if not df_temp.empty:
        df_temp = df_temp.set_index("data").resample("H")["valor"].mean().reset_index()
        sns.lineplot(x="data", y="valor", data=df_temp, label=f"Aviário {aviario}")

plt.title("Variação de Consumo de ração ao Longo do Tempo em Aviários Selecionados")
plt.xlabel("Data")
plt.ylabel("Consumo de ração")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("consumo_racao_time_series.png")
plt.close()

# Consumo de Eletricidade
plt.figure(figsize=(15, 7))
for aviario in sample_aviarios:
    df_temp = df_sensors[(df_sensors["nome_do_aviario"] == aviario) & (df_sensors["tipo_de_evento"] == "Consumo de Eletricidade")]
    if not df_temp.empty:
        df_temp = df_temp.set_index("data").resample("H")["valor"].mean().reset_index()
        sns.lineplot(x="data", y="valor", data=df_temp, label=f"Aviário {aviario}")

plt.title("Variação de Consumo de Eletricidade ao Longo do Tempo em Aviários Selecionados")
plt.xlabel("Data")
plt.ylabel("Consumo de Eletricidade")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("eletricidade_time_series.png")
plt.close()

# Temperatura Ambiente
plt.figure(figsize=(15, 7))
for aviario in sample_aviarios:
    df_temp = df_sensors[(df_sensors["nome_do_aviario"] == aviario) & (df_sensors["tipo_de_evento"] == "Temperatura Ambiente")]
    if not df_temp.empty:
        df_temp = df_temp.set_index("data").resample("H")["valor"].mean().reset_index()
        sns.lineplot(x="data", y="valor", data=df_temp, label=f"Aviário {aviario}")

plt.title("Variação de Temperatura Ambiente ao Longo do Tempo em Aviários Selecionados")
plt.xlabel("Data")
plt.ylabel("Temperatura Ambiente")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("temperatura_ambiente_time_series.png")
plt.close()

# Temperatura da Cama
plt.figure(figsize=(15, 7))
for aviario in sample_aviarios:
    df_temp = df_sensors[(df_sensors["nome_do_aviario"] == aviario) & (df_sensors["tipo_de_evento"] == "Temperatura da Cama")]
    if not df_temp.empty:
        df_temp = df_temp.set_index("data").resample("H")["valor"].mean().reset_index()
        sns.lineplot(x="data", y="valor", data=df_temp, label=f"Aviário {aviario}")

plt.title("Variação de Temperatura da Cama ao Longo do Tempo em Aviários Selecionados")
plt.xlabel("Data")
plt.ylabel("Temperatura da Cama")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("temperatura_cama_time_series.png")
plt.close()

# Umidade
plt.figure(figsize=(15, 7))
for aviario in sample_aviarios:
    df_temp = df_sensors[(df_sensors["nome_do_aviario"] == aviario) & (df_sensors["tipo_de_evento"] == "Umidade")]
    if not df_temp.empty:
        df_temp = df_temp.set_index("data").resample("H")["valor"].mean().reset_index()
        sns.lineplot(x="data", y="valor", data=df_temp, label=f"Aviário {aviario}")

plt.title("Variação de Umidade ao Longo do Tempo em Aviários Selecionados")
plt.xlabel("Data")
plt.ylabel("Umidade")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("umidade_time_series.png")
plt.close()

# Velocidade do Vento
plt.figure(figsize=(15, 7))
for aviario in sample_aviarios:
    df_temp = df_sensors[(df_sensors["nome_do_aviario"] == aviario) & (df_sensors["tipo_de_evento"] == "Velocidade do Vento")]
    if not df_temp.empty:
        df_temp = df_temp.set_index("data").resample("H")["valor"].mean().reset_index()
        sns.lineplot(x="data", y="valor", data=df_temp, label=f"Aviário {aviario}")

plt.title("Variação de Velocidade do Vento ao Longo do Tempo em Aviários Selecionados")
plt.xlabel("Data")
plt.ylabel("Velocidade do Vento")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("velocidade_vento_time_series.png")
plt.close()

print("\nEDA enriquecida concluída. Novos gráficos gerados.")
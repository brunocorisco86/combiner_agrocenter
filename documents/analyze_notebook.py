
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
df_feed = pd.read_csv("database_feed.csv", encoding="utf-8", sep=";", on_bad_lines="skip", dtype=str)
df_sensors = pd.read_csv("dados_combinados.csv", encoding="utf-8", sep=",", on_bad_lines="skip", dtype=str)

# Data Cleaning and Type Conversion for df_feed (from notebook)
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
# Convert 'data' column to datetime
df_sensors["data"] = pd.to_datetime(df_sensors["data"], format="%d/%m/%Y %H:%M:%S")
# Convert 'valor' to numeric, handling potential errors
df_sensors["valor"] = pd.to_numeric(df_sensors["valor"], errors="coerce")

# Display basic info and head of both dataframes
print("df_feed info:")
df_feed.info()
print("\ndf_feed head:")
print(df_feed.head())

print("\ndf_sensors info:")
df_sensors.info()
print("\ndf_sensors head:")
print(df_sensors.head())

# Define numerical and categorical columns for df_feed
colunas_numericas = df_feed.select_dtypes(include=['int64', 'float64']).columns.tolist()
colunas_categoricas = df_feed.select_dtypes(include=['object']).columns.tolist()

# Correlation analysis from notebook (simplified for execution)
# Let's try to replicate the correlation analysis mentioned in the notebook for 'fator.fb' and 'fb.total'
correlation_fator_fb_total = df_feed["fator.fb"].corr(df_feed["fb.total"])
print(f"\nCorrelação entre fator.fb e fb.total: {correlation_fator_fb_total:.2f}")

# Example: Distribution of 'fator.fb'
plt.figure(figsize=(8, 6))
sns.histplot(df_feed["fator.fb"], kde=True)
plt.title("Distribuição do Fator de Correção (fator.fb)")
plt.xlabel("Fator de Correção")
plt.ylabel("Frequência")
plt.savefig("fator_fb_distribution.png")
plt.close()

# Example: Scatter plot of 'fator.fb' vs 'fb.total'
plt.figure(figsize=(10, 7))
sns.scatterplot(x="fb.total", y="fator.fb", data=df_feed)
plt.title("Fator de Correção vs. Consumo Total de Ração")
plt.xlabel("Consumo Total de Ração (fb.total)")
plt.ylabel("Fator de Correção (fator.fb)")
plt.savefig("fator_fb_vs_fb_total_scatter.png")
plt.close()

# Correlation matrix of numerical columns in df_feed
plt.figure(figsize=(12, 10))
sns.heatmap(df_feed[colunas_numericas].corr(), annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Matriz de Correlação - Dados de Ração")
plt.savefig("df_feed_correlation_heatmap.png")
plt.close()

print("\nAnálise inicial concluída. Gerados gráficos de distribuição e scatter plot.")



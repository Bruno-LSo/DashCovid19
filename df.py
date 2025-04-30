import pandas as pd

# leitura dos arquivos
df_brasil = pd.read_csv("df_brasil.csv")
df_states = pd.read_csv("df_states.csv")

# df_brasil
print("=== df_brasil: primeiras 10 linhas ===")
print(df_brasil.head(10), "\n")
print("=== df_brasil: info ===")
df_brasil.info()
print("\n=== df_brasil: estatísticas descritivas ===")
print(df_brasil.describe(), "\n")

# df_states
print("=== df_states: primeiras 10 linhas ===")
print(df_states.head(10), "\n")
print("=== df_states: info ===")
df_states.info()
print("\n=== df_states: estatísticas descritivas ===")
print(df_states.describe())


negativos_brasil = df_brasil.query('casosNovos < 0')
negativos_states = df_states.query('casosNovos < 0')


print("=== df_brasil negativos ===")
print(negativos_brasil['casosNovos'], "\n")
print("=== df_states negativos ===")
print(negativos_states['casosNovos'], "\n")

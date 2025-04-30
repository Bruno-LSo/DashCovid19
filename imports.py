import pandas as pd
import numpy as np
from glob import glob

def load_covid_panel(path_pattern: str = "HIST_PAINEL_COVIDBR*.csv", sep: str = ";") -> pd.DataFrame:
    """
    Lê e concatena todos os CSVs cujo nome começa com HIST_PAINEL_COVIDBR.
    """
    files = sorted(glob(path_pattern))
    if not files:
        raise FileNotFoundError(f"Nenhum arquivo encontrado para o padrão: {path_pattern}")
    return pd.concat((pd.read_csv(f, sep=sep) for f in files), ignore_index=True)

def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    """
    - Converte 'estado' para uppercase (mantendo NaNs)
    - Transforma em absoluto as colunas de óbitos e casos
    """
    # Estado em maiúsculas (sem transformar NaNs em strings)
    df['estado'] = (
        df['estado']
        .where(df['estado'].notna())
        .astype(str)
        .str.upper()
        .replace({'nan': np.nan})
    )
    # Valor absoluto
    for col in ('obitosAcumulado', 'obitosNovos', 'casosNovos'):
        if col in df.columns:
            df[col] = df[col].abs()
    return df

def split_and_save(df: pd.DataFrame,
                   states_path: str = "df_states.csv",
                   brazil_path: str = "df_brasil.csv") -> None:
    """
    Separa em df_states e df_brazil, aplica preprocess, drop_duplicates e salva em CSV.
    """
    df_states = df[df['estado'].notna() & df['codmun'].isna()].copy()
    df_brazil = df[df['regiao'] == 'Brasil'].copy()

    df_states = preprocess(df_states).drop_duplicates()
    df_brazil = preprocess(df_brazil).drop_duplicates()

    df_states.to_csv(states_path, index=False)
    df_brazil.to_csv(brazil_path, index=False)
    print(f"Estados: {len(df_states)} linhas salvas em {states_path}")
    print(f"Brasil:   {len(df_brazil)} linhas salvas em {brazil_path}")

def main():
    df = load_covid_panel()
    split_and_save(df)

if __name__ == "__main__":
    main()

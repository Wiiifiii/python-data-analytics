# src/pda/task1.py
import pandas as pd

def load_data(path: str) -> pd.DataFrame:
    return pd.read_excel(path, engine="openpyxl")

def make_freq_table(series: pd.Series) -> pd.DataFrame:
    freq = series.value_counts(dropna=False).sort_index()
    rel = freq / freq.sum()
    return pd.DataFrame({"Count": freq, "Percent": rel * 100})

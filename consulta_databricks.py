import os
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
import openpyxl
import duckdb
import time
import pyarrow.parquet as pq
from datetime import datetime
from pathlib import Path





def is_cache_valid() -> bool:
    """Verifica se já existe parquet salvo hoje."""
    if not os.path.exists(CACHE_FILE) or not os.path.exists(CACHE_DATE_FILE):
        return False

    with open(CACHE_DATE_FILE, "r") as f:
        saved_date = f.read().strip()

    today = datetime.today().strftime("%Y-%m-%d")
    return saved_date == today




def save_cache(df: pd.DataFrame, df_budget: pd.DataFrame):
    """Salva o dataframe em parquet e atualiza a data de cache."""

    print("salvando dados em parquet na função save_cache")
    if df.empty:
        raise ValueError("⚠️ Nenhum dado retornado da tabela do banco de dados. Cache não será salvo.")
    df.to_parquet(CACHE_FILE, index=False)
    today = datetime.today().strftime("%Y-%m-%d")
    with open(CACHE_DATE_FILE, "w") as f:
        f.write(today)

    if df_budget.empty:
        raise ValueError("⚠️ Nenhum dado retornado da tabela do banco de dados. Cache não será salvo.")
    df_budget.to_parquet(CACHE_FILE_BUDGET, index=False)
    today = datetime.today().strftime("%Y-%m-%d")
    with open(CACHE_DATE_FILE, "w") as f:
        f.write(today)





# =======================
# 🔹 Query do databricks
# =======================

@st.cache_data(persist=True)
def query_sellout_data(sql: str) -> pd.DataFrame:
    if not Path(CACHE_FILE).exists() or os.path.getsize(CACHE_FILE) == 0:
        st.error("⚠️ Arquivo de cache inválido ou vazio. Recarregue os dados.")

    base_query = f"FROM read_parquet('{CACHE_FILE}')"

    if sql.strip().upper().startswith("SELECT"):
        query = sql
    else:
        query = f"SELECT * {base_query} {sql}"

    return duckdb.query(query).to_df()



@st.cache_data(persist=True)
def query_budget_data(sql: str) -> pd.DataFrame:
    """
    Executa queries SQL no arquivo parquet via DuckDB.
    """
    if not Path(CACHE_FILE_BUDGET).exists() or os.path.getsize(CACHE_FILE_BUDGET) == 0:
        st.error("⚠️ Arquivo de cache inválido ou vazio. Recarregue os dados.")


    base_query = f"FROM read_parquet('{CACHE_FILE_BUDGET}')"

    # Se começar com SELECT → assume query completa
    if sql.strip().upper().startswith("SELECT"):
        query = sql
    else:
        query = f"SELECT * {base_query} {sql}"

    return duckdb.query(query).to_df()



CACHE_FILE = "base_ficticia.parquet"
CACHE_DATE_FILE = "data_cache_date.txt"

CACHE_FILE_BUDGET = "base_ficticia_budget.parquet"

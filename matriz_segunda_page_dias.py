import os
import pandas as pd
import numpy as np
import openpyxl
import streamlit as st

# %%
# data = arquivo_lido()
def matriz_segunda_page_dias(data):

    # tratamento de dados
    # data['cod_loja'] = data['cod_loja'].astype(str)
    data = data.sort_values(by='dia', ascending=True)

    data['perc_desc_2024'] = data['perc_desc_2024'].astype(float)
    data['perc_desc_2025'] = data['perc_desc_2025'].astype(float)
    data['dia'] = data['dia'].astype(str)


    base_matriz_per_ano = data.rename(columns={"perc_desc_2024": "%_desc_2024",
                                "perc_desc_2025": "%_desc_2025"})

    base_matriz_per_ano["Delta_24"] = (base_matriz_per_ano['%_desc_2025'] - base_matriz_per_ano['%_desc_2024'])

    base_matriz_per_ano["%_desc_2024"] = base_matriz_per_ano["%_desc_2024"].abs()
    base_matriz_per_ano["%_desc_2025"] = base_matriz_per_ano["%_desc_2025"].abs()

    for coluna in list(base_matriz_per_ano.columns):
        if pd.api.types.is_numeric_dtype(base_matriz_per_ano[coluna]):
            base_matriz_per_ano[coluna] = base_matriz_per_ano[coluna].fillna(0)

    base_matriz_per_ano = base_matriz_per_ano.rename(columns={
        "dia": "Dia",
        "%_desc_2024": r"% Desc. 2024",
        "%_desc_2025": r"% Desc. 2025",
        "Delta_24": r"Δ p.p (25x24)" })

    base_matriz_per_ano = base_matriz_per_ano[["Dia", r'% Desc. 2025', r'% Desc. 2024', r"Δ p.p (25x24)"]]

    return base_matriz_per_ano


# base_matriz_per_ano = matriz_descontos_loja(data)

# display(matriz_desconto)
# %%

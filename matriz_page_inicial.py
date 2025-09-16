import os
import pandas as pd
import numpy as np
import openpyxl
import streamlit as st

# %%
# data = arquivo_lido()
def matriz_descontos_loja(data, budget):

    # tratamento de dados
    # data['cod_loja'] = data['cod_loja'].astype(str)
    data['perc_desc_2023'] = data['perc_desc_2023'].astype(float)
    data['perc_desc_2024'] = data['perc_desc_2024'].astype(float)
    data['perc_desc_2025'] = data['perc_desc_2025'].astype(float)
    budget['percentual_budget'] = budget['percentual_budget'].astype(float)

    data = pd.merge(data, budget, on="marca", how="left")

    data = data.rename(columns={"perc_desc_2023": "%_desc_2023",
                                "perc_desc_2024": "%_desc_2024",
                                "perc_desc_2025": "%_desc_2025",
                                "percentual_budget": "perc_budget"})


    base_matriz_per_ano = data.sort_values(by='%_desc_2025', ascending=True)
    base_matriz_per_ano["Delta_23"] = (base_matriz_per_ano['%_desc_2025'] - base_matriz_per_ano['%_desc_2023']) * -1
    # print(base_matriz_per_ano["Delta_23"])
    base_matriz_per_ano["Delta_24"] = (base_matriz_per_ano['%_desc_2025'] - base_matriz_per_ano['%_desc_2024']) * -1
    base_matriz_per_ano["Delta_Budget"] = (base_matriz_per_ano['%_desc_2025'] - base_matriz_per_ano['perc_budget']) * -1
    # print(base_matriz_per_ano["Delta_24"])

    # Laço de repetição para transformar colunas númericas em porcentagem.
    for coluna in base_matriz_per_ano.columns:
        if pd.api.types.is_numeric_dtype(base_matriz_per_ano[coluna]):
            base_matriz_per_ano[coluna] = (base_matriz_per_ano[coluna] * 100)
            # base_matriz_per_ano[coluna] = base_matriz_per_ano[coluna].apply(lambda x: f'{x:.1f}%')

    base_matriz_per_ano["%_desc_2023"] = base_matriz_per_ano["%_desc_2023"].abs()
    base_matriz_per_ano["%_desc_2024"] = base_matriz_per_ano["%_desc_2024"].abs()
    base_matriz_per_ano["%_desc_2025"] = base_matriz_per_ano["%_desc_2025"].abs()
    base_matriz_per_ano["perc_budget"] = base_matriz_per_ano["perc_budget"].abs()


    for coluna in list(base_matriz_per_ano.columns):
        if pd.api.types.is_numeric_dtype(base_matriz_per_ano[coluna]):
            base_matriz_per_ano[coluna] = base_matriz_per_ano[coluna].fillna(0)



    base_matriz_per_ano = base_matriz_per_ano.rename(columns={
        "marca": "Marca",
        "%_desc_2023": r"% Desc. 2023",
        "%_desc_2024": r"% Desc. 2024",
        "%_desc_2025": r"% Desc. 2025",
        "perc_budget": r"% Budget",
        "Delta_23": r"Δ p.p (25x23)",
        "Delta_24": r"Δ p.p (25x24)",
        "Delta_Budget": r"Δ p.p (25xBudget)"
    })


    base_matriz_per_ano = base_matriz_per_ano[["Marca", r'% Desc. 2025', r'% Budget', r"Δ p.p (25xBudget)", r'% Desc. 2024', r"Δ p.p (25x24)", r'% Desc. 2023', r"Δ p.p (25x23)"]]

    return base_matriz_per_ano


# base_matriz_per_ano = matriz_descontos_loja(data)

# display(matriz_desconto)
# %%

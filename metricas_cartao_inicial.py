import os
import pandas as pd
import numpy as np
import openpyxl
import streamlit as st


def cor_delta_card(valor1, valor2, reverso):
    if reverso:
        if valor1 > valor2:
            cores = "#60cd60"
            return cores
        else:
            cores = "#e93434"
            return cores
    else:
        if valor1 < valor2:
            cores = "#60cd60"
            return cores
        else:
            cores = "#e93434"
            return cores
    

def safe_div(a, b):
    return (a / b) -1 if b != 0 else 0



def get_val(df, col, default=0):
    if col in df and not df.empty:
        val = df[col].iloc[0]
        return default if pd.isna(val) else val
    return default




def format_brl(valor):
    return f"R$ {(valor / 1000):,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")


def metricas_cartoes_inicial(df_sellout, df_budget):
    
    receita_23 = get_val(df_sellout, 'receita_2023')
    receita_24 = get_val(df_sellout, 'receita_2024')
    receita_25 = get_val(df_sellout, 'receita_2025')
    print("receita 2025 metricas cartoes inicials:", receita_25)
    print(df_sellout['receita_2025'][0])
    desconto_23 = get_val(df_sellout, 'desconto_2023')
    desconto_24 = get_val(df_sellout, 'desconto_2024')
    desconto_25 = get_val(df_sellout, 'desconto_2025')
    # percentual_desconto_23 = get_val(df_sellout, 'perc_desc_2023')
    # percentual_desconto_24 = get_val(df_sellout, 'perc_desc_2024')
    # percentual_desconto_25 = get_val(df_sellout, 'perc_desc_2025')

    desconto_23 = get_val(df_sellout, 'desconto_2023')
    desconto_24 = get_val(df_sellout, 'desconto_2024')
    desconto_25 = get_val(df_sellout, 'desconto_2025')
    percentual_desconto_23 = get_val(df_sellout, 'perc_desc_2023')
    percentual_desconto_24 = get_val(df_sellout, 'perc_desc_2024')
    percentual_desconto_25 = get_val(df_sellout, 'perc_desc_2025')

    # BUDGET
    percentual_budget = get_val(df_budget, "percentual_budget")
    receita_budget = get_val(df_budget, "receita_budget")
    desconto_budget = get_val(df_budget, "desconto_budget") * -1
    print("desconto_budget", desconto_budget)
    print("desconto_2025", desconto_25)


    



    delta_percentual_desconto_24 = percentual_desconto_25 - percentual_desconto_24
    delta_percentual_desconto_23 = percentual_desconto_25 - percentual_desconto_23
    delta_percentual_budget = percentual_desconto_25 - percentual_budget
    print("delta_percentual_budget", delta_percentual_budget, type(delta_percentual_budget))
    delta_receita_24 = safe_div(receita_25, receita_24)
    delta_receita_23 = safe_div(receita_25, receita_23)
    delta_desconto_24 = safe_div(desconto_25, desconto_24)
    delta_desconto_23 = safe_div(desconto_25, desconto_23)
    delta_receita_budget = safe_div(receita_25, receita_budget)
    delta_desconto_budget = safe_div(desconto_25, desconto_budget)
    print("delta_receita_budget", delta_receita_budget, type(delta_receita_budget))
    print("delta_desconto_budget", delta_desconto_budget, type(delta_desconto_budget))

    return receita_23, receita_24, receita_budget, desconto_budget, percentual_budget, receita_25, desconto_23, desconto_24, desconto_25, percentual_desconto_23, percentual_desconto_24, percentual_desconto_25, delta_percentual_desconto_24, delta_percentual_desconto_23, delta_receita_24, delta_receita_23, delta_desconto_24, delta_desconto_23, delta_percentual_budget, delta_receita_budget, delta_desconto_budget

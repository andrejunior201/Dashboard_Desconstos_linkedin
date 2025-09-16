import os
import pandas as pd
import numpy as np
import openpyxl
import streamlit as st



def tabela_produtos_imagem(data):
    data['link_imagem_produtos'] = data['link_imagem_produtos'].astype(str) 
    data['SKU'] = data['SKU'].astype(str)
    data['nome_ajustado'] = data['nome_ajustado'].astype(str)
    data['Receita_liquida_total'] = data['Receita_liquida_total'].astype(float)
    data['PVL_total'] = data['PVL_total'].astype(float)
    data['Receita_liquida_unitario'] = data['Receita_liquida_unitario'].astype(float)
    data['PVL_unitaria'] = data['PVL_unitaria'].astype(float)
    data['Perc_Desconto'] = data['Perc_Desconto'].astype(float)
    data['Volume'] = data['Volume']


    for coluna in list(data.columns):
        if pd.api.types.is_numeric_dtype(data[coluna]):
            data[coluna] = data[coluna].fillna(0)


    
    return data
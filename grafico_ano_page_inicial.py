import os
import pandas as pd
import numpy as np
import openpyxl
import streamlit as st



def grafico_anual_primeira_page(data):
    data['receita_nf'] = data['receita_nf'].astype(float)
    data['receita_nf'] = data['receita_nf'].astype(float)
    data['desconto'] = data['desconto'].astype(float)
    data['pvl'] = data['pvl'].astype(float)
    data['desconto_novo'] = data['desconto_novo'].astype(float)


    data_agrupado_receita_desconto = data[['ano', 'receita_nf', 'pvl', 'desconto', 'desconto_novo']]


    return data_agrupado_receita_desconto

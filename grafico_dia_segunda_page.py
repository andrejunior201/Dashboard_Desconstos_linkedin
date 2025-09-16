import os
import pandas as pd
import numpy as np
import openpyxl
import streamlit as st



def grafico_dias_segunda_page(data):
    data['receita_nf'] = data['perc_desc_2024'].astype(float)
    data['receita_nf'] = data['perc_desc_2025'].astype(float)
    data['desconto'] = data['desconto'].astype(float)
    data['pvl'] = data['pvl'].astype(float)
    data['receita_2025'] = data['receita_2025'].astype(float)
    data['dia'] = data['dia'].astype(str)

    data_agrupado_receita_desconto = data[['dia', 'perc_desc_2024', 'perc_desc_2025', 'pvl', 'desconto']]
    

    return data_agrupado_receita_desconto

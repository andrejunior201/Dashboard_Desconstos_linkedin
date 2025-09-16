import os
import pandas as pd
import numpy as np
import openpyxl
import streamlit as st



def grafico_mensal_linhas(sellout, budget):

    # tratamento de dados
    sellout['mes'] = sellout['mes'].astype(str)
    sellout['perc_desc_2024'] = sellout['perc_desc_2024'].astype(float)
    sellout['perc_desc_2025'] = sellout['perc_desc_2025'].astype(float)

    budget['mes'] = budget['mes'].astype(str)
    budget['BUDGET'] = budget['BUDGET'].astype(float)


    data = pd.merge(sellout, budget, on="mes", how="left")

    
    data = data.rename(columns={"perc_desc_2024": "2024",
                                "mes": "Mês",
                                "perc_desc_2025": "2025"})
    return data




def tirar_dia_do_filtro(condicoes, filtro_dia):
    if "dia IN (" in condicoes:
        

        if ("WHERE " + filtro_dia) == condicoes:
            filtro_unico = "WHERE " + filtro_dia
            condicoes = condicoes.replace(filtro_unico, "")
            return condicoes
        
        # CASO TENHA MAIS FILTROS
        
        if (filtro_dia + " AND ") in condicoes:
            filtro_dia = filtro_dia + " AND "
            condicoes = condicoes.replace(filtro_dia, "")
            return condicoes
        
    
        if (" AND " + filtro_dia) in condicoes:
            filtro_dia = " AND " + filtro_dia
            condicoes = condicoes.replace(filtro_dia, "")
            return condicoes
    
    return condicoes
        


def tirar_meses_do_filtro(condicoes, filtro_meses):
    
    if "mes IN (" in condicoes:
        
        
        if ("WHERE " + filtro_meses) == condicoes:
            filtro_unico = "WHERE " + filtro_meses
            condicoes = condicoes.replace(filtro_unico, "")
            return condicoes
        
        # CASO TENHA MAIS FILTROS
        if (filtro_meses + " AND ") in condicoes:
            filtro_meses = filtro_meses + " AND "
            condicoes = condicoes.replace(filtro_meses, "")
            return condicoes
        
        if (" AND " + filtro_meses) in condicoes:
            filtro_meses = " AND " + filtro_meses
            condicoes = condicoes.replace(filtro_meses, "")
            return condicoes
    return condicoes
        



def tirar_ano_do_filtro(condicoes, filtro_ano):
    
    if "ano IN (" in condicoes:
        
        if ("WHERE " + filtro_ano) == condicoes:
            filtro_unico = "WHERE " + filtro_ano
            condicoes = condicoes.replace(filtro_unico, "")
            return condicoes
        
        # CASO TENHA MAIS FILTROS
        if (filtro_ano + " AND ") in condicoes:
            filtro_ano = filtro_ano + " AND "
            condicoes = condicoes.replace(filtro_ano, "")
            return condicoes
        
        if (" AND " + filtro_ano) in condicoes:
            filtro_ano = " AND " + filtro_ano
            condicoes = condicoes.replace(filtro_ano, "")
            return condicoes
    return condicoes





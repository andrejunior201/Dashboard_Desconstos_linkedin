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



# Funções
from matriz_page_inicial import matriz_descontos_loja
from grafico_ano_page_inicial import grafico_anual_primeira_page
from metricas_cartao_inicial import metricas_cartoes_inicial, format_brl, cor_delta_card
from grafico_meses_segunda_page import grafico_mensal_linhas, tirar_dia_do_filtro, tirar_meses_do_filtro, tirar_ano_do_filtro
from consulta_databricks import query_sellout_data, query_budget_data
from grafico_dia_segunda_page import grafico_dias_segunda_page
from matriz_segunda_page_loja import matriz_descontos_lojas
from matriz_segunda_page_dias import matriz_segunda_page_dias
from tabela_de_produtos_imagem import tabela_produtos_imagem



# print teste
print("\n Rodando \n ")
# =======================
# 🔹 Configuração da página
# =======================
st.set_page_config(
    layout="wide",
    page_title="Descontos",
    page_icon=":chart_with_upwards_trend:"
)

# Configurações para melhor performance
st.config.set_option('server.maxMessageSize', 200)
st.config.set_option('deprecation.showfileUploaderEncoding', False)





# =======================
# 🔹 Setando os nomes
# =======================
CACHE_FILE = "base_ficticia.parquet"
CACHE_DATE_FILE = "data_cache_date.txt"
CACHE_FILE_BUDGET = "base_ficticia_budget.parquet"




# =======================
# 🔹 Cabeçalho Personalizado
# =======================
st.markdown(f"""
<style>
    .header-container {{
        background: linear-gradient(135deg, #274566 0%, #539193 100%);
        padding: 15px;
        border-radius: 6px;
        margin-bottom: 15px;
        text-align: center;
    }}
    
    .header-title {{
        color: white;
        font-size: 24px;
        font-weight: 600;
        margin: 0;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }}
</style>

<div class="header-container">
    <h1 class="header-title">Painel de Descontos</h1>
</div>
""", unsafe_allow_html=True)



# ---------------------------
# 🔹 Botão no sidebar
# ---------------------------
st.markdown("""
<style>
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #539193; /* Fundo do sidebar */
        color: white;
    }
    
    /* Textos dentro do sidebar */
    [data-testid="stSidebar"] .stMarkdown, 
    [data-testid="stSidebar"] .stTextInput,
    [data-testid="stSidebar"] .stButton > button {
        color: black !important;
    }

    /* Botão de ocultar/mostrar sidebar */
    [data-testid="stSidebarCollapseButton"] {
        background-color: #539193 !important; /* cor do fundo */
        color: black !important; /* cor do ícone (seta) */
        border-radius: 8px !important; /* opcional: borda arredondada */
    }
    
    /* Hover no botão */
    [data-testid="stSidebarCollapseButton"]:hover {
        background-color: #407476 !important; /* cor quando passa o mouse */
    }
            
</style>
""", unsafe_allow_html=True)




st.sidebar.image("./imagem/LogoAZZAS_288X38_branco-01.png", width=500)


# st.sidebar.title("⚙️ Opções")
if st.sidebar.button("🔄 Atualizar dados agora"):
    print("atualizando os dados")
    st.cache_data.clear()
    st.cache_resource.clear()
    # update_cache_from_db() **** Aqui puxava os dados do BD
    st.rerun()
    st.success("✅ Cache atualizado com sucesso!")





with st.sidebar:

    st.header("Filtros 🔍")
    # =======================
    # 🔹 Filtros com DuckDB
    # =======================

    # ANO
    if Path("base_ficticia.parquet").exists():
        ano_options = query_sellout_data(
            "SELECT DISTINCT ano FROM read_parquet('base_ficticia.parquet')"
            ).sort_values("ano")["ano"].tolist()
    else:
        ano_options = []
    anos_selecionados = st.multiselect("Ano:", options=ano_options, placeholder="Selecione o ano", default=[])

    #MES
    if Path("base_ficticia.parquet").exists():
        mes_options = query_sellout_data(
            "SELECT DISTINCT mes FROM read_parquet('base_ficticia.parquet')"
            ).sort_values("mes")["mes"].tolist()
    else:
        mes_options = []
    meses_selecionados = st.multiselect("Mês:", options=mes_options, placeholder="Selecione o mês", default=[])

    #DIA
    if Path("base_ficticia.parquet").exists():
        dia_options = query_sellout_data(
            "SELECT DISTINCT dia FROM read_parquet('base_ficticia.parquet')"
            ).sort_values("dia")["dia"].tolist()
    else:
        dia_options = []
    dias_selecionados = st.multiselect("Dia:", options=dia_options, placeholder="Selecione o dia", default=[])

    #MARCA
    if Path("base_ficticia.parquet").exists():
        marcas_options = query_sellout_data(
            "SELECT DISTINCT marca FROM read_parquet('base_ficticia.parquet')"
        ).sort_values("marca")["marca"].tolist()
    else:
        marcas_options = []
    marcas_selecionadas = st.multiselect("Marcas:", options=marcas_options, placeholder="Selecione a marca", default=[])

    #CANAL
    if Path("base_ficticia.parquet").exists():
        canais_options = query_sellout_data(
            "SELECT DISTINCT canal FROM read_parquet('base_ficticia.parquet')"
            ).sort_values("canal")["canal"].tolist()
    else:
        canais_options = []
    canal_selecionado = st.multiselect("Canal:", options=canais_options, placeholder="Selecione um canal", default=[])

    #LOJA
    if Path("base_ficticia.parquet").exists():
        canais_options = query_sellout_data(
            "SELECT DISTINCT nome_ajustado FROM read_parquet('base_ficticia.parquet')"
            ).sort_values("nome_ajustado")["nome_ajustado"].tolist()
    else:
        canais_options = []
    loja_selecionado = st.multiselect("Loja:", options=canais_options, placeholder="Selecione a loja", default=[])


    #CLASSIFICAÇÃO
    if Path("base_ficticia.parquet").exists():
        canais_options = query_sellout_data(
            "SELECT DISTINCT Classificacao_apoio FROM read_parquet('base_ficticia.parquet')"
            ).sort_values("Classificacao_apoio")["Classificacao_apoio"].tolist()
    else:
        canais_options = []
    classificacao_selecionado = st.multiselect("Classificação:", options=canais_options, placeholder="Selecione a classificação", default=[])






# =======================
# 🔹 Montando SQL dinamicamente
# =======================
where_clauses = []
anos_retirar_do_filtro = ""
if anos_selecionados:
    ano_str = ",".join(str(a) for a in anos_selecionados)
    where_clauses.append(f"ano IN ({ano_str})")
    anos_retirar_do_filtro = f"ano IN ({ano_str})"


meses_retirar_do_filtro = ""
if meses_selecionados:
    meses_str = ",".join(str(m) for m in meses_selecionados)
    where_clauses.append(f"mes IN ({meses_str})")
    meses_retirar_do_filtro = f"mes IN ({meses_str})"


dias_retirar_do_filtro = ""
if dias_selecionados:
    dias_str = ",".join(str(d) for d in dias_selecionados)
    where_clauses.append(f"dia IN ({dias_str})")
    dias_retirar_do_filtro = f"dia IN ({dias_str})"


# Filtro de marcas
if marcas_selecionadas:
    marcas_str = ",".join([f"'{m}'" for m in marcas_selecionadas])
    where_clauses.append(f"marca IN ({marcas_str})")

# Filtro de canal
if canal_selecionado:
    canal_str = ",".join([f"'{c}'" for c in canal_selecionado])
    where_clauses.append(f"canal IN ({canal_str})")

# Filtro de Loja
if loja_selecionado:
    canal_str = ",".join([f"'{c}'" for c in loja_selecionado])
    where_clauses.append(f"nome_ajustado IN ({canal_str})")

# Filtro de Classificação
if classificacao_selecionado:
    canal_str = ",".join([f"'{c}'" for c in classificacao_selecionado])
    where_clauses.append(f"Classificacao_apoio IN ({canal_str})")

# Construindo WHERE final
where_sql = ""
if where_clauses:
    where_sql = "WHERE " + " AND ".join(where_clauses)

# st.write("DEBUG - WHERE SQL:", where_sql)




# =======================
# 🔹 Extrai informações dos filtros
# =======================
# Budget:
condicao_budget_cartao = tirar_dia_do_filtro(where_sql, dias_retirar_do_filtro)
condicao_budget_cartao = tirar_ano_do_filtro(condicao_budget_cartao, anos_retirar_do_filtro)

# Grafico mensal:
retirar_ano = tirar_ano_do_filtro(where_sql, anos_retirar_do_filtro)
retirar_mes = tirar_meses_do_filtro(retirar_ano, meses_retirar_do_filtro)
retirar_dia = tirar_dia_do_filtro(retirar_mes, dias_retirar_do_filtro)

retirar_ano_grafico_dias = tirar_ano_do_filtro(where_sql, anos_retirar_do_filtro)
retirar_dia_grafico_dias = tirar_dia_do_filtro(retirar_ano_grafico_dias, dias_retirar_do_filtro)



# =======================
# 🔹 Consultas final no DuckDB
# =======================
df_matriz_marca = query_sellout_data(f"""
                                   SELECT
                                        marca,
                                        SUM(CASE WHEN ano = 2023 THEN receita_nf END) / SUM(CASE WHEN ano = 2023 THEN pvl END) - 1 AS perc_desc_2023,
                                        SUM(CASE WHEN ano = 2024 THEN receita_nf END) / SUM(CASE WHEN ano = 2024 THEN pvl END) - 1 AS perc_desc_2024,
                                        SUM(CASE WHEN ano = 2025 THEN receita_nf END) / SUM(CASE WHEN ano = 2025 THEN pvl END) - 1 AS perc_desc_2025
                                    FROM read_parquet('{CACHE_FILE}') {where_sql}
                                    GROUP BY ALL""")

df_matriz_loja = query_sellout_data(f"""
                                   SELECT
                                        cod_loja,
                                        nome_ajustado,
                                        SUM(CASE WHEN ano = 2023 THEN receita_nf END) / SUM(CASE WHEN ano = 2023 THEN pvl END) - 1 AS perc_desc_2023,
                                        SUM(CASE WHEN ano = 2024 THEN receita_nf END) / SUM(CASE WHEN ano = 2024 THEN pvl END) - 1 AS perc_desc_2024,
                                        SUM(CASE WHEN ano = 2025 THEN receita_nf END) / SUM(CASE WHEN ano = 2025 THEN pvl END) - 1 AS perc_desc_2025
                                    FROM read_parquet('{CACHE_FILE}') {retirar_ano}
                                    GROUP BY ALL""")


matriz_descontos_por_dia = query_sellout_data(f""" 
                               SELECT 
                                    dia, 
                                    --sum(pvl) as pvl,
                                    --SUM(CASE WHEN ano = 2025 THEN pvl END) AS pvl_2025,
                                    --SUM(CASE WHEN ano = 2025 THEN receita_nf END) AS receita_2025,
                                    (SUM(CASE WHEN ano = 2024 THEN receita_nf END) / SUM(CASE WHEN ano = 2024 THEN pvl END) - 1) * -100 AS perc_desc_2024,
                                    (SUM(CASE WHEN ano = 2025 THEN receita_nf END) / SUM(CASE WHEN ano = 2025 THEN pvl END) - 1) * -100 AS perc_desc_2025
                                    --(SUM(receita_nf ) - SUM(pvl)) * -1 AS desconto
                               FROM read_parquet('{CACHE_FILE}') {retirar_ano} 
                               GROUP BY ALL""")



grafico_ano_first_page = query_sellout_data(f""" 
                               SELECT 
                                    ano, 
                                    sum(pvl) as pvl, 
                                    sum(receita_nf) as receita_nf, 
                                    (SUM(receita_nf ) - SUM(pvl)) * -1 AS desconto,
                                    (SUM(receita_nf) / SUM(pvl) - 1) * -1 AS desconto_novo
                               FROM read_parquet('{CACHE_FILE}') {where_sql} 
                               GROUP BY ALL""")

grafico_days_second_page = query_sellout_data(f""" 
                               SELECT 
                                    dia, 
                                    sum(pvl) as pvl,
                                    SUM(CASE WHEN ano = 2025 THEN pvl END) AS pvl_2025,
                                    SUM(CASE WHEN ano = 2025 THEN receita_nf END) AS receita_2025,
                                    (SUM(CASE WHEN ano = 2024 THEN receita_nf END) / SUM(CASE WHEN ano = 2024 THEN pvl END) - 1) * -100 AS perc_desc_2024,
                                    (SUM(CASE WHEN ano = 2025 THEN receita_nf END) / SUM(CASE WHEN ano = 2025 THEN pvl END) - 1) * -100 AS perc_desc_2025,
                                    (SUM(receita_nf ) - SUM(pvl)) * -1 AS desconto
                               FROM read_parquet('{CACHE_FILE}') {retirar_dia_grafico_dias} 
                               GROUP BY ALL""")

df_cartoes_indicadores = query_sellout_data(f"""
                                   SELECT
                                          
                                        SUM(CASE WHEN ano = 2023 THEN receita_nf END) AS receita_2023,
                                        SUM(CASE WHEN ano = 2024 THEN receita_nf END) AS receita_2024,
                                        SUM(CASE WHEN ano = 2025 THEN receita_nf END) AS receita_2025,
                                          
                                        SUM(CASE WHEN ano = 2023 THEN pvl END) AS pvl_2023,
                                        SUM(CASE WHEN ano = 2024 THEN pvl END) AS pvl_2024,
                                        SUM(CASE WHEN ano = 2025 THEN pvl END) AS pvl_2025,
                                          
                                        SUM(CASE WHEN ano = 2023 THEN receita_nf END) - SUM(CASE WHEN ano = 2023 THEN pvl END) AS desconto_2023,
                                        SUM(CASE WHEN ano = 2024 THEN receita_nf END) - SUM(CASE WHEN ano = 2024 THEN pvl END) AS desconto_2024,
                                        SUM(CASE WHEN ano = 2025 THEN receita_nf END) - SUM(CASE WHEN ano = 2025 THEN pvl END) AS desconto_2025,
                                        
                                        
                                    
                                        (SUM(CASE WHEN ano = 2023 THEN receita_nf END) / SUM(CASE WHEN ano = 2023 THEN pvl END) - 1) * -1 AS perc_desc_2023,
                                        (SUM(CASE WHEN ano = 2024 THEN receita_nf END) / SUM(CASE WHEN ano = 2024 THEN pvl END) - 1) * -1 AS perc_desc_2024,
                                        (SUM(CASE WHEN ano = 2025 THEN receita_nf END) / SUM(CASE WHEN ano = 2025 THEN pvl END) - 1) * -1 AS perc_desc_2025
                                    FROM read_parquet('{CACHE_FILE}') {where_sql}
                                    GROUP BY ALL""")



df_budget_cartao = query_budget_data(f"""
                                   SELECT
                                        SUM(receita_nf) AS receita_budget,
                                        SUM(pvl) AS pvl_2025,
                                        SUM(desconto) AS desconto_budget,
                                        (((SUM(receita_nf) / SUM(pvl)) - 1) * -1) AS percentual_budget
                                    FROM read_parquet('{CACHE_FILE_BUDGET}') {condicao_budget_cartao}
                                    GROUP BY ALL""")

df_matriz_budget_marca = query_budget_data(f"""
                                   SELECT
                                        marca,
                                        (((SUM(receita_nf) / SUM(pvl)) - 1)) AS percentual_budget
                                    FROM read_parquet('{CACHE_FILE_BUDGET}') {condicao_budget_cartao}
                                    GROUP BY ALL""")


df_matriz_budget_lojas = query_budget_data(f"""
                                   SELECT
                                        cod_loja,
                                        nome_ajustado,
                                        (((SUM(receita_nf) / SUM(pvl)) - 1)) AS percentual_budget
                                    FROM read_parquet('{CACHE_FILE_BUDGET}') {condicao_budget_cartao}
                                    GROUP BY ALL""")

consulta_grafico_meses_sellout = query_sellout_data(f"""
                                   SELECT
                                        mes,
                                        ((SUM(CASE WHEN ano = 2024 THEN receita_nf END) / SUM(CASE WHEN ano = 2024 THEN pvl END) - 1) * -1) * 100 AS perc_desc_2024,
                                        ((SUM(CASE WHEN ano = 2025 THEN receita_nf END) / SUM(CASE WHEN ano = 2025 THEN pvl END) - 1) * -1) * 100 AS perc_desc_2025
                                    FROM read_parquet('{CACHE_FILE}') {retirar_dia}
                                    GROUP BY ALL""")

consulta_grafico_meses_budget = query_budget_data(f"""
                                   SELECT
                                        mes,
                                        ((SUM(receita_nf) / SUM(pvl) - 1) * -1) * 100 AS BUDGET
                                    FROM read_parquet('{CACHE_FILE_BUDGET}') {retirar_dia}
                                    GROUP BY ALL""")




# =======================
# 🔹 Processar tabelas finais
# =======================
base_matriz_per_ano = matriz_descontos_loja(df_matriz_marca, df_matriz_budget_marca)
data_agrupado_receita_desconto = grafico_anual_primeira_page(grafico_ano_first_page)
receita_23, receita_24, receita_budget, desconto_budget, percentual_budget, receita_25, desconto_23, desconto_24, desconto_25, percentual_desconto_23, percentual_desconto_24, percentual_desconto_25, delta_percentual_desconto_24, delta_percentual_desconto_23, delta_receita_24, delta_receita_23, delta_desconto_24, delta_desconto_23, delta_percentual_budget, delta_receita_budget, delta_desconto_budget = metricas_cartoes_inicial(df_cartoes_indicadores, df_budget_cartao)
base_grafico_mensal_linhas = grafico_mensal_linhas(consulta_grafico_meses_sellout, consulta_grafico_meses_budget)
base_grafico_dias_segunda_page = grafico_dias_segunda_page(grafico_days_second_page)
base_matriz_loja_segunda_page = matriz_descontos_lojas(df_matriz_loja, df_matriz_budget_lojas)
base_matriz_dia_segunda_page = matriz_segunda_page_dias(matriz_descontos_por_dia)

print("TABELA DE MARCAS INICIAL:")
print(base_matriz_loja_segunda_page)
print("TABELA DE MARCA INICIAL:")
print(base_matriz_loja_segunda_page.info())
print(base_matriz_loja_segunda_page.columns)

# =======================
# 🔹 INICIO FRONT
# =======================

st.markdown("""
<style>
    /* Deixar as abas maiores e mais visíveis */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #274566;
        border-radius: 8px 8px 0px 0px;
        gap: 8px;
        padding: 10px 20px;
        font-weight: 600;
        font-size: 16px;
        color: white;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #539193;
        color: white;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #3a5a7a;
        color: white;
    }
    
    /* Container das abas mais destacado */
    .stTabs {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        margin-bottom: 20px;
        border: 1px solid #dde1e6;
    }
    
    /* Conteúdo dentro das abas */
    .stTabs [data-baseweb="tab-panel"] {
        padding: 20px;
        background-color: white;
        border-radius: 0px 0px 8px 8px;
        border: 1px solid #dde1e6;
        border-top: none;
    }
</style>
""", unsafe_allow_html=True)

# ABAS
aba1, aba2, aba3 = st.tabs(["📊 Visão Geral", "🏪 Abertura por loja", "👟 Análise de produtos"])



# ============== aba1 ===============
with aba1:
    
    # CSS para reduzir espaçamento
    st.markdown("""
        <style>
        .stPlotlyChart {
            margin: 0px !important;
            padding: 0px !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # Seu título
    st.markdown(
        """
        <div style="
            background-color:#000000;
            color:white;
            text-align:center;
            padding:10px;
            border-radius:8px;
            font-size:26px;
            font-weight:bold;
            margin-bottom: 10px;">
            DESCONTO ANUAL
        </div>
        """,
        unsafe_allow_html=True
    )

        # =============== GRÁFICO BARRA + LINHA ================
    col1, col2 = st.columns(2)

    with col1:

        fig1 = go.Figure()
        # Linhas
        fig1.add_trace(go.Scatter(x=base_grafico_mensal_linhas["Mês"], y=base_grafico_mensal_linhas["2025"], mode="lines+markers+text",
                                name="2025", line=dict(color="navy", width=3),
                                text=[f"{v:.1f}%" for v in base_grafico_mensal_linhas["2025"]],
                                textposition="top center",
                                textfont=dict(color="black", size=12, family="Arial")))

        fig1.add_trace(go.Scatter(x=base_grafico_mensal_linhas["Mês"], y=base_grafico_mensal_linhas["2024"], mode="lines+markers+text",
                                name="2024", line=dict(color="gray", width=3),
                                text=[f"{v:.1f}%" for v in base_grafico_mensal_linhas["2024"]],
                                textposition="bottom center",
                                textfont=dict(color="black", size=12, family="Arial")))

        #Quando inputar o Budget pra dentro do Databricks.
        fig1.add_trace(go.Scatter(x=base_grafico_mensal_linhas["Mês"], y=base_grafico_mensal_linhas["BUDGET"], mode="lines+markers+text",
                                name="Budget", line=dict(color="lightblue", width=2, dash="dash"),
                                text=[f"{v:.1f}%" for v in base_grafico_mensal_linhas["BUDGET"]],
                                textposition="top center",
                                textfont=dict(color="black", size=12, family="Arial")))



        # Gráfico com altura e margens ajustadas
        fig1.update_layout(
            height=380,
            margin=dict(l=0, r=10, t=40, b=40),
            xaxis_title="Mês",
            yaxis_title="%",
            template="simple_white",
            legend=dict(orientation="v", y=1, x=0.9)
        )



        st.plotly_chart(fig1, use_container_width=True)



    with col2:

        fig2 = go.Figure()
    # Barras - Receita
        data_agrupado_receita_desconto["ano"] = data_agrupado_receita_desconto["ano"].astype(str)

        # Barras - Receita
        fig2.add_trace(go.Bar(
            x=data_agrupado_receita_desconto["ano"],
            y=data_agrupado_receita_desconto["receita_nf"],
            name="Receita",
            marker_color="#B7A696" 
        ))

        # Barras - Desconto
        fig2.add_trace(go.Bar(
            x=data_agrupado_receita_desconto["ano"],
            y=data_agrupado_receita_desconto["desconto"],
            name="Desconto",
            marker_color="#274566"
        ))

        # Linha - Percentual
        fig2.add_trace(go.Scatter(
            x=data_agrupado_receita_desconto["ano"],
            y=data_agrupado_receita_desconto["desconto_novo"],
            name="Percentual",
            yaxis="y2",
            mode="lines+markers+text",
            text=[f"{p:.1%}" for p in data_agrupado_receita_desconto["desconto_novo"]],
            textposition="top center",
            textfont=dict(color="black", size=12, family="Arial"),
            line=dict(color="rgba(160, 198, 237, 0.9)", width=4, shape="spline"),  # spline = curva suave
            marker=dict(size=10, symbol="diamond", color="rgba(0, 200, 83, 1)", line=dict(width=1, color="white"))
        ))

        

        # Layout com dois eixos Y
        fig2.update_layout(
            xaxis=dict(
                title="Ano",
                type="category",  # força eixo categórico
                categoryorder="category ascending",  # ordena
                tickfont=dict(color="black", size=12)
            ),
            yaxis=dict(
                title=dict(text="Valores (R$)", font=dict(color="black", size=14)),
                tickfont=dict(color="black", size=12),
                showgrid=False
            ),
            yaxis2=dict(
                title=dict(text="Percentual", font=dict(color="black", size=14)),
                tickfont=dict(color="black", size=12),
                overlaying="y",
                side="right",
                position=0.95,
                tickformat=".1%",
                showgrid=True,
                title_standoff=30,
                automargin=True
            ),
            height=380,
            margin=dict(l=0, r=10, t=30, b=40),
            barmode="group",
            bargap=0.3
        )


            # Protando o gráfico
        st.plotly_chart(fig2, use_container_width=True)



    # Cartões
    col1, col2, col3= st.columns(3)
    with col1:
        st.markdown(
        f"""
            <div style="
                background-color: #274566;
                padding: 10px;
                border-radius: 15px;
                box-shadow: 2px 2px 10px rgba(0,0,0,0.3);
                margin-bottom: 10px;
            ">
                <h3 style="color:white; margin-bottom:0px;">2025</h2>
                <p style="color:#f4f5f4; font-size:26px; margin:0;">📉 % Desconto: {percentual_desconto_25:.1%}</p>
                <p style="color:#f4f5f4; font-size:18px; margin:0;">Δ Desconto (25 x Budget): <n style="color:{cor_delta_card(percentual_desconto_25, percentual_budget, False)}; font-size:18px; margin:0;"> {delta_percentual_budget:.1%}</p>
                <p style="border:1px solid #bbb; margin:4;">
                <p style="color: #bbb; font-size:20px; margin:2px 0;">💵 Receita: {format_brl(receita_25)} Δ Budget: <n style="color: {cor_delta_card(receita_25, receita_budget, True)}; font-size:20px; margin:2px 0;">{delta_receita_budget:.1%}</p>
                <p style="color: #bbb; font-size:20px; margin:2px 0;">🏷️ Desconto: {format_brl(desconto_25)} Δ Budget: <n style="color: {cor_delta_card(desconto_25, desconto_budget, True)}; font-size:20px; margin:2px 0;">{delta_desconto_budget:.1%}</p>

            </div>
        """,
        unsafe_allow_html=True)

    with col2:
        st.markdown(
        f"""
            <div style="
                background-color: #274566;
                padding: 10px;
                border-radius: 15px;
                box-shadow: 2px 2px 10px rgba(0,0,0,0.3);
                margin-bottom: 10px;
            ">
                <h3 style="color:white; margin-bottom:0px;">2024</h2>
                <p style="color:#f4f5f4; font-size:26px; margin:0;">📉 % Desconto: {percentual_desconto_24:.1%}</p>
                <p style="color:#f4f5f4; font-size:18px; margin:0;">Δ Desconto (25 x 24): <n style="color:{cor_delta_card(percentual_desconto_25, percentual_desconto_24, False)}; font-size:18px; margin:0;"> {delta_percentual_desconto_24:.1%}</p>
                <p style="border:1px solid #bbb; margin:4;">
                <p style="color: #bbb; font-size:20px; margin:2px 0;">💵 Receita: {format_brl(receita_24)} Δ 25: <n style="color: {cor_delta_card(receita_25, receita_24, True)}; font-size:20px; margin:2px 0;">{delta_receita_24:.1%}</p>
                <p style="color: #bbb; font-size:20px; margin:2px 0;">🏷️ Desconto: {format_brl(desconto_24)} Δ 25: <n style="color: {cor_delta_card(desconto_25, desconto_24, True)}; font-size:20px; margin:2px 0;">{delta_desconto_24:.1%}</p>
            </div>
        """,
        unsafe_allow_html=True)

    with col3:
        st.markdown(
        f"""
            <div style="
                background-color: #274566;
                padding: 10px;
                border-radius: 15px;
                box-shadow: 2px 2px 10px rgba(0,0,0,0.3);
                margin-bottom: 10px;
            ">
                <h3 style="color:white; margin-bottom:0px;">2023</h2>
                <p style="color:#f4f5f4; font-size:26px; margin:0;">📉 % Desconto: {percentual_desconto_23:.1%}</p>
                <p style="color:#f4f5f4; font-size:18px; margin:0;">Δ Desconto (25 x 23): <n style="color:{cor_delta_card(percentual_desconto_25, percentual_desconto_23, False)}; font-size:18px; margin:0;"> {delta_percentual_desconto_23:.1%}</p>
                <p style="border:1px solid #bbb; margin:4;">
                <p style="color: #bbb; font-size:20px; margin:2px 0;">💵 Receita: {format_brl(receita_23)} Δ 25: <n style="color: {cor_delta_card(receita_25, receita_23, True)}; font-size:20px; margin:2px 0;">{delta_receita_23:.1%}</p>
                <p style="color: #bbb; font-size:20px; margin:2px 0;">🏷️ Desconto: {format_brl(desconto_23)} Δ 25: <n style="color: {cor_delta_card(desconto_25, desconto_23, True)}; font-size:20px; margin:2px 0;">{delta_desconto_23:.1%}</p>
            </div>
        """,
        unsafe_allow_html=True)








    # =========== TABELA DE DELTAS =================

    # tabela plotada
    st.subheader("Desconto por marcas:")
    # Puxando a função que transforma a tabela para nosso visual desejado.


    @st.cache_data(ttl=60)
    def color_delta(val):
        if pd.isna(val):  # Trata valores nulos
            return ""

        if abs(val) > 1 :  # Só aplica cor se o valor for maior que 1 p.p. em módulo
            color = "green" if val < 0 else "red" 
            return f"color: {color}; font-weight: bold"

        return ""  # Caso não atenda à condição, não aplica estilo
        

    def format_percent(val):
        return f"{val:.1f}%"

    def format_delta(val):
        return f"{val:.1f}"

    

    # aplica o estilo usando os novos nomes
    styled_df = (
        base_matriz_per_ano.style
        .applymap(color_delta, subset=["Δ p.p (25x23)", "Δ p.p (25x24)", "Δ p.p (25xBudget)"])
        .format({
            "% Desc. 2025": lambda x: f"{x:.1f}%" if pd.notnull(x) else "",
            "% Desc. 2024": lambda x: f"{x:.1f}%" if pd.notnull(x) else "",
            "% Desc. 2023": lambda x: f"{x:.1f}%" if pd.notnull(x) else "",
            "% Budget": lambda x: f"{x:.1f}%" if pd.notnull(x) else "",
            "Δ p.p (25x23)": lambda x: f"{x:.1f}" if pd.notnull(x) else "",
            "Δ p.p (25x24)": lambda x: f"{x:.1f}" if pd.notnull(x) else "",
            "Δ p.p (25xBudget)": lambda x: f"{x:.1f}" if pd.notnull(x) else "",
        }, na_rep=""
        )
    )

    st.dataframe(styled_df, use_container_width=True, hide_index=True, height=350)




# ============== aba2 ===============
with aba2:

    # =========== GRAFICO DE LINHAS POR DIA =================
    # Seu título
    st.markdown(
        """
        <div style="
            background-color:#000000;
            color:white;
            text-align:center;
            padding:10px;
            border-radius:8px;
            font-size:26px;
            font-weight:bold;
            margin-bottom: 10px;">
            DESCONTO DIA
        </div>
        """,
        unsafe_allow_html=True
    )

    fig = go.Figure()
    # Linhas
    fig.add_trace(go.Scatter(x=base_grafico_dias_segunda_page["dia"], y=base_grafico_dias_segunda_page["perc_desc_2025"], mode="lines+markers+text",
                            name="2025", line=dict(color="navy", width=3),
                            text=[f"{v:.1f}%" for v in base_grafico_dias_segunda_page["perc_desc_2025"]],
                            textposition="top center",
                            textfont=dict(color="black", size=12, family="Arial")))

    fig.add_trace(go.Scatter(x=base_grafico_dias_segunda_page["dia"], y=base_grafico_dias_segunda_page["perc_desc_2024"], mode="lines+markers+text",
                            name="2024", line=dict(color="gray", width=3),
                            text=[f"{v:.1f}%" for v in base_grafico_dias_segunda_page["perc_desc_2024"]],
                            textposition="bottom center",
                            textfont=dict(color="black", size=12, family="Arial")))


    # Gráfico com altura e margens ajustadas
    fig.update_layout(
        # title="Descontos dia",
        height=380,
        margin=dict(l=0, r=10, t=40, b=40),
        xaxis_title="Dias",
        yaxis_title="%",
        template="simple_white",
        legend=dict(orientation="v", y=1.2, x=0)
    )

    st.plotly_chart(fig, use_container_width=True)




    # =========== TABELA DE DELTAS LOJAS =================
 

    # Puxando a função que transforma a tabela para nosso visual desejado.
    def color_delta(val):
        if pd.isna(val):  # Trata valores nulos
            return ""

        if abs(val) > 1 :  # Só aplica cor se o valor for maior que 1 p.p. em módulo
            color = "green" if val < 0 else "red" 
            return f"color: {color}; font-weight: bold"

        return ""  # Caso não atenda à condição, não aplica estilo
        

    def format_percent(val):
        return f"{val:.1f}%"

    def format_delta(val):
        return f"{val:.1f}"

    st.subheader("Desconto por loja:")

    # aplica o estilo usando os novos nomes
    styled_df = (
        base_matriz_loja_segunda_page.style
        .applymap(color_delta, subset=["Δ p.p (25x23)", "Δ p.p (25x24)", "Δ p.p (25xBudget)"])
        .format({
            "% Desc. 2025": lambda x: f"{x:.1f}%" if pd.notnull(x) else "",
            "% Desc. 2024": lambda x: f"{x:.1f}%" if pd.notnull(x) else "",
            "% Desc. 2023": lambda x: f"{x:.1f}%" if pd.notnull(x) else "",
            "% Budget": lambda x: f"{x:.1f}%" if pd.notnull(x) else "",
            "Δ p.p (25x23)": lambda x: f"{x:.1f}" if pd.notnull(x) else "",
            "Δ p.p (25x24)": lambda x: f"{x:.1f}" if pd.notnull(x) else "",
            "Δ p.p (25xBudget)": lambda x: f"{x:.1f}" if pd.notnull(x) else ""
        }, na_rep=""
        )
    )

    st.dataframe(styled_df, use_container_width=True, hide_index=True, height=350)


        # =========== TABELA DE DELTAS DIAS =================
    col1, col2, col3= st.columns(3)

    with col1:
        # Puxando a função que transforma a tabela para nosso visual desejado.
        def color_delta(val):
            if pd.isna(val):  # Trata valores nulos
                return ""

            if abs(val) > 1 :  # Só aplica cor se o valor for maior que 1 p.p. em módulo
                color = "green" if val < 0 else "red" 
                return f"color: {color}; font-weight: bold"

            return ""  # Caso não atenda à condição, não aplica estilo
            

        def format_percent(val):
            return f"{val:.1f}%"

        def format_delta(val):
            return f"{val:.1f}"

        st.subheader("Desconto por dia:")

        # aplica o estilo usando os novos nomes
        styled_df = (
            base_matriz_dia_segunda_page.style
            .applymap(color_delta, subset=["Δ p.p (25x24)"])
            .format({
                r"% Desc. 2025": lambda x: f"{x:.1f}%" if pd.notnull(x) else "",
                r"% Desc. 2024": lambda x: f"{x:.1f}%" if pd.notnull(x) else "",
                r"Δ p.p (25x24)": lambda x: f"{x:.1f}" if pd.notnull(x) else ""
            }, na_rep=""
            )
        )

        st.dataframe(styled_df, use_container_width=True, hide_index=True, height=500)






with aba3:


    st.subheader("Filtros da tabela produtos:")

    # filtros produto:
    FIG_ANO, FIG_MES, FIG_DIA, FIG_MARCA, FIG_CANAL, FIG_LOJA, FIG_CLASSIFICAAO, FIG_DS_ESTACAO, FIG_DS_COLECAO, FIG_DS_TEMA = st.columns(10)

    with FIG_ANO:

        if Path("base_ficticia.parquet").exists():
            ano_options = query_sellout_data(
                "SELECT DISTINCT ano FROM read_parquet('base_ficticia.parquet')"
                ).sort_values("ano")["ano"].tolist()
        else:
            ano_options = []
        anos_tabela_imagem = st.multiselect("Ano:", options=ano_options, placeholder="Selecione o ano", default=[], key="Ano_produto")


    with FIG_MES:
        #MES
        if Path("base_ficticia.parquet").exists():
            mes_options = query_sellout_data(
                "SELECT DISTINCT mes FROM read_parquet('base_ficticia.parquet')"
                ).sort_values("mes")["mes"].tolist()
        else:
            mes_options = []
        meses_tabela_imagem = st.multiselect("Mês:", options=mes_options, placeholder="Selecione o mês", default=[], key="mes_produto")



    with FIG_DIA:
        #DIA
        if Path("base_ficticia.parquet").exists():
            dia_options = query_sellout_data(
                "SELECT DISTINCT dia FROM read_parquet('base_ficticia.parquet')"
                ).sort_values("dia")["dia"].tolist()
        else:
            dia_options = []
        dias_tabela_imagem = st.multiselect("Dia:", options=dia_options, placeholder="Selecione o dia", default=[], key="Dia_produto")


    with FIG_MARCA:
        #MARCA
        if Path("base_ficticia.parquet").exists():
            marcas_options = query_sellout_data(
                "SELECT DISTINCT marca FROM read_parquet('base_ficticia.parquet')"
            ).sort_values("marca")["marca"].tolist()
        else:
            marcas_options = []
        marcas_tabela_imagem = st.multiselect("Marcas:", options=marcas_options, placeholder="Selecione a marca", default=[], key="Marca_produto")

    with FIG_CANAL:
        #CANAL
        if Path("base_ficticia.parquet").exists():
            canais_options = query_sellout_data(
                "SELECT DISTINCT canal FROM read_parquet('base_ficticia.parquet')"
                ).sort_values("canal")["canal"].tolist()
        else:
            canais_options = []
        canal_tabela_imagem = st.multiselect("Canal:", options=canais_options, placeholder="Selecione um canal", default=[], key="Canal_produto")

    with FIG_LOJA:
        #LOJA
        if Path("base_ficticia.parquet").exists():
            canais_options = query_sellout_data(
                "SELECT DISTINCT nome_ajustado FROM read_parquet('base_ficticia.parquet')"
                ).sort_values("nome_ajustado")["nome_ajustado"].tolist()
        else:
            canais_options = []
        loja_tabela_imagem = st.multiselect("Loja:", options=canais_options, placeholder="Selecione a loja", default=[], key="Loja_produto")

    with FIG_CLASSIFICAAO:
        #CLASSIFICAÇÃO
        if Path("base_ficticia.parquet").exists():
            canais_options = query_sellout_data(
                "SELECT DISTINCT Classificacao_apoio FROM read_parquet('base_ficticia.parquet')"
                ).sort_values("Classificacao_apoio")["Classificacao_apoio"].tolist()
        else:
            canais_options = []
        classificacao_tabela_imagem = st.multiselect("Classificação:", options=canais_options, placeholder="Selecione a classificação", default=[], key="Classi_produto")


    with FIG_DS_ESTACAO:
        #DESCRIÇÃO ESTAÇÃO
        if Path("base_ficticia.parquet").exists():
            canais_options = query_sellout_data(
                "SELECT DISTINCT DS_ESTACAO FROM read_parquet('base_ficticia.parquet')"
                ).sort_values("DS_ESTACAO")["DS_ESTACAO"].tolist()
        else:
            canais_options = []
        estacao_tabela_imagem = st.multiselect("Desc. Estação:", options=canais_options, placeholder="Selecione a classificação", default=[], key="Classi_estacao")


    with FIG_DS_COLECAO:
        #DESCRIÇÃO COLEÇÃO
        if Path("base_ficticia.parquet").exists():
            canais_options = query_sellout_data(
                "SELECT DISTINCT DS_COLECAO FROM read_parquet('base_ficticia.parquet')"
                ).sort_values("DS_COLECAO")["DS_COLECAO"].tolist()
        else:
            canais_options = []
        colecao_tabela_imagem = st.multiselect("Desc. Coleção:", options=canais_options, placeholder="Selecione a classificação", default=[], key="Classi_colecao")



    with FIG_DS_TEMA:
        #DESCRIÇÃO COLEÇÃO
        if Path("base_ficticia.parquet").exists():
            canais_options = query_sellout_data(
                "SELECT DISTINCT DS_TEMA FROM read_parquet('base_ficticia.parquet')"
                ).sort_values("DS_TEMA")["DS_TEMA"].tolist()
        else:
            canais_options = []
        tema_tabela_imagem = st.multiselect("Desc. Tema:", options=canais_options, placeholder="Selecione a classificação", default=[], key="Classi_tema")



    # =======================
    # 🔹 Montando SQL dinamicamente
    # =======================
     # Filtro de Ano
    where_clauses_produtos = []
    anos_retirar_do_filtro = ""
    if anos_tabela_imagem:
        ano_str = ",".join(str(a) for a in anos_tabela_imagem)
        where_clauses_produtos.append(f"ano IN ({ano_str})")
        anos_retirar_do_filtro = f"ano IN ({ano_str})"

     # Filtro de Mes
    meses_retirar_do_filtro = ""
    if meses_tabela_imagem:
        meses_str = ",".join(str(m) for m in meses_tabela_imagem)
        where_clauses_produtos.append(f"mes IN ({meses_str})")
        meses_retirar_do_filtro = f"mes IN ({meses_str})"

     # Filtro de Dia
    dias_retirar_do_filtro = ""
    if dias_tabela_imagem:
        dias_str = ",".join(str(d) for d in dias_tabela_imagem)
        where_clauses_produtos.append(f"dia IN ({dias_str})")
        dias_retirar_do_filtro = f"dia IN ({dias_str})"


    # Filtro de marcas
    if marcas_tabela_imagem:
        marcas_str = ",".join([f"'{m}'" for m in marcas_tabela_imagem])
        where_clauses_produtos.append(f"marca IN ({marcas_str})")

    # Filtro de canal
    if canal_tabela_imagem:
        canal_str = ",".join([f"'{c}'" for c in canal_tabela_imagem])
        where_clauses_produtos.append(f"canal IN ({canal_str})")

    # Filtro de Loja
    if loja_tabela_imagem:
        canal_str = ",".join([f"'{c}'" for c in loja_tabela_imagem])
        where_clauses_produtos.append(f"nome_ajustado IN ({canal_str})")

    # Filtro de Classificação
    if classificacao_tabela_imagem:
        canal_str = ",".join([f"'{c}'" for c in classificacao_tabela_imagem])
        where_clauses_produtos.append(f"Classificacao_apoio IN ({canal_str})")

   # Filtro de estação
    if estacao_tabela_imagem:
        canal_str = ",".join([f"'{c}'" for c in estacao_tabela_imagem])
        where_clauses_produtos.append(f"DS_ESTACAO IN ({canal_str})")


    # Filtro de coleção
    if colecao_tabela_imagem:
        canal_str = ",".join([f"'{c}'" for c in colecao_tabela_imagem])
        where_clauses_produtos.append(f"DS_COLECAO IN ({canal_str})")

   # Filtro de tema
    if tema_tabela_imagem:
        canal_str = ",".join([f"'{c}'" for c in tema_tabela_imagem])
        where_clauses_produtos.append(f"DS_TEMA IN ({canal_str})")


    # Construindo WHERE final
    where_sql_produto = ""
    if where_clauses_produtos:
        where_sql_produto = "WHERE " + " AND ".join(where_clauses_produtos)


    base_produtos_imagem = query_sellout_data(f"""
                                    SELECT
                                            link_imagem_produtos,
                                            SKU,
                                            nome_ajustado,
                                            SUM(receita_nf) as Receita_liquida_total,
                                            SUM(pvl) as PVL_total,
                                            SUM(receita_nf) / NULLIF(SUM(volume), 0) as Receita_liquida_unitario,
                                            SUM(pvl) / NULLIF(SUM(volume),0) as PVL_unitaria,
                                            (((SUM(receita_nf) / NULLIF(SUM(pvl), 0)) - 1) * -1) * 100 AS Perc_Desconto,
                                            SUM(volume) as Volume,
                                            CASE
                                                WHEN ((((SUM(receita_nf) / NULLIF(SUM(pvl), 0)) - 1) * -1) * 100) > 95 THEN 'BRINDE'
                                                WHEN ((((SUM(receita_nf) / NULLIF(SUM(pvl), 0)) - 1) * -1) * 100) > 10 THEN 'MARKDOWN'
                                                ELSE 'FULL PRICE'
                                            END AS Cluster
                                        FROM read_parquet('{CACHE_FILE}') {where_sql_produto} 
                                        GROUP BY ALL""")


    df_page = tabela_produtos_imagem(base_produtos_imagem)

    def formato_real(value):
        return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    



    filtro_1, filtro_2, filtro_3, filtro_4, filtro_5 = st.columns(5)



    with filtro_1:
        filtro_cluster = st.selectbox("Cluster:", ["Todos Selecionados", "BRINDE", "MARKDOWN", "FULL PRICE"], index=0)
        if filtro_cluster != "Todos Selecionados":
            df_page = df_page[df_page["Cluster"] == filtro_cluster]




    with filtro_2:
        opcoes_filtro = ["Receita Liquida Total", "PVL Total", "Receita Liquida Unit.", "PVL Unit.", "% Desconto", "Volume"]
        filtro_colunas = st.selectbox("Coluna ordenação:",opcoes_filtro, index=4)
    

        if filtro_colunas == "Receita Liquida Total":
            filtro_colunas = "Receita_liquida_total"
        if filtro_colunas == "PVL Total":
            filtro_colunas = "PVL_total"
        if filtro_colunas == "Receita Liquida Unit.":
            filtro_colunas = "Receita_liquida_unitario"
        if filtro_colunas == "PVL Unit.":
            filtro_colunas = "PVL_unitaria"
        if filtro_colunas == "% Desconto":
            filtro_colunas = "Perc_Desconto"

    with filtro_3:
        filtro_cresc_desc = st.selectbox("Tipo de ordenação:", ["Decrescente", "Crescente"], index=0)
        if filtro_cresc_desc == "Decrescente":
            tipo_ordem = False
        else:
            tipo_ordem = True

    df_page = df_page.sort_values(by=filtro_colunas, ascending=tipo_ordem)


    with filtro_4:
    # Definir tamanho da página
        page_size = st.selectbox("Itens por página", [10, 50, 100, 500], index=1)

    with filtro_5:
        # Calcular número de páginas
        total_pages = (len(df_page) - 1) // page_size + 1
        
        if total_pages == 0:
            total_pages = 1
        page = st.number_input("Página", min_value=1, max_value=total_pages, value=1)

        # Fatiar o dataframe
        start = (page - 1) * page_size
        end = start + page_size
        df_page = df_page.iloc[start:end]



    st.markdown(
        """
        <div style="
            background-color:#000000;
            color:white;
            text-align:center;
            padding:10px;
            border-radius:8px;
            font-size:26px;
            font-weight:bold;
            margin-bottom: 10px;">
            Tabela Produto
        </div>
        """,
        unsafe_allow_html=True
    )



    df_page['Receita_liquida_total'] = df_page['Receita_liquida_total'].apply(formato_real)
    df_page['PVL_total'] = df_page['PVL_total'].apply(formato_real)
    df_page['Receita_liquida_unitario'] = df_page['Receita_liquida_unitario'].apply(formato_real)
    df_page['PVL_unitaria'] = df_page['PVL_unitaria'].apply(formato_real)


    # Mostrar tabela com imagens
    st.data_editor(
        df_page,
        column_config={
            "link_imagem_produtos": st.column_config.ImageColumn("Foto", help="Imagem do produto", width="small"),
            "SKU": st.column_config.TextColumn("SKU"),
            "nome_ajustado": st.column_config.TextColumn("Loja"),
            "Receita_liquida_total": st.column_config.TextColumn("Receita Liquida Total"),
            "PVL_total": st.column_config.TextColumn("PVL Total"),
            "Receita_liquida_unitario": st.column_config.TextColumn("Receita Liquida Unit."),
            "PVL_unitaria": st.column_config.TextColumn("PVL Unit."),
            "Perc_Desconto": st.column_config.NumberColumn("% Desconto", format="%.1f%%"),
            "Volume": st.column_config.NumberColumn("Volume"),
        },
        hide_index=True,
        use_container_width=True,
        height=500,
    )








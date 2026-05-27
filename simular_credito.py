import streamlit as st
import pandas as pd
import numpy as np
import json
from joblib import load
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler

# ------------------------------------------------------------
# Definição da classe Transformador (idêntica à do treino)
# ------------------------------------------------------------
class Transformador(BaseEstimator, TransformerMixin):
    def __init__(self, colunas_quantitativas, colunas_categoricas):
        self.colunas_quantitativas = colunas_quantitativas
        self.colunas_categoricas = colunas_categoricas
        self.enc = OneHotEncoder()
        self.scaler = MinMaxScaler()

    def fit(self, X, y=None):
        self.enc.fit(X[self.colunas_categoricas])
        self.scaler.fit(X[self.colunas_quantitativas])
        return self

    def transform(self, X, y=None):
        X_categoricas = pd.DataFrame(
            data=self.enc.transform(X[self.colunas_categoricas]).toarray(),
            columns=self.enc.get_feature_names_out(self.colunas_categoricas)
        )
        X_quantitativas = pd.DataFrame(
            data=self.scaler.transform(X[self.colunas_quantitativas]),
            columns=self.colunas_quantitativas
        )
        return pd.concat([X_quantitativas, X_categoricas], axis=1)

# ------------------------------------------------------------
# Função de avaliação de crédito
# ------------------------------------------------------------
def avaliar_mau(dict_respostas):
    try:
        modelo = load('obj/modelo.joblib')
        features = load('obj/features.joblib')
    except FileNotFoundError as e:
        st.error(f"Erro ao carregar os arquivos necessários: {e}")
        return None

    df = pd.DataFrame([dict_respostas])
    df = df[features]
    prob = modelo.predict_proba(df)[0, 1]
    classe = "Mau pagador" if prob >= 0.5 else "Bom pagador"
    return prob, classe

# ------------------------------------------------------------
# Configuração da página
# ------------------------------------------------------------
st.set_page_config(page_title="Simulador de Crédito", page_icon="💳", layout="wide")
st.markdown("""
    <style>
    .stButton button {
        background-color: #0A6EBD;
        color: white;
        border-radius: 10px;
        padding: 12px 28px;
        font-size: 20px;
        font-weight: bold;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: all 0.3s ease;
    }
    .stButton button:hover {
        background-color: #085A9E;
        box-shadow: 0 6px 12px rgba(0,0,0,0.2);
    }
    .big-text {
        font-size: 24px;
        font-weight: 600;
    }
    </style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# Cabeçalho
# ------------------------------------------------------------
st.title("💳 Simulador de Concessão de Crédito")
st.markdown("""
    <div style="border-left: 4px solid #0A6EBD; padding-left: 16px; margin-bottom: 30px;">
        <p style="font-size: 18px; color: #555; margin: 0;">
            Preencha os dados do cliente e obtenha uma avaliação de risco de inadimplência baseada em Machine Learning.
        </p>
    </div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------
# Carregar listas de opções (JSON)
# ------------------------------------------------------------
try:
    with open('obj/lista_campos.json', 'r', encoding='utf-8') as f:
        lista_campos = json.load(f)
except FileNotFoundError:
    st.error("Arquivo 'lista_campos.json' não encontrado. Verifique se o arquivo está na pasta 'obj'.")
    st.stop()

# ------------------------------------------------------------
# Mapeamento de valores padrão (seus dados)
# ------------------------------------------------------------
default_categoria_renda = "Working"
default_grau_escolaridade = "Academic degree"
default_estado_civil = "Single / not married"
default_moradia = "House / apartment"
default_ocupacao = "Managers"

# Função auxiliar para obter índice seguro
def get_index(lista, valor):
    try:
        return lista.index(valor)
    except ValueError:
        return 0

# ------------------------------------------------------------
# Formulário organizado em seções (design aplicado)
# ------------------------------------------------------------
st.subheader("📋 Dados Pessoais")
col1, col2 = st.columns(2)

with col1:
    idade = st.number_input("Idade", min_value=18, max_value=100, value=27)
    estado_civil = st.selectbox("Estado civil",
                                lista_campos['Estado_Civil'],
                                index=get_index(lista_campos['Estado_Civil'], default_estado_civil))
    qtd_filhos = st.number_input("Quantos filhos possui?", min_value=0, max_value=10, value=0)
    tamanho_familia = st.number_input("Tamanho da família", min_value=1, max_value=10, value=5)

with col2:
    grau_escolaridade = st.selectbox("Grau de escolaridade",
                                     lista_campos['Grau_Escolaridade'],
                                     index=get_index(lista_campos['Grau_Escolaridade'], default_grau_escolaridade))
    moradia = st.selectbox("Tipo de moradia",
                           lista_campos['Moradia'],
                           index=get_index(lista_campos['Moradia'], default_moradia))
    tem_carro = st.selectbox("Possui carro?", ("Sim", "Não"), index=1)   # 1 = "Não"
    tem_casa_propria = st.selectbox("Possui casa própria?", ("Sim", "Não"), index=0) # 0 = "Sim"

st.subheader("💼 Dados Profissionais")
col3, col4 = st.columns(2)

with col3:
    categoria_renda = st.selectbox("Categoria de renda",
                                   lista_campos['Categoria_de_renda'],
                                   index=get_index(lista_campos['Categoria_de_renda'], default_categoria_renda))
    rendimento_anual = st.number_input("Rendimento anual (R$)",
                                       min_value=0.0, value=50400.0, step=1000.0,
                                       help="Renda mensal de R$4.200,00 equivale a R$50.400,00 anuais")
    anos_empregado = st.number_input("Anos de emprego", min_value=0, max_value=50, value=1)

with col4:
    ocupacao = st.selectbox("Ocupação",
                            lista_campos['Ocupacao'],
                            index=get_index(lista_campos['Ocupacao'], default_ocupacao))
    tem_telefone_trabalho = st.selectbox("Possui telefone do trabalho?", ("Sim", "Não"), index=1)
    tem_telefone_fixo = st.selectbox("Possui telefone fixo?", ("Sim", "Não"), index=1)
    tem_email = st.selectbox("Possui e-mail?", ("Sim", "Não"), index=0)

# ------------------------------------------------------------
# Botão de ação (Lei de Fitts: grande e centralizado)
# ------------------------------------------------------------
st.markdown("<br>", unsafe_allow_html=True)
col_btn, _, _ = st.columns([2, 1, 1])  # coluna centralizada
with col_btn:
    avaliar = st.button("🔍 Avaliar risco de crédito", use_container_width=True)

# ------------------------------------------------------------
# Processamento e resultado
# ------------------------------------------------------------
if avaliar:
    respostas = {
        'Tem_Carro': 1 if tem_carro == "Sim" else 0,
        'Tem_Casa_Propria': 1 if tem_casa_propria == "Sim" else 0,
        'Categoria_de_renda': categoria_renda,
        'Grau_Escolaridade': grau_escolaridade,
        'Estado_Civil': estado_civil,
        'Moradia': moradia,
        'Tem_telefone_trabalho': 1 if tem_telefone_trabalho == "Sim" else 0,
        'Tem_telefone_fixo': 1 if tem_telefone_fixo == "Sim" else 0,
        'Tem_email': 1 if tem_email == "Sim" else 0,
        'Ocupacao': ocupacao,
        'Idade': idade,
        'Qtd_Filhos': qtd_filhos,
        'Rendimento_Anual': rendimento_anual,
        'Anos_empregado': anos_empregado,
        'Tamanho_Familia': tamanho_familia
    }

    resultado = avaliar_mau(respostas)

    if resultado is None:
        st.error("Erro durante a avaliação. Verifique se os arquivos do modelo estão presentes.")
    else:
        prob, classe = resultado
        # Container de resultado com destaque (contraste e alinhamento)
        with st.container():
            st.markdown("---")
            st.subheader("📊 Resultado da Análise")
            col_res, _ = st.columns([3, 1])

            with col_res:
                if classe == "Mau pagador":
                    st.error(f"**Probabilidade de inadimplência:** {prob:.2%}")
                    st.markdown("### ❌ Classificação: **Mau pagador – Crédito NEGADO**")
                else:
                    st.success(f"**Probabilidade de inadimplência:** {prob:.2%}")
                    st.markdown("### ✅ Classificação: **Bom pagador – Crédito APROVADO**")

                st.caption("ℹ️ Modelo de aprendizado. Decisões reais devem considerar políticas de negócio e análise humana.")

# ------------------------------------------------------------
# Rodapé
# ------------------------------------------------------------
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #888; font-size: 14px;'>"
    "REPAGINANDO UM PROJETO DE 2022"
    "</p>",
    unsafe_allow_html=True
)
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
st.set_page_config(page_title="Simulador de Crédito", page_icon="💳")
st.title("💳 Simulador de Concessão de Crédito")
st.markdown("Preencha os dados do cliente para avaliação de risco de inadimplência.")

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
# Formulário de entrada (idêntico ao anterior)
# ------------------------------------------------------------
st.header("Dados do cliente")
col1, col2 = st.columns(2)

with col1:
    tem_carro = st.selectbox("Possui carro?", ("Sim", "Não"))
    tem_casa_propria = st.selectbox("Possui casa própria?", ("Sim", "Não"))
    categoria_renda = st.selectbox("Categoria de renda", lista_campos['Categoria_de_renda'])
    grau_escolaridade = st.selectbox("Grau de escolaridade", lista_campos['Grau_Escolaridade'])
    estado_civil = st.selectbox("Estado civil", lista_campos['Estado_Civil'])
    moradia = st.selectbox("Tipo de moradia", lista_campos['Moradia'])

with col2:
    tem_telefone_trabalho = st.selectbox("Possui telefone do trabalho?", ("Sim", "Não"))
    tem_telefone_fixo = st.selectbox("Possui telefone fixo?", ("Sim", "Não"))
    tem_email = st.selectbox("Possui e-mail?", ("Sim", "Não"))
    ocupacao = st.selectbox("Ocupação", lista_campos['Ocupacao'])
    idade = st.number_input("Idade", min_value=18, max_value=100, value=30)
    qtd_filhos = st.number_input("Quantos filhos possui?", min_value=0, max_value=10, value=0)
    rendimento_anual = st.number_input("Rendimento anual (R$)", min_value=0.0, value=50000.0, step=1000.0)
    anos_empregado = st.number_input("Anos de emprego", min_value=0, max_value=50, value=5)
    tamanho_familia = st.number_input("Tamanho da família", min_value=1, max_value=10, value=2)

if st.button("Avaliar risco de crédito"):
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
        st.subheader("Resultado da análise:")
        st.write(f"Probabilidade de inadimplência: **{prob:.2%}**")
        if classe == "Mau pagador":
            st.error(f"Classificação: {classe} - **Crédito NEGADO**")
        else:
            st.success(f"Classificação: {classe} - **Crédito APROVADO**")
        st.caption("Este é um modelo de aprendizado. As decisões reais devem considerar políticas de negócio e análise humana.")
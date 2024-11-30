import streamlit as st
from joblib import load
import pandas as pd
from utils import Transformador
from imblearn.over_sampling import SMOTE

def avaliar_mau(dict_respostas):
    # Carregando modelo e features
    try:
        modelo = load('obj/modelo.joblib')
        features = load('obj/features.joblib')
    except FileNotFoundError as e:
        st.error(f"Erro ao carregar os arquivos necessários: {e}")
        return None

    # Ajustando valores de emprego/desemprego
    if dict_respostas.get('Anos_desempregado', 0) > 0:
        dict_respostas['Anos_empregado'] = -dict_respostas['Anos_desempregado']
    
    # Verificação de consistência
    if not all(col in dict_respostas for col in features):
        st.error("Nem todas as respostas foram preenchidas corretamente.")
        return None

    # Criando DataFrame com as respostas do cliente
    respostas = [dict_respostas[col] for col in features]
    df_novo_cliente = pd.DataFrame(data=[respostas], columns=features)

    # Predizendo o resultado
    try:
        mau = modelo.predict(df_novo_cliente)[0]
    except Exception as e:
        st.error(f"Erro ao realizar a predição: {e}")
        return None

    return mau


st.image('img/bytebank_logo.png')
st.write('# Precisando de crédito amigão?')


try:
    lista_campos = load('obj/lista_campos.joblib')
except FileNotFoundError:
    st.error("Erro: lista_campos.joblib não encontrada.")
    st.stop()

dict_respostas = {}

with st.expander('Trabalho'):
    col1, col2 = st.columns(2)
    dict_respostas['Ocupacao'] = col1.selectbox('Qual sua Ocupação ?', lista_campos['Ocupacao'])
    dict_respostas['Categoria_de_renda'] = col1.selectbox('Qual categoria de renda ?', lista_campos['Categoria_de_renda'])
    dict_respostas['Rendimento_Anual'] = col1.slider('Qual o salário mensal?', min_value=0, max_value=35000, step=500) * 12
    dict_respostas['Tem_telefone_trabalho'] = 1 if col2.selectbox('Tem um telefone do trabalho?', ['Sim', 'Não']) == 'Sim' else 0
    dict_respostas['Anos_empregado'] = col2.slider('Quantos anos empregado?', min_value=0.0, max_value=60.0, step=0.5)
    dict_respostas['Anos_desempregado'] = col2.slider('Quantos anos desempregado?', min_value=0.0, max_value=60.0, step=0.5)

with st.expander('Pessoal'):
    col3, col4 = st.columns(2)
    dict_respostas['Grau_Escolaridade'] = col3.selectbox(
        'Qual seu grau de escolaridade?', lista_campos['Grau_Escolaridade']
    )
    dict_respostas['Idade'] = col4.slider(
        'Qual sua idade?', min_value=1, max_value=100, step=1
    )
    dict_respostas['Tem_Carro'] = 1 if col3.selectbox(
        'Você possui um carro?', ['Sim', 'Não']
    ) == 'Sim' else 0
    dict_respostas['Tem_telefone_fixo'] = 1 if col4.selectbox(
        'Você possui telefone fixo?', ['Sim', 'Não']
    ) == 'Sim' else 0
    dict_respostas['Tem_email'] = 1 if col3.selectbox(
        'Você possui um e-mail?', ['Sim', 'Não']
    ) == 'Sim' else 0
    dict_respostas['Estado_Civil'] = col4.selectbox(
        'Qual seu estado civil?', lista_campos['Estado_Civil']
    )


with st.expander('Família'):
    col5, col6 = st.columns(2)
    dict_respostas['Moradia'] = col5.selectbox(
        'Qual o tipo de moradia?', lista_campos['Moradia']
    )
    dict_respostas['Tamanho_Familia'] = col6.slider(
        'Quantas pessoas estão na sua família?', min_value=0, max_value=10, step=1
    )
    dict_respostas['Tem_Casa_Propria'] = 1 if col5.selectbox(
        'Você possui casa própria?', ['Sim', 'Não']
    ) == 'Sim' else 0
    dict_respostas['Qtd_Filhos'] = col6.slider(
        'Quantos filhos você possui?', min_value=0, max_value=10, step=1
    )



with st.expander('Pessoal'):
    col3, col4 = st.columns(2)
    dict_respostas['Grau_Escolaridade'] = col3.selectbox(
        'Qual seu grau de escolaridade?', lista_campos['Grau_Escolaridade']
    )
    dict_respostas['Idade'] = col4.slider(
        'Qual sua idade?', min_value=1, max_value=100, step=1
    )
    dict_respostas['Tem_Carro'] = 1 if col3.selectbox(
        'Você possui um carro?', ['Sim', 'Não']
    ) == 'Sim' else 0
    dict_respostas['Tem_telefone_fixo'] = 1 if col4.selectbox(
        'Você possui telefone fixo?', ['Sim', 'Não']
    ) == 'Sim' else 0
    dict_respostas['Tem_email'] = 1 if col3.selectbox(
        'Você possui um e-mail?', ['Sim', 'Não']
    ) == 'Sim' else 0
    dict_respostas['Estado_Civil'] = col4.selectbox(
        'Qual seu estado civil?', lista_campos['Estado_Civil']
    )

# Expansor 'Família'
with st.expander('Família'):
    col5, col6 = st.columns(2)
    dict_respostas['Moradia'] = col5.selectbox(
        'Qual o tipo de moradia?', lista_campos['Moradia']
    )
    dict_respostas['Tamanho_Familia'] = col6.slider(
        'Quantas pessoas estão na sua família?', min_value=0, max_value=10, step=1
    )
    dict_respostas['Tem_Casa_Propria'] = 1 if col5.selectbox(
        'Você possui casa própria?', ['Sim', 'Não']
    ) == 'Sim' else 0
    dict_respostas['Qtd_Filhos'] = col6.slider(
        'Quantos filhos você possui?', min_value=0, max_value=10, step=1
    )



if st.button('Avaliar crédito'):
    resultado = avaliar_mau(dict_respostas)
    if resultado is None:
        st.error('Erro durante a avaliação do crédito.')
    elif resultado:
        st.error('Crédito negado.')
    else:
        st.success('Crédito aprovado.')




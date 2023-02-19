import streamlit as st
from joblib import load
import pandas as pd
from utils import Transformador
from imblearn.over_sampling import SMOTE

def avaliar_mau(dict_respostas):
	#modelo = load('obj/modelo_salvo2.joblib')
	modelo = load('obj/modelo.joblib')
	features = load('obj/features.joblib')

	if dict_respostas['Anos_desempregado'] > 0:
		dict_respostas['Anos_empregado'] = dict_respostas['Anos_desempregado'] * -1 
	
	respostas = []
	for coluna in features:
		respostas.append(dict_respostas[coluna])

	df_novo_cliente = pd.DataFrame(data=[respostas], columns=features)

	mau = modelo.predict(df_novo_cliente)[0]

	return mau



st.image('img/bytebank_logo.png')
st.write('# Precisando de credito amigao?')

my_expander_1 = st.expander('Trabalho')

my_expander_2 = st.expander('Pessoal')

my_expander_3 = st.expander('Familia')

dict_respostas = {}
lista_campos = load('obj/lista_campos.joblib')

with my_expander_1:
    col1_form, col2_form = st.columns(2)

    dict_respostas['Ocupacao'] = col1_form.selectbox('Qual sua Ocupação ?', lista_campos['Ocupacao'])

    dict_respostas['Categoria_de_renda'] = col1_form.selectbox('Qual categoria de renda ?', lista_campos['Categoria_de_renda'])
    
    dict_respostas['Rendimento_Anual'] = col1_form.slider('Qual o salario mensal ?',help='Podemos mover usando as setas do teclado', min_value=0, max_value=35000, step=500) * 12

    dict_respostas['Tem_telefone_trabalho'] = 1 if col2_form.selectbox('Tem um telefone do trabalho', ['sim','Não']) == 'Sim' else 0

    dict_respostas['Anos_empregado'] = col2_form.slider('Quantos Anos Empregado ?',help='Podemos mover usando as setas do teclado', min_value=0.0, max_value=60.0, step=0.5)

    dict_respostas['Anos_desempregado'] = col2_form.slider('Quantos Anos desempregado ?', help='Podemos mover usando as setas do teclado',min_value=0.0, max_value=60.0, step=0.5)




with my_expander_2:
    col3_form, col4_form = st.columns(2)

    dict_respostas['Grau_Escolaridade'] = col3_form.selectbox('Como foste de estudo formal ?', lista_campos['Grau_Escolaridade'])

    dict_respostas['Idade'] = col4_form.slider('Qual sua Idade ?',help='Podemos mover usando as setas do teclado', min_value=1, max_value=100, step=1)

    dict_respostas['Tem_Carro'] = 1 if col3_form.selectbox('Tem Carro ?', ['Sim', 'Não']) == 'Sim' else 0

    dict_respostas['Tem_telefone_fixo'] = 1 if col4_form.selectbox('Tem Telefone Fixo ?', ['Sim', 'Não']) == 'Sim' else 0

    dict_respostas['Tem_email'] = 1 if col3_form.selectbox('Tem email ?', ['Sim', 'Não']) == 'Sim' else 0

    dict_respostas['Estado_Civil'] = col4_form.selectbox('Como vai as namoradinha ?', lista_campos['Estado_Civil'])




with my_expander_3:
    col5_form, col6_form = st.columns(2)

    dict_respostas['Moradia'] = col5_form.selectbox('Tipo de maradia ?', lista_campos['Moradia'])

    dict_respostas['Tamanho_Familia'] = col6_form.slider('Tamanho da Familia ?',help='Podemos mover usando as setas do teclado',min_value=0, max_value=10, step=1)

    dict_respostas['Tem_Casa_Propria'] = 1 if col5_form.selectbox('Tem Casa Propria ?', ['Sim', 'Não']) == 'Sim' else 0

    dict_respostas['Qtd_Filhos'] = col6_form.slider('Tem Filhos ?', help='Podemos mover usando as setas do teclado',min_value=0, max_value=10, step=1)


if st.button('Avaliar crédito'):
    
	if avaliar_mau(dict_respostas):
		st.error('Crédito negado')
	else:
		st.success('Crédito aprovado')




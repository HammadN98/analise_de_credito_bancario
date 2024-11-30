# Concessão de Crédito - Análise de Inadimplência  

## **Visão Geral**  
O projeto aborda um problema crítico enfrentado pelo setor financeiro: **identificar clientes com maior risco de inadimplência** no contexto da concessão de crédito. Utilizando técnicas avançadas de análise de dados e machine learning, desenvolvemos um pipeline robusto que integra limpeza de dados, feature engineering e modelagem preditiva. O objetivo é oferecer ao Banco Byte Bank insights acionáveis para minimizar riscos e otimizar a rentabilidade.  

---

## **Objetivos do Projeto**  
- Identificar os principais fatores que influenciam a inadimplência.  
- Construir modelos preditivos para categorizar clientes como "bons" ou "maus pagadores".  
- Fornecer recomendações acionáveis para reduzir perdas financeiras.  

---

## **Estrutura de Dados e Limpeza**  

### **Características do Dataset**  
| **Coluna**               | **Tipo**      | **Descrição**                         |  
|--------------------------|---------------|---------------------------------------|  
| ID_Cliente               | Numérica      | Identificador único do cliente.       |  
| Rendimento_Anual         | Contínua      | Rendimento anual reportado (em R$).   |  
| Anos_empregado           | Contínua      | Tempo de trabalho atual (anos).       |  
| Faixa_atraso             | Categórica    | Faixa de atraso de pagamento.         |  

### **Distribuição das Variáveis Quantitativas**  
As distribuições foram analisadas e ajustadas para excluir outliers, como no caso de `Rendimento_Anual`, onde valores extremos acima de R$ 700.000 foram tratados.  

![Boxplot de Rendimento](https://via.placeholder.com/600x400)  

---

## **Metodologia e Pipeline de Machine Learning**  

1. **Limpeza de Dados**:  
   - Remoção de duplicatas e valores irrelevantes.  
   - Substituição de valores inconsistentes, como `-1000.7 anos de trabalho` para `-1` para marcar pensionistas.  

2. **Transformações**:  
   - Codificação de variáveis categóricas usando OneHotEncoder.  
   - Normalização de variáveis contínuas com MinMaxScaler.  

3. **Modelos Avaliados**:  
   - **Random Forest**  
   - **Decision Tree**  
   - **KNN**  
   - **Logistic Regression**  

4. **Balanceamento**:  
   Utilizamos **SMOTE** para lidar com 


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

![Boxplot de Rendimento](https://github.com/HammadN98/analise_de_credito_bancario/blob/main/img/rendimento%20anual_bank.png)  

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
   Utilizamos **SMOTE** para lidar com o desbalanceamento significativo entre bons e maus pagadores.  

---

## **Resultados dos Modelos**  

| Modelo                   | AUC   | Precisão  | Recall    | KS       |  
|--------------------------|-------|-----------|-----------|----------|  
| Random Forest            | 0.83  | 98%       | 36%       | 0.97     |  
| Decision Tree            | 0.75  | 97%       | 37%       | 0.94     |  
| Logistic Regression      | 0.58  | 55%       | 58%       | 0.13     |  
| KNN                      | 0.71  | 90%       | 45%       | 0.81     |  

---

## **Insights e Visualizações**  

### **Distribuição de Pagamentos em Atraso**  
A maior parte dos atrasos foi registrada na faixa de **1-29 dias**, indicando que intervenções precoces podem melhorar a recuperação.  

| Faixa de Atraso          | Quantidade de Clientes | Percentual |  
|--------------------------|------------------------|------------|  
| Pagamento Realizado      | 442.031               | 42%        |  
| 1-29 dias                | 383.120               | 37%        |  

![Distribuição de Atrasos](https://github.com/HammadN98/analise_de_credito_bancario/blob/main/img/atraso_bank.png)  
<img src="https://github.com/HammadN98/analise_de_credito_bancario/blob/main/img/atraso_bank.png" width="600"/>

### **Análise Vintage: Taxa de Inadimplência ao Longo do Tempo**  
Clientes com maior tempo de relacionamento (MOB > 10 meses) apresentaram aumento na inadimplência.  

![Curva Vintage](https://github.com/HammadN98/analise_de_credito_bancario/blob/main/img/mob_bank.png)  

---

## **Recomendações Acionáveis**  

1. **Adoção do Modelo Random Forest**  
   - Implementar o modelo preditivo na tomada de decisões de crédito.  

2. **Intervenções Precoces**  
   - Desenvolver alertas automáticos para clientes com atrasos menores que 30 dias.  

3. **Política de Renovação**  
   - Atualizar condições de crédito para clientes com MOB superior a 10 meses e histórico de atrasos.  

4. **Monitoramento Contínuo**  
   - Incorporar dados em tempo real para aprimorar previsões e ajustes de crédito.  

---

## **Conclusão**  
Este projeto não só apresenta um modelo eficiente para previsão de inadimplência, como também fornece insights valiosos para estratégia operacional e de crédito. O uso de análises temporais e machine learning ajudará o Byte Bank a reduzir riscos financeiros e melhorar sua eficiência operacional.  

**Próximos Passos:**  
- Expandir o modelo para incluir variáveis externas, como indicadores macroeconômicos.  
- Criar uma API para integração do modelo com sistemas existentes do banco.  


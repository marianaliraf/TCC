# -*- coding: utf-8 -*-
"""
Created on Thu Feb 24 10:40:28 2022

@author: mlfarias
"""

'''
Script para criação de tabela de descrição de respostas do
questionário do SAEB 2017
'''
import pandas as pd
import re 
import string
#pandas-profilling

respostas = pd.read_csv('C:/Users/maril/Documents/ufs/TCC e Pesquisa IDEB/Perguntas Questionário - Respostas.csv')
questoes = pd.read_csv('C:/Users/maril/Documents/ufs/TCC e Pesquisa IDEB/Perguntas Questionário - Questões.csv')

derivadas_se = pd.read_csv('C:/Users/maril/Documents/ufs/TCC e Pesquisa IDEB/TCC/datasets/variaveis_derivadas_se.csv')

#questoes.set_index('Questão', inplace=True)
#respostas.set_index('Questão', inplace=True)
   
#list_resp = list(string.ascii_uppercase)[:7]   

coluna_questoes = list(derivadas_se.columns)[8:]

novo_df = pd.DataFrame()


for col_questao in coluna_questoes: 
    if re.search(r"Q0\d\d", col_questao):
       intervalo = re.search(r"Q0\d\d",  col_questao).span()
       #Pegando a Descrição da Questão
       q = col_questao[intervalo[0]:intervalo[1]]
       questao = questoes.loc[questoes['Questão'] == q]
       resposta = respostas.loc[respostas['Questão'] == q]
            
       #Pegando a Resposta
       letra_resp = col_questao[-1]
            
       questao = list(questao['Descrição'])[0]
       resposta = list(resposta[letra_resp])[0]
            
       #Criando Sentença Pergunta + Resposta para facilitar a Análise
       nova_descricao = questao +" R: "+ resposta
            
       #Adicionando o Dataframe de Descrição da Resposta
            
       novo_df.insert(len(novo_df), col_questao, [nova_descricao])
            
        #print(respostas[questao])
    else:
        print('Não encontrou')

novo_df.rename({0: 'Descrição'}, inplace=True)
novo_df = novo_df.T
novo_df['Questão_d'] = novo_df.index

#novo_df.to_csv('descricao_respostas_saeb.csv', )

#Criando descrição para Sergipe
resul_sergipe = pd.read_csv('C:/Users/maril/Documents/ufs/TCC e Pesquisa IDEB/TCC/datasets/resultado_analise_merge_dataset_completo_SE.csv')

resul_sergipe.rename(columns=({'Unnamed: 0': 'ID_ESCOLA'}), inplace=True)
resul_sergipe.set_index('ID_ESCOLA', inplace=True)

resul_sergipe_sumarizado = resul_sergipe.sum()


resul_sergipe = resul_sergipe.T
resul_sergipe['Questão'] = resul_sergipe.index

df_resul_sergipe_descricao = pd.merge(resul_sergipe, novo_df, how='left', left_on='Questão', right_on='Questão_d')
df_resul_sergipe_descricao.drop(columns=('Questão_d'), inplace=True)
df_resul_sergipe_descricao.set_index('Questão', inplace=True)

resul_sergipe_sumarizado.to_csv('C:/Users/maril/Documents/ufs/TCC e Pesquisa IDEB/TCC/datasets/resultado_analise_sumarizada_sergipe.csv')
df_resul_sergipe_descricao.to_csv('C:/Users/maril/Documents/ufs/TCC e Pesquisa IDEB/TCC/datasets/resultado_analise_sergipe_descricao.csv')

#Criando descrição para Alagoas

resul_alagoas = pd.read_csv('C:/Users/maril/Documents/ufs/TCC e Pesquisa IDEB/TCC/datasets/resultado_analise_merge_dataset_completo_AL.csv')

resul_alagoas.rename(columns=({'Unnamed: 0': 'ID_ESCOLA'}), inplace=True)
resul_alagoas.set_index('ID_ESCOLA', inplace=True)

resul_alagoas_sumarizado = resul_alagoas.sum()



resul_alagoas = resul_alagoas.T
resul_alagoas['Questão'] = resul_alagoas.index

df_resul_alagoas_descricao = pd.merge(resul_alagoas, novo_df, how='left', left_on='Questão', right_on='Questão_d')
df_resul_alagoas_descricao.drop(columns=('Questão_d'), inplace=True)
df_resul_alagoas_descricao.set_index('Questão', inplace=True)

resul_alagoas_sumarizado.to_csv('C:/Users/maril/Documents/ufs/TCC e Pesquisa IDEB/TCC/datasets/resultado_analise_sumarizada_alagoas.csv')
df_resul_alagoas_descricao.to_csv('C:/Users/maril/Documents/ufs/TCC e Pesquisa IDEB/TCC/datasets/resultado_analise_alagoas_descricao.csv')

#Criando descrição para Bahia

resul_bahia = pd.read_csv('C:/Users/maril/Documents/ufs/TCC e Pesquisa IDEB/TCC/datasets/resultado_analise_merge_dataset_completo_BA.csv')

resul_bahia.rename(columns=({'Unnamed: 0': 'ID_ESCOLA'}), inplace=True)
resul_bahia.set_index('ID_ESCOLA', inplace=True)

resul_bahia_sumarizado = resul_bahia.sum()

resul_bahia = resul_bahia.T
resul_bahia['Questão'] = resul_bahia.index

df_resul_bahia_descricao = pd.merge(resul_bahia, novo_df, how='left', left_on='Questão', right_on='Questão_d')
df_resul_bahia_descricao.drop(columns=('Questão_d'), inplace=True)
df_resul_bahia_descricao.set_index('Questão', inplace=True)

resul_bahia_sumarizado.to_csv('C:/Users/maril/Documents/ufs/TCC e Pesquisa IDEB/TCC/datasets/resultado_analise_sumarizada_bahia.csv')
df_resul_bahia_descricao.to_csv('C:/Users/maril/Documents/ufs/TCC e Pesquisa IDEB/TCC/datasets/resultado_analise_bahia_descricao.csv')

#Criando Dataframe com Variaveis em comum

lista_de_colunas = list(resul_bahia.index) + list(resul_sergipe.index) + list(resul_alagoas.index)
lista_de_colunas = list(set(lista_de_colunas))
lista_de_colunas.remove('Valor Real Ideb')
lista_de_colunas.remove('Previsão Ideb')

df_variaveis_comum = pd.DataFrame(index=lista_de_colunas, columns=['Sergipe', 'Alagoas', 'Bahia'])
    

for index in lista_de_colunas:   
    if (index in list(resul_sergipe_sumarizado.index)):
        df_variaveis_comum.loc[index]['Sergipe'] = resul_sergipe_sumarizado.loc[index]
    if (index in list(resul_alagoas_sumarizado.index)):
        df_variaveis_comum.loc[index]['Alagoas'] = resul_alagoas_sumarizado.loc[index]
    if (index in list(resul_bahia_sumarizado.index)):
        df_variaveis_comum.loc[index]['Bahia'] = resul_bahia_sumarizado.loc[index]
    
df_variaveis_comum.drop(['DT_ANO_LETIVO_TERMINO', 'DT_ANO_LETIVO_INICIO'], inplace=True)
df_variaveis_comum.fillna(0, inplace=True)

df_variaveis_comum.to_csv('C:/Users/maril/Documents/ufs/TCC e Pesquisa IDEB/TCC/datasets/resultado_em_comum.csv')
#Criando DESCRIÇÃO PARA OS 3 ESTADOS


resul_todos = pd.read_csv('C:/Users/maril/Documents/ufs/TCC e Pesquisa IDEB/TCC/datasets/resultado_analise_merge_dataset_completo.csv')

resul_todos.rename(columns=({'Unnamed: 0': 'ID_ESCOLA'}), inplace=True)
resul_todos.set_index('ID_ESCOLA', inplace=True)

resul_todos_sumarizado = resul_todos.sum()

resul_todos = resul_todos.T
resul_todos['Questão'] = resul_todos.index

df_resul_todos_descricao = pd.merge(resul_todos, novo_df, how='left', left_on='Questão', right_on='Questão_d')
df_resul_todos_descricao.drop(columns=('Questão_d'), inplace=True)
df_resul_todos_descricao.set_index('Questão', inplace=True)

resul_todos_sumarizado.to_csv('C:/Users/maril/Documents/ufs/TCC e Pesquisa IDEB/TCC/datasets/resultado_analise_sumarizada_todos.csv')
df_resul_todos_descricao.to_csv('C:/Users/maril/Documents/ufs/TCC e Pesquisa IDEB/TCC/datasets/resultado_analise_todos_descricao.csv')

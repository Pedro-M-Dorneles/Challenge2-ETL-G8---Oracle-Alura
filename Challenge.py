import pandas as pd
import numpy as np
#Convertendo os Arquivos para análise em um Data Frame
dado = pd.read_json('G:/Meu Drive/Oracle_alura/ETL G8/Challenge_2/Dados/TelecomX_Data.json')
print(dado.head(),'\n\n')


#Normalizando o arquivo
normal = pd.json_normalize(dado.to_dict(orient='records'))
print(normal)

#Verificando valores nulos e duplicados
print('NULOS ->',normal.isnull().sum())
print('DUPLICADOS',normal.duplicated().sum())

#Valores unicos em cada coluna
for coluna in normal.columns:
    unico=normal[coluna].unique()
    print(f'\n\nValores unicos da coluna {coluna}->{unico} \n\n')



#Transformando certas colunas para Float
normal['account.Charges.Total']=pd.to_numeric(normal['account.Charges.Total'], errors='coerce')
normal['customer.tenure']=pd.to_numeric(normal['customer.tenure'], errors='coerce')

#Criando uma coluna para gastos diarios
normal=normal.drop('Total.Day', errors='ignore')
normal['Total.Day']=((normal['account.Charges.Total'] / normal['customer.tenure'])/30).round(2)
normal.insert(19,'Total.Day', normal.pop('Total.Day'))

#Removendo os valores vazios da coluna Churn
normal.query('Churn != ""', inplace=True)
print('\n\nValores unicos da coluna Churn', normal['Churn'].unique(),'\n\n')



#Estatisticas descritivas
descrito = normal.describe()

mean = descrito.loc['mean']
median = descrito.loc['50%']
std = descrito.loc['std']
print(f'Mediana\n{median}\n\n media\n{mean}\n\n std\n{std}\n\n')


#Fazendo os gráficos pra perceber os motivos das saida
import plotly.express as px
import matplotlib.pyplot as plt
print(normal.info())


#Gráficos em função do dado Churn
#Tenure
fig, ax = plt.subplots(figsize=(8,5))

churn_yes = normal[normal['Churn'] == 'Yes']['customer.tenure']
churn_no  = normal[normal['Churn'] == 'No']['customer.tenure']

ax.hist([churn_yes, churn_no], bins=20, label=['Churn: Sim', 'Churn: Não'], stacked=True)
nome='Histograma de Tenure por Churn'
ax.set_title(nome)
ax.set_xlabel('Meses de permanência')
ax.set_ylabel('Número de clientes')
ax.legend()

fig.savefig(f'G:/Meu Drive/Oracle_alura/ETL G8/Challenge_2/Gráficos/{nome}.png', transparent=False, dpi=300, bbox_inches='tight')
plt.show()

#Outras variaveis não numericas
def churn_grafico(coluna, color):
    fig, ax = plt.subplots(figsize=(8,5))
    churn_yes = normal[normal['Churn'] == 'Yes'][coluna]
    churn_no  = normal[normal['Churn'] == 'No'][coluna]
    
    ax.hist([churn_yes, churn_no], bins=50, label=['Churn: Sim', 'Churn: Não'], stacked=True, color=color)
    nome_f=f'Histograma de {coluna} por Churn'
    ax.set_title(nome_f)
    ax.set_xlabel(coluna)
    ax.set_ylabel('Número de clientes')
    ax.legend()

    fig.savefig(f'G:/Meu Drive/Oracle_alura/ETL G8/Challenge_2/Gráficos/{nome_f}.png', transparent=False, dpi=300, bbox_inches='tight')
    plt.show()

    

#Contagem de evasão variaveis numéricas
churn_grafico('account.Charges.Total', ['red', 'gold'])
churn_grafico('Total.Day', ['#4DF6FA', '#FA8F4D'])


#Contagem de evasão variaveis categóricas
churn_grafico('customer.gender', ['#722BFA','#FAEF2A'])
churn_grafico('account.Contract', ['#FA1E58', '#1EFA3C'])
churn_grafico('account.PaymentMethod', ['#D33FFA', '#B4FA3E'])
churn_grafico('internet.InternetService', ['#FA573A', '#3CFAA9'])


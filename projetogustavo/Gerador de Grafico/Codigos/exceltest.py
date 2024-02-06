
import random
import xlsxwriter
import os
import pandas as pd
from pathlib import Path
from input_clear import data_input_cleaner
from data_manipulation import bloco_da_pergunta,preenche
# %%
ROOT_PATH=Path(__file__).parent.parent
SRCS=ROOT_PATH / 'Codigos'
INPUT_FILE_PATH = ROOT_PATH/'Excel de Pesquisa'
OUTPUT_FILE_PATH = ROOT_PATH/'Excel de Resposta'

INPUT_FILE_NAME=os.listdir(INPUT_FILE_PATH).pop()
INPUT_SHEET_NAME='Base_%'


input_data,perguntas_linha = data_input_cleaner()


# %%

numero_linha= perguntas_linha.linha

dict_perguntas_completas = {}
for i in range(numero_linha.__len__()):
    dict_opcoes={}
    index,texto=perguntas_linha.iloc[i]
    
    pergunta_bloco = bloco_da_pergunta(input_data,numero_linha,i)

    
    for index,linha in pergunta_bloco.iterrows():#percorrendo em cada pergunta
        
        if not pd.isna(linha['Unnamed: 0']):
            dados_list = [{'pergunta':linha['Unnamed: 0']},]
        
        if not pd.isna(linha['Unnamed: 1']):#achou uma opcao
            option_list =  {'opcao':linha['Unnamed: 1']}
            
            op=0
            aux = []
            for j in range(3,len(linha)):
                option = linha.iloc[j]
                option_not_empty = not pd.isna(option)
                
                if option_not_empty :
                    aux.append(option)
                  
                else:#se linha com opcao for vazia
            
                    op+=1
                    pergunta_dict = preenche(op, *aux)  # Supondo que preenche retorna um dicionário
                    print(f"pergunta:{(pergunta_dict)}")
                    chave, valor = next(iter(pergunta_dict.items()))
                    option_list[chave]=valor
                    print(f"opcao:{option_list}")
                    aux=[]
                   
            if op==3:
                pergunta_dict = preenche(4, *aux)  # Supondo que preenche retorna um dicionário
                chave, valor = next(iter(pergunta_dict.items()))
                option_list[chave]=valor

            
            dict_opcoes[option_list['opcao']] =option_list
    dict_perguntas_completas[texto]=dict_opcoes      
    


# %%

# Seu código existente para carregar dados e estruturar perguntas

# Criar um escritor de Excel
excel_file_path = 'graficos_excel.xlsx'
workbook = xlsxwriter.Workbook(excel_file_path)

# Criar uma lista para armazenar os DataFrames de cada pergunta
dataframes = []

for pergunta in perguntas_linha['pergunta']:
    print(dict_perguntas_completas[pergunta])
    infos_dict = {}
    for opcao, valor in dict_perguntas_completas[pergunta].items():
        if opcao == 'Contagem total (respondendo) ':
            valor_total = valor['sexo']['total']
            continue
        print('opcao: ', opcao)
        valor = valor['sexo']['total']
        print("valor", valor)
        infos_dict[str(opcao)] = float(valor) * 100  # Multiplicar por 100 para obter o percentual

    # Plotting the histogram after accumulating data
    if infos_dict:
        labels = list(infos_dict.keys())
        values = list(infos_dict.values())

        # Gerar uma lista de cores aleatórias
        colors = [f"#{random.randint(0, 0xFFFFFF):06x}" for _ in range(len(labels))]

        # Adicionar uma nova planilha para cada pergunta
        pergunta_comlpleta = pergunta
        pergunta=pergunta[0:20].replace(":"," ")
        worksheet = workbook.add_worksheet(f'Pergunta_{pergunta}')

        # Adicionar os dados à planilha
        worksheet.write_row('A1', ['Opções', 'Valores'])
        worksheet.write_column('A2', labels)
        worksheet.write_column('B2', values)

        # Adicionar um gráfico de barras à planilha
        chart = workbook.add_chart({'type': 'bar'})
        chart.add_series({'values': f'=Pergunta_{pergunta}!$B$2:$B${len(values) + 1}',
                          'categories': f'=Pergunta_{pergunta}!$A$2:$A${len(labels) + 1}',
                          'name': 'Valores'})
        chart.set_x_axis({'name': 'Opções'})
        chart.set_y_axis({'name': 'Valores (%)'})
        chart.set_title({'name': f'Pergunta_{pergunta_comlpleta} - Total = {valor_total}'})
        worksheet.insert_chart('D2', chart)

        # Adicionar dados à lista
        dataframes.append(pd.DataFrame({'Opções': labels, 'Valores': values}))

# Combinar todos os DataFrames em um único DataFrame
resultado_final = pd.concat(dataframes, axis=1)

# Salvar o DataFrame em uma planilha do Excel usando a função 'to_excel' do pandas
resultado_final.to_excel(excel_file_path, sheet_name='Dados', index=False, engine='openpyxl')

# Fechar o arquivo Excel
workbook.close()



from imports import *

ROOT_PATH = Path(__file__).parent.parent
SRCS = ROOT_PATH / 'Codigos'
INPUT_FILE_PATH = ROOT_PATH / 'Excel de Pesquisa'
OUTPUT_FILE_PATH = ROOT_PATH / 'Excel de Resposta'

INPUT_FILE_NAME = os.listdir(INPUT_FILE_PATH).pop()
INPUT_SHEET_NAME = 'Base_%'

input_data, perguntas_linha = data_input_cleaner()

numero_linha = perguntas_linha.linha

dict_perguntas_completas = {}
for i in range(numero_linha.__len__()):
    dict_opcoes = {}
    index, texto = perguntas_linha.iloc[i]

    pergunta_bloco = bloco_da_pergunta(input_data, numero_linha, i)

    for index, linha in pergunta_bloco.iterrows():
        if not pd.isna(linha['Unnamed: 0']):
            dados_list = [{'pergunta': linha['Unnamed: 0']},]

        if not pd.isna(linha['Unnamed: 1']):
            option_list = {'opcao': linha['Unnamed: 1']}

            op = 0
            aux = []
            for j in range(3, len(linha)):
                option = linha.iloc[j]
                option_not_empty = not pd.isna(option)

                if option_not_empty:
                    aux.append(option)
                else:
                    op += 1
                    pergunta_dict = preenche(op, *aux)
                    chave, valor = next(iter(pergunta_dict.items()))
                    option_list[chave] = valor
                    aux = []

            if op == 3:
                pergunta_dict = preenche(4, *aux)
                chave, valor = next(iter(pergunta_dict.items()))
                option_list[chave] = valor

            dict_opcoes[option_list['opcao']] = option_list
    dict_perguntas_completas[texto] = dict_opcoes

# Criar um escritor de Excel
excel_file_path = 'graficos_excel_melhorados.xlsx'
workbook = xlsxwriter.Workbook(excel_file_path)

# Função para gerar gráficos de barras
def gerar_grafico(worksheet, labels, values, pergunta, valor_total):
    chart = workbook.add_chart({'type': 'bar'})
    chart.add_series({
        'values': f"='{worksheet.get_name()}'!$B$2:$B${len(values) + 1}",
        'categories': f"='{worksheet.get_name()}'!$A$2:$A${len(labels) + 1}",
        'name': 'Valores'
    })
    chart.set_x_axis({'name': 'Opções'})
    chart.set_y_axis({'name': 'Valores (%)'})
    chart.set_title({'name': f'Pergunta: {pergunta} - Total = {valor_total}'})
    chart.set_size({'width': 720, 'height': 576})
    worksheet.insert_chart('D2', chart)

# Criar uma lista para armazenar os DataFrames de cada pergunta
dataframes = []

for pergunta in perguntas_linha['pergunta']:
    print(dict_perguntas_completas[pergunta])
    infos_dict = {}
    valor_total = 0
    for opcao, valor in dict_perguntas_completas[pergunta].items():
        if opcao == 'Contagem total (respondendo) ':
            valor_total = valor['sexo']['total']
            continue
        valor = valor['sexo']['total']
        infos_dict[str(opcao)] = float(valor) * 100

    if infos_dict:
        labels = list(infos_dict.keys())
        values = list(infos_dict.values())

        # Usar uma paleta de cores consistente
        colors = ['#4CAF50', '#FFC107', '#2196F3', '#FF5722', '#9C27B0', '#E91E63', '#00BCD4', '#8BC34A']

        # Adicionar uma nova planilha para cada pergunta
        pergunta_completa = pergunta
        pergunta = pergunta[0:20].replace(":", " ")
        worksheet_name = f'Pergunta_{pergunta}'
        worksheet = workbook.add_worksheet(worksheet_name)

        # Adicionar os dados à planilha
        worksheet.write_row('A1', ['Opções', 'Valores'])
        worksheet.write_column('A2', labels)
        worksheet.write_column('B2', values)

        # Gerar o gráfico de barras
        gerar_grafico(worksheet, labels, values, pergunta_completa, valor_total)

        # Adicionar dados à lista
        dataframes.append(pd.DataFrame({'Opções': labels, 'Valores': values}))

# Combinar todos os DataFrames em um único DataFrame
resultado_final = pd.concat(dataframes, axis=1)

# Salvar o DataFrame em uma planilha do Excel usando a função 'to_excel' do pandas
resultado_final.to_excel(excel_file_path, sheet_name='Dados', index=False, engine='openpyxl')

# Fechar o arquivo Excel
workbook.close()
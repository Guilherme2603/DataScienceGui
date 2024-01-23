import random
import pandas as pd
import xlsxwriter
import streamlit as st
from pathlib import Path
import os

ROOT_PATH=Path(__file__).parent.parent
SRCS=ROOT_PATH / 'Codigos'
INPUT_FILE_PATH = ROOT_PATH/'Excel de Pesquisa'
OUTPUT_FILE_PATH = ROOT_PATH/'Excel de Resposta'

INPUT_FILE_NAME = os.listdir(INPUT_FILE_PATH).pop()
INPUT_SHEET_NAME_DEFAULT ='Base_%'

def data_input_cleaner():
    
    input_data = pd.read_excel(f'{INPUT_FILE_PATH}/{INPUT_FILE_NAME}', 
                            sheet_name=INPUT_SHEET_NAME_DEFAULT).reset_index()

    input_data = input_data['Unnamed: 0'].dropna().reset_index()
    input_data.columns = ['linha','pergunta']

    return input_data



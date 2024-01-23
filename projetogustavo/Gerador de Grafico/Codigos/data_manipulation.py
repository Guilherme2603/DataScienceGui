import random
import pandas as pd
import xlsxwriter
import streamlit as st
from pathlib import Path
import os


def op_sexo(total,masculino,feminino):
    sexo = {'sexo':{"total":total,"masculino":masculino,"feminino":feminino}}
    return sexo
def op_etaria(total,dezesseis,trinta,cinquenta):
    faixa_etaria ={'faixa_etaria':{"total":total,"16_29":dezesseis,"30_49":trinta,
                                    "50":cinquenta}
                }
    return faixa_etaria
def op_classe(total,ab,c,de):
    classe_social = {'classe_social':{"total":total,"AB":ab,"C":c,"DE":de}}
    return classe_social
def op_regiao(total,se,s,co,n,ne):
    regiao = {'regiao':{"total":total,"sudeste":se,"sul":s,"centrooeste":co,"norte":n,"nordeste":ne}}
    return regiao

def opcoes(pergunta,sexo,faixa_etaria,classe_social,regiao):
    dados = {'pergunta':pergunta,"sexo":sexo,"faixa_etaria":faixa_etaria,"classe_social":classe_social,"regiao":regiao}
    return dados
def preenche(op,*args):
    res =''
    if op ==1:
        res = op_sexo(*args)
    elif op ==2 :
        res = op_etaria(*args)
    elif op ==3 :
        res = op_classe(*args)
    elif op ==4 :
        res = op_regiao(*args)
    elif op ==5 :
        opcoes(*args)
    return res

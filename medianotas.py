import pandas as pd
import numpy as np
import unidecode
import os

chunks = pd.read_csv("C:\\Users\\vicen\\Downloads\\MICRODADOS_ENEM_2023.csv", sep=';', encoding='latin1', chunksize=10000)
medianotas = pd.DataFrame()
soma = {}
contagem = {}
for chunk in chunks:
    chunk['nota'] = (chunk['NU_NOTA_MT'] + chunk['NU_NOTA_LC'] + chunk['NU_NOTA_CN'] + chunk['NU_NOTA_CH'] + chunk['NU_NOTA_REDACAO']) / 5
    agruped = chunk.groupby('NO_MUNICIPIO_ESC')['nota'].agg(['sum', 'count']).reset_index()
    for _, row in agruped.iterrows():
        municipio = row['NO_MUNICIPIO_ESC']
        if pd.isnull(municipio):  # ignora cidades nulas
            continue
        if municipio not in soma:
            soma[municipio] = 0
            contagem[municipio] = 0
            
        soma[municipio] += row['sum']
        contagem[municipio] += row['count']
dados = []
for municipio in soma:
    if contagem[municipio] > 0:
        media = soma[municipio] / contagem[municipio]
        dados.append({'NO_MUNICIPIO_ESC': municipio, 'nota': media})
medianotas = pd.DataFrame(dados)
medianotas['NO_MUNICIPIO_ESC'] = medianotas['NO_MUNICIPIO_ESC'].astype(str).str.upper().str.strip().apply(unidecode.unidecode)
medianotas.to_csv("medianotas.csv", index=False)
print("Arquivo salvo em:", os.path.abspath("medianotas.csv"))
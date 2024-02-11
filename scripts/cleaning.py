# ./scripts/cleaning.py
# ==================================================
# standard
import os, glob
# requirements
import pandas as pd
# --------------------------------------------------

def data_cleaning() -> None:
    
    txt_file = open('./temp/TERRITORIO.txt', 'r').readlines()
    txt_file = [line.rstrip()for line in txt_file]
    
    not_found = open('./temp/NOTFOUND.txt', 'r').readlines()
    not_found = [line.rstrip() for line in not_found]
    
    found = [x[x.find(';')+1:] for x in txt_file if x[:x.find(';')] not in not_found]
    
    csv_downloads = glob.glob('./downloads/*.csv')
    csv_downloads.sort(key=os.path.getctime)
    
    df = pd.DataFrame()
    for te, fi in zip(found, csv_downloads):
        data_file = pd.read_csv(fi, sep=',', encoding='iso-8859-1', skiprows=10, skipfooter=29, header=None, engine='python')
        data_file.columns = ['PARTIDO', 'TOTAL', 'PORCENTAJE_VALIDO']
        data_file['UBICACION'] = te
        
        print(f'[INFO] Appending: {fi}')
        df = pd.concat([df, data_file])
    df['PORCENTAJE_VALIDO'] = df['PORCENTAJE_VALIDO'] / 100
    
    print('Cantidad de partidos: {}'.format(len(df['PARTIDO'].unique())))
    print('Cantidad de distritos: {}'.format(len(df['UBICACION'].unique())))
    print('Total Dataset = Nro. Partidos x Nro. distritos: {}'.format(len(df) == len(df['PARTIDO'].unique()) * len(df['UBICACION'].unique())))
    
    df = df.pivot(index='UBICACION', columns='PARTIDO', values=['TOTAL', 'PORCENTAJE_VALIDO']).reset_index()
    df.columns = ['{}_{}'.format(i,o) for o,i in df.columns]
    df['_UBICACION'] = df['_UBICACION'].str.split('//')
    
    for i, col in enumerate(['DEPARTAMENTO', 'PROVINCIA', 'DISTRITO']):
        df[col] = df['_UBICACION'].apply(lambda y: pd.Series(y[i]))
    
    df = df.sort_values(by=['DEPARTAMENTO', 'PROVINCIA', 'DISTRITO'])
    
    # [NOTE] merge con Ubigeo RENIEC
    # --------------------------------------------------
    ubigeo = pd.read_pickle('./temp/UBI_RENIEC.pkl')
    df = df.merge(ubigeo, how='inner', on=['DEPARTAMENTO', 'PROVINCIA', 'DISTRITO'])
    
    re = len(df.columns) - df.columns.get_loc('DEPARTAMENTO')
    df = df[['UBIGEO_RENIEC', 'DEPARTAMENTO', 'PROVINCIA', 'DISTRITO'] + list(df.columns)[1:-re]]
    df.to_csv(f5 := './temp/RESULTS.csv', sep=';', index_label='ID_DIS', encoding='iso-8859-1')
    
    # [NOTE] cantidad de provincias por departamento
    # --------------------------------------------------
    dep = list(df['DEPARTAMENTO'].unique())
    for d in dep:
        print('[INFO] {}: {}'.format(d, len(df[df['DEPARTAMENTO'] == d]['PROVINCIA'].unique())))
    
    # [NOTE] Loreto falta 1 provincia
    # df[df['DEPARTAMENTO'] == 'Loreto']['PROVINCIA'].unique()
    
    print(f'Exported final file at: {f5}')

# ./scripts/links.py
# ==================================================
# standard
import os
# requirements
import pandas as pd
# --------------------------------------------------

def retrieve_links() -> None:
    
    df = pd.read_excel('./resources/UBIGEO_RENIEC.xlsx', sheet_name='ubigeo_reniec', dtype={'Ubigeo': str})
    df = df[df.columns[:4]]
    
    df['departamento'] = df['Ubigeo'].str.slice(start=0, stop=2) + '0000'
    df['provincia'] = df['Ubigeo'].str.slice(start=0, stop=4) + '00'
    df['distrito'] = df['Ubigeo']
    
    dep = list(df['departamento'])
    pro = list(df['provincia'])
    dis = list(df['distrito'])
    idl = [x for x in range(len(list(df['distrito'])))]
    
    with open(f1 :=  './temp/LINKS.txt', 'w') as txt_file:
        for de, pr, di, i in zip(dep, pro, dis, idl):
            txt_file.write('{}-https://www.resultados.eleccionesgenerales2021.pe/EG2021/EleccionesPresidenciales/RePres/P/{}/{}/{}\n'.format(i, de, pr, di))
    
    dep = list(df['Departamento'])
    pro = list(df['Provincia'])
    dis = list(df['Distrito'])
    idl = [d for d in range(len(list(df['distrito'])))]
    
    with open(f2 := './temp/TERRITORIO.txt', 'w') as txt_file:
        for de, pr, di, i in zip(dep, pro, dis, idl):
            txt_file.write('{};{}//{}//{}\n'.format(i, de, pr, di))
    
    df = df.sort_values(by=['Departamento', 'Provincia', 'Distrito'])
    df = df[['Ubigeo', 'Departamento', 'Provincia', 'Distrito']]
    df.columns = ['UBIGEO_RENIEC', 'DEPARTAMENTO', 'PROVINCIA', 'DISTRITO']
    
    df.to_pickle(f3 := './temp/UBI_RENIEC.pkl')
    
    print(f'Created files at: {f1}, {f2}, {f3}')

import pandas as pd
import os

def create_output_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

def pregunta_01():
    """
        Realice la limpieza del archivo "files/input/solicitudes_de_credito.csv".
        El archivo tiene problemas como registros duplicados y datos faltantes.
        Tenga en cuenta todas las verificaciones discutidas en clase para
        realizar la limpieza de los datos.

        El archivo limpio debe escribirse en "files/output/solicitudes_de_credito.csv"
    """
    # Se elimina el archivo en caso de que ya exista:
    if os.path.exists('files/output/solicitudes_de_credito.csv'):
        os.remove('files/output/solicitudes_de_credito.csv')
    
    # Se abre el archivo
    ruta = 'files/input/solicitudes_de_credito.csv'
    df = pd.read_csv(ruta, sep=';', index_col=0, encoding='UTF-8')

    #Se limpian las columnas
    df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    df = df.apply(lambda x: x.str.lower() if x.dtype == "object" else x)

        # Limpiar idea_negocio
    df['idea_negocio'] = df['idea_negocio'].str.replace(' ','_').str.replace('-','_').str.strip('_')

    # Limpiar la columna barrio
    df['barrio'] = df['barrio'].str.replace(' ', '_').str.replace('-', '_').str.replace('.', '').str.strip('_')

    # Dar formato a estrato
    df['estrato'] = df['estrato'].astype(int)

    # Dar formato a comuna_ciudadano
    df['comuna_ciudadano'] = df['comuna_ciudadano'].astype(int)

    # Limpiar la columna fecha_de_beneficio
    df['fecha_de_beneficio'] = df['fecha_de_beneficio'].apply(lambda x: '/'.join([y for y in reversed(x.split('/'))]) if len(x.split('/')[0]) == 4 else x)

    # Limpiar la columna monto_del_credito
    df['monto_del_credito'] = pd.to_numeric(df['monto_del_credito'].str.replace('$', '').str.replace(',', ''), errors='coerce').astype(int)


    # Limpiar la columna linea_credito
    df['línea_credito'] = df['línea_credito'].str.replace(r'[\s\-.]', '_', regex=True).str.strip('_')

    for columna in df.columns:
        df[f'{columna}'] = df[f'{columna}'].replace({None: pd.NA, '': pd.NA})
        # Eliminamos las filas que sean nulas o con vacíos
        df.dropna(subset=[f'{columna}'], inplace=True)

    # Eliminamos todos los datos repetidos:
    df.drop_duplicates(subset=None, keep='first', inplace=True)

    # Crear el directorio de salida
    create_output_directory('files/output')

    # Guardar el DataFrame limpio
    df.to_csv('files/output/solicitudes_de_credito.csv', sep=';', index=False)

pregunta_01()
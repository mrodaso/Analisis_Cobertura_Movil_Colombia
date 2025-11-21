"""
DICCIONARIO DE DATOS - COBERTURA MÓVIL
CAMPO                | TIPO DE DATO | DESCRIPCIÓN
---------------------|--------------|-----------------------------------------------------------------------------------------------------------------------------
ANNO                 | Entero       | Corresponde al año para el cual se reporta la información.
TRIMESTRE            | Entero       | Corresponde al trimestre del año para el cual se reporta la información.
ID_DEPARTAMENTO      | Entero       | Codificación de la DIVIPOLA (DANE) para los departamentos.
DEPARTAMENTO         | Texto        | Nombre del departamento.
ID_MUNICIPIO         | Entero       | Codificación de la DIVIPOLA (DANE) para los municipios.
MUNICIPIO            | Texto        | Nombre del municipio.
ID_CPOB              | Entero       | Codificación de la DIVIPOLA (DANE) para cabeceras municipales y centros poblados.
CPOB                 | Texto        | Nombre de la cabecera municipal o centro poblado.
AREA_CPOB            | Flotante     | Área en km² de la cabecera municipal o centro poblado según el Mapa Geoestadístico Nacional 2023 del DANE.
ID_TECNOLOGIA        | Entero       | Código de tecnología: 2=2G, 3=3G, 4=4G, 5=5G. En zonas sin cobertura el valor es 0.
TECNOLOGIA           | Texto        | Nombre de la tecnología asociada (2G, 3G, 4G, 5G). En zonas sin cobertura el valor es "Ninguna".
NIVEL_SENAL          | Entero       | Nivel de potencia de recepción según la tabla del PRSTM (Circular CRC 156 de 2024). En zonas sin cobertura el valor es 0.
AREA_COB_CLARO       | Flotante     | Área en km² cubierta por CLARO.
AREA_COB_MOVISTAR    | Flotante     | Área en km² cubierta por MOVISTAR.
AREA_COB_TIGO        | Flotante     | Área en km² cubierta por TIGO.
AREA_COB_WOM         | Flotante     | Área en km² cubierta por WOM.
"""

import pandas as pd

# ============================================================================
# CARGA Y LIMPIEZA DE DATOS
# ============================================================================

# Leer base de datos
df = pd.read_csv('./data/Datos_Cobertura Movil_1T_2023 a 4T_2024.csv', sep=';')

# Convertir los tipos de datos de las columnas de área
cols = ['AREA_COB_CLARO', 'AREA_COB_MOVISTAR', 'AREA_COB_TIGO', 'AREA_COB_WOM', 'AREA_CPOB']

df[cols] = (
    df[cols]
    .apply(lambda x: x.str.replace(',', '.', regex=False))  # Reemplaza coma por punto
    .astype(float)  # Convierte a número decimal
)

# Convertir los tipos de datos de las columnas categóricas
df['ANNO'] = df['ANNO'].astype(str)
df['TRIMESTRE'] = df['TRIMESTRE'].astype(str)
df['ID_DEPARTAMENTO'] = df['ID_DEPARTAMENTO'].astype(str)
df['DEPARTAMENTO'] = df['DEPARTAMENTO'].astype(str)
df['ID_MUNICIPIO'] = df['ID_MUNICIPIO'].astype(str)
df['MUNICIPIO'] = df['MUNICIPIO'].astype(str)
df['CPOB'] = df['CPOB'].astype(str)
df['ID_TECNOLOGIA'] = df['ID_TECNOLOGIA'].astype(str)

# ============================================================================
# DATAFRAMES PROCESADOS PARA ANÁLISIS
# ============================================================================

# Columnas de operadores
cols_operadores = ['AREA_COB_CLARO', 'AREA_COB_MOVISTAR', 'AREA_COB_TIGO', 'AREA_COB_WOM']

# --- DataFrame de cobertura por señal ---
df_sennal = (
    df.groupby(['ANNO', 'TRIMESTRE', 'DEPARTAMENTO', 'MUNICIPIO', 'CPOB', 'TECNOLOGIA'], as_index=False)
      [cols_operadores]
      .sum()
)

# --- DataFrame resumen por CPOB y tecnología ---
df_resumen = (
    df.groupby(['ANNO', 'TRIMESTRE', 'DEPARTAMENTO', 'CPOB', 'TECNOLOGIA'], as_index=False)
    .agg({
        'AREA_CPOB': 'first',
        'AREA_COB_CLARO': 'sum',
        'AREA_COB_MOVISTAR': 'sum',
        'AREA_COB_TIGO': 'sum',
        'AREA_COB_WOM': 'sum'
    })
)

# Calcular porcentajes de cobertura por operador
df_resumen['PCT_CLARO'] = (df_resumen['AREA_COB_CLARO'] / df_resumen['AREA_CPOB']) * 100
df_resumen['PCT_MOVISTAR'] = (df_resumen['AREA_COB_MOVISTAR'] / df_resumen['AREA_CPOB']) * 100
df_resumen['PCT_TIGO'] = (df_resumen['AREA_COB_TIGO'] / df_resumen['AREA_CPOB']) * 100
df_resumen['PCT_WOM'] = (df_resumen['AREA_COB_WOM'] / df_resumen['AREA_CPOB']) * 100
df_resumen['PCT_PROMEDIO'] = df_resumen[['PCT_CLARO', 'PCT_MOVISTAR', 'PCT_TIGO', 'PCT_WOM']].mean(axis=1)
df_resumen = df_resumen.round(2)

# --- DataFrame de cobertura general (con/sin internet) ---
total = (
    df[['DEPARTAMENTO', 'CPOB']]
    .drop_duplicates()
    .groupby('DEPARTAMENTO')
    .size()
    .reset_index(name='NUM_CPOB')
)

con_internet = (
    df[df['TECNOLOGIA'].isin(['2G', '3G', '4G', '5G'])]
    [['DEPARTAMENTO', 'CPOB']]
    .drop_duplicates()
    .groupby('DEPARTAMENTO')
    .size()
    .reset_index(name='CPOB_CON_INTERNET')
)

df_final = total.merge(con_internet, on='DEPARTAMENTO', how='left')
df_final['CPOB_SIN_INTERNET'] = df_final['NUM_CPOB'] - df_final['CPOB_CON_INTERNET'].fillna(0)
df_final['%_CON_INTERNET'] = (df_final['CPOB_CON_INTERNET'] / df_final['NUM_CPOB']) * 100
df_final['%_SIN_INTERNET'] = (df_final['CPOB_SIN_INTERNET'] / df_final['NUM_CPOB']) * 100

df_final_sorted = df_final.sort_values(by='CPOB_SIN_INTERNET', ascending=False)

# ============================================================================
# ANÁLISIS ESPECÍFICO PARA EL AÑO 2024 - TRIMESTRE 4
# ============================================================================

# Filtrar datos para el año 2024 y trimestre 4
df_actual = df[(df['ANNO'] == '2024') & (df['TRIMESTRE'] == '4')].copy()

# Agrupar por DEPARTAMENTO, MUNICIPIO, CPOB y TECNOLOGIA y sumar las áreas de cobertura
df_actual = (
    df_actual.groupby(['ANNO', 'TRIMESTRE', 'DEPARTAMENTO', 'MUNICIPIO', 'CPOB', 'TECNOLOGIA'], as_index=False)
    .agg({
        'AREA_CPOB': 'first',  # el área total urbana es la misma
        'AREA_COB_CLARO': 'sum',
        'AREA_COB_MOVISTAR': 'sum',
        'AREA_COB_TIGO': 'sum',
        'AREA_COB_WOM': 'sum'
    })
)

# Calcular el área de cobertura máxima entre los operadores para cada fila
df_actual["AREA_COB_MAX"] = df_actual[["AREA_COB_CLARO", "AREA_COB_MOVISTAR", "AREA_COB_TIGO", "AREA_COB_WOM"]].max(axis=1)

# Identificar de qué operador es ese máximo
df_actual["OPERADOR_MAX"] = (
    df_actual[["AREA_COB_CLARO", "AREA_COB_MOVISTAR", "AREA_COB_TIGO", "AREA_COB_WOM"]]
    .idxmax(axis=1)                       # obtiene el nombre de la columna con el valor máximo
    .str.replace("AREA_COB_", "")          # quita el prefijo
    .str.upper()                           # pone todo en mayúsculas (por estética)
)

# Calcular el máximo y la tecnología correspondiente por cada CPOB
df_max_tecnologia = (
    df_actual.loc[df_actual.groupby(['ANNO', 'TRIMESTRE', 'DEPARTAMENTO', 'MUNICIPIO', 'CPOB'])['AREA_COB_MAX'].idxmax()]
    .copy()
)
# Renombrar la columna para mayor claridad
df_max_tecnologia.rename(columns={'AREA_COB_MAX': 'AREA_COB_MAX_TECNOLOGIAS'}, inplace=True)

# Crear una columna que identifique la tecnología del máximo
df_max_tecnologia['TECNOLOGIA_MAX'] = df_max_tecnologia['TECNOLOGIA']

# Calcular el porcentaje de cobertura del operador con mayor área de cobertura en comparación con el área total del CPOB
df_max_tecnologia['PORCENTAJE_COBERTURA'] = (df_max_tecnologia['AREA_COB_MAX_TECNOLOGIAS'] / df_max_tecnologia['AREA_CPOB']) * 100
df_max_tecnologia = df_max_tecnologia.sort_values(by='PORCENTAJE_COBERTURA', ascending=True)

# --- Análisis por departamento ---
df_departamento = df_max_tecnologia.groupby('DEPARTAMENTO', as_index=False).agg({
    'PORCENTAJE_COBERTURA': 'mean',
    'OPERADOR_MAX': lambda x: x.value_counts().idxmax()
})

# Top 10 con menor y mayor cobertura
top10_menor = df_departamento.sort_values(by='PORCENTAJE_COBERTURA', ascending=True).head(6)
top10_mayor = df_departamento.sort_values(by='PORCENTAJE_COBERTURA', ascending=False).head(6)

# Añadir signo negativo a los de menor cobertura (para gráfico espejo)
top10_menor['PORCENTAJE_COBERTURA'] = -top10_menor['PORCENTAJE_COBERTURA']

# Unir ambos en un solo DataFrame
df_comparativo = pd.concat([top10_menor, top10_mayor])

# --- Conteo por operador predominante ---
conteo_operador = df_max_tecnologia['OPERADOR_MAX'].value_counts()
porcentaje_operador = (conteo_operador / conteo_operador.sum()) * 100

# --- Conteo por tecnología predominante ---
conteo_tecnologia = df_max_tecnologia['TECNOLOGIA_MAX'].value_counts()
porcentaje_tecnologia = (conteo_tecnologia / conteo_tecnologia.sum()) * 100

# --- Operador predominante por municipio ---
df_municipio = (
    df_max_tecnologia
    .groupby(['DEPARTAMENTO', 'MUNICIPIO', 'OPERADOR_MAX'], as_index=False)
    .agg({'AREA_COB_MAX_TECNOLOGIAS': 'sum'})
)

df_municipio_predominante = (
    df_municipio.loc[
        df_municipio.groupby(['DEPARTAMENTO', 'MUNICIPIO'])['AREA_COB_MAX_TECNOLOGIAS'].idxmax()
    ][['DEPARTAMENTO', 'MUNICIPIO', 'OPERADOR_MAX']]
)

# --- Top departamentos por cantidad de registros ---
df_filtrado = df[(df['ANNO'] == '2024') & (df['TRIMESTRE'] == '4')]

# Seleccionar los top departamentos por cantidad de registros
top_deptos = df_filtrado['DEPARTAMENTO'].value_counts().head(30).index
df_top = df_filtrado[df_filtrado['DEPARTAMENTO'].isin(top_deptos)]

# --- Lugares sin cobertura ---
df_sin_tecnologia = df[(df['TECNOLOGIA'] == 'Ninguna')]

df_cuenta_sin_tecnologia = (
    df_sin_tecnologia
    .groupby(['ANNO', 'DEPARTAMENTO'])['CPOB']
    .nunique()
    .reset_index(name='NUM_CPOB_SIN_TEC')
)
df_cuenta_sin_tecnologia = df_cuenta_sin_tecnologia.sort_values(['ANNO', 'NUM_CPOB_SIN_TEC'], ascending=[True, False])

# --- Matriz de correlación ---
cols_num = ['AREA_CPOB', 'AREA_COB_CLARO', 'AREA_COB_MOVISTAR', 'AREA_COB_TIGO', 'AREA_COB_WOM']
corr_matrix = df[cols_num].corr()

# --- Análisis temporal ---
df_temp = (
    df.groupby(["ANNO", "TRIMESTRE", "TECNOLOGIA"], as_index=False)
    .agg({
        "AREA_COB_CLARO": "sum",
        "AREA_COB_MOVISTAR": "sum",
        "AREA_COB_TIGO": "sum",
        "AREA_COB_WOM": "sum"
    })
)

df_temp["PERIODO"] = df_temp["ANNO"].astype(str) + "-T" + df_temp["TRIMESTRE"].astype(str)

# Reorganizar a formato largo
df_long = df_temp.melt(
    id_vars=["PERIODO", "ANNO", "TRIMESTRE", "TECNOLOGIA"],
    value_vars=cols_operadores,
    var_name="OPERADOR",
    value_name="AREA_COBERTURA"
)
df_long["OPERADOR"] = df_long["OPERADOR"].str.replace("AREA_COB_", "", regex=False)

# --- Datos en formato melt para análisis de distribución ---
df_melt = df.melt(
    value_vars=cols_operadores,
    var_name='Operador',
    value_name='Área Cobertura'
)
df_melt['Operador'] = df_melt['Operador'].str.replace("AREA_COB_", "", regex=False)

# ============================================================================
# PROCESAMIENTO PARA MAPAS COROPLÉTICOS
# ============================================================================

import json
from urllib.request import urlopen

# Crear el DataFrame de Cobertura por tecnología 4G
df_resumen_4g = (
    df.groupby(['ANNO', 'TRIMESTRE', 'DEPARTAMENTO', 'CPOB', 'TECNOLOGIA'], as_index=False)
    .agg({
        'AREA_CPOB': 'first',
        'AREA_COB_CLARO': 'sum',
        'AREA_COB_MOVISTAR': 'sum',
        'AREA_COB_TIGO': 'sum',
        'AREA_COB_WOM': 'sum'
    })
)

df_4g = df_resumen_4g[df_resumen_4g['TECNOLOGIA'] == '4G'].copy()

# Calcular porcentajes de cobertura
df_4g['PCT_CLARO'] = (df_4g['AREA_COB_CLARO'] / df_4g['AREA_CPOB']) * 100
df_4g['PCT_MOVISTAR'] = (df_4g['AREA_COB_MOVISTAR'] / df_4g['AREA_CPOB']) * 100
df_4g['PCT_TIGO'] = (df_4g['AREA_COB_TIGO'] / df_4g['AREA_CPOB']) * 100
df_4g['PCT_WOM'] = (df_4g['AREA_COB_WOM'] / df_4g['AREA_CPOB']) * 100

# Ajustar porcentajes mayores a 100
df_4g[['PCT_CLARO', 'PCT_MOVISTAR', 'PCT_TIGO', 'PCT_WOM']] = (
    df_4g[['PCT_CLARO', 'PCT_MOVISTAR', 'PCT_TIGO', 'PCT_WOM']].clip(upper=100)
)

# Crear DataFrame de Cobertura Máxima por Departamento
df_cob_max_cpob_4g = (
    df_4g.groupby(['DEPARTAMENTO', 'CPOB'])[['PCT_CLARO', 'PCT_MOVISTAR', 'PCT_TIGO', 'PCT_WOM']]
    .max()
    .reset_index()
)

# Promedio departamental de los PCT_COB máximos reportados
df_cob_max_depto_4g = (
    df_cob_max_cpob_4g.groupby('DEPARTAMENTO')[['PCT_CLARO', 'PCT_MOVISTAR', 'PCT_TIGO', 'PCT_WOM']]
    .mean()
    .reset_index()
)

# Renombrar columnas
df_cob_max_depto_4g.rename(columns={
    'PCT_CLARO': 'PCT_MAX_PROMEDIO_CLARO',
    'PCT_MOVISTAR': 'PCT_MAX_PROMEDIO_MOVISTAR',
    'PCT_TIGO': 'PCT_MAX_PROMEDIO_TIGO',
    'PCT_WOM': 'PCT_MAX_PROMEDIO_WOM'
}, inplace=True)

# Cargar GeoJSON de Colombia
url_geojson = 'https://gist.githubusercontent.com/john-guerra/43c7656821069d00dcbc/raw/be6a6e239cd5b5b803c6e7c2ec405b793a9064dd/Colombia.geo.json'

try:
    with urlopen(url_geojson) as response:
        counties = json.load(response)
    
    # Mapeo de nombres de departamentos
    mapeo_nombres = {
        'ARCHIPIELAGO DE SAN ANDRES PROVIDENCIA Y SANTA CATALINA': 'SAN ANDRES',
        'SANTAFE DE BOGOTA D.C': 'BOGOTÁ. D.C.',
        'AMAZONAS': 'AMAZONAS',
        'ANTIOQUIA': 'ANTIOQUIA',
        'ARAUCA': 'ARAUCA',
        'ATLANTICO': 'ATLÁNTICO',
        'BOLIVAR': 'BOLÍVAR',
        'BOYACA': 'BOYACÁ',
        'CALDAS': 'CALDAS',
        'CAQUETA': 'CAQUETÁ',
        'CASANARE': 'CASANARE',
        'CAUCA': 'CAUCA',
        'CESAR': 'CESAR',
        'CHOCO': 'CHOCÓ',
        'CORDOBA': 'CÓRDOBA',
        'CUNDINAMARCA': 'CUNDINAMARCA',
        'GUAINIA': 'GUAINÍA',
        'GUAVIARE': 'GUAVIARE',
        'HUILA': 'HUILA',
        'LA GUAJIRA': 'LA GUAJIRA',
        'MAGDALENA': 'MAGDALENA',
        'META': 'META',
        'NARIÑO': 'NARIÑO',
        'NORTE DE SANTANDER': 'NORTE DE SANTANDER',
        'PUTUMAYO': 'PUTUMAYO',
        'QUINDIO': 'QUINDÍO',
        'RISARALDA': 'RISARALDA',
        'SANTANDER': 'SANTANDER',
        'SUCRE': 'SUCRE',
        'TOLIMA': 'TOLIMA',
        'VALLE DEL CAUCA': 'VALLE DEL CAUCA',
        'VAUPES': 'VAUPÉS',
        'VICHADA': 'VICHADA'
    }
    
    # Aplicar mapeo
    for feature in counties['features']:
        nombre_geojson = feature['properties']['NOMBRE_DPT']
        if nombre_geojson in mapeo_nombres:
            feature['properties']['NOMBRE_DPT'] = mapeo_nombres[nombre_geojson]
        feature['id'] = feature['properties']['NOMBRE_DPT']
    
except Exception as e:
    print(f"Error al cargar GeoJSON: {e}")
    counties = None

#VARIABLES 
"""
CAMPO	       TIPO DE DATO	DESCRIPCIÓN
ANNO	        ENTERO	     Corresponde al año para el cual se reporta la información.
TRIMESTRE	    ENTERO	     Corresponde al trimestre del año para el cual se reporta la información.
ID_DEPARTAMENTO	ENTERO	     Corresponde a la Codificación de la División Político Administrativa de Colombia - DIVIPOLA (DANE) para los departamentos.
DEPARTAMENTO	ENTERO	     Nombre del departamento.
ID_MUNICIPIO	ENTERO	     Corresponde a la Codificación de la División Político Administrativa de Colombia - DIVIPOLA (DANE) para los municipios.
MUNICIPIO	    ENTERO	     Nombre del municipio.
ID_CPOB	        ENTERO	     Corresponde a la Codificación de la División Político Administrativa de Colombia - DIVIPOLA (DANE) para la cabecereas municpales y los centros poblados.
CPOB	        ENTERO	     Nombre de la cabecera municipal o centro poblado.
AREA_CPOB	    FLOTANTE	 Corresponde al área de la cabecera municipal o centro poblado o en Km^2, calculada con base en el Mapa Geoestadístico Nacional 2023 del DANE.
ID_TECNOLOGIA	ENTERO	     Corresponde a la tecnología de la cobertura: 2 = 2G, 3 = 3G, 4 = 4G y 5 = 5G. Para las áreas en las cuales no hay cobertura de servicios asociada, el ID_TECNOLOGIA es «0» (cero).
TECNOLOGIA	    TEXTO	     Corresponde a la tecnología (2G, 3G, 4G o 5G) de la cobertura. Para las áreas en las cuales no hay cobertura de servicios asociada, la TECNOLOGÍA es «Ninguna».
NIVEL_SENAL	    ENTERO	     Corresponde al nivel de potencia de recepción reportado por el PRSTM de acuerdo con la tabla 2 «Tabla de códigos de nivel de señal» del instructivo para el reporte de información de mapas de cobertura de redes móviles de la Circular CRC 156 de 2024. Para las áreas en las cuales no hay cobertura de servicios asociada, el NIVEL_SEÑAL es «0» (cero).
AREA_COB_CLARO	FLOTANTE	 Corresponde al área cubierta por CLARO de la cabecera municipal o centro poblado, en Km^2.
AREA_COB_MOVISTAR FLOTANTE   Corresponde al área cubierta por MOVISTAR de la cabecera municipal o centro poblado, en Km^2.
AREA_COB_TIGO	FLOTANTE	 Corresponde al área cubierta por TIGO de la cabecera municipal o centro poblado, en Km^2.
AREA_COB_WOM	FLOTANTE	 Corresponde al área cubierta por WOM de la cabecera municipal o centro poblado, en Km^2.

"""

import pandas as pd

# leer base de datos

df = pd.read_csv('./data/Datos_Cobertura Movil_1T_2023 a 4T_2024.csv', sep=';')
df.info()
# Dimensiones del df
print(df.shape)
# Revisar si hay valores nulos
df.isnull().values.any()
print(df.shape)
# Convertir los tipos de datos de cada variable
cols = ['AREA_COB_CLARO', 'AREA_COB_MOVISTAR', 'AREA_COB_TIGO', 'AREA_COB_WOM','AREA_CPOB']

df[cols] = (
    df[cols]
    .apply(lambda x: x.str.replace(',', '.', regex=False))  # Reemplaza coma por punto
    .astype(float)  # Convierte a número decimal
)

# Convertir los tipos de datos de cada variable
df['ANNO'] = df['ANNO'].astype(str)
df['TRIMESTRE'] = df['TRIMESTRE'].astype(str)
df['ID_DEPARTAMENTO'] = df['ID_DEPARTAMENTO'].astype(str)
df['DEPARTAMENTO'] = df['DEPARTAMENTO'].astype(str)
df['ID_MUNICIPIO'] = df['ID_MUNICIPIO'].astype(str)
df['MUNICIPIO'] = df['MUNICIPIO'].astype(str)
df['CPOB'] = df['CPOB'].astype(str)
df['ID_TECNOLOGIA'] = df['ID_TECNOLOGIA'].astype(str)

df.describe()

df_antioquia = df[df['DEPARTAMENTO'] == 'ANTIOQUIA']
print(df_antioquia['MUNICIPIO'].unique())

# Agrupación del df por nivel de señal
df_sennal = (
    df.groupby(['ANNO', 'TRIMESTRE', 'DEPARTAMENTO', 'MUNICIPIO', 'CPOB', 'TECNOLOGIA'], as_index=False)
      [['AREA_COB_CLARO', 'AREA_COB_MOVISTAR', 'AREA_COB_TIGO', 'AREA_COB_WOM']]
      .sum()
)
# Mostrar df agrupado por señal para CPOB == MEDELLÍN
df_sennal_medellin = df_sennal[df_sennal['CPOB'] == 'MEDELLÍN']
print(df_sennal_medellin)

# Agrupación del df por CPOB
df_cobertura = (
    df.groupby('CPOB', as_index=False)[
        ['AREA_CPOB', 'AREA_COB_CLARO', 'AREA_COB_MOVISTAR', 'AREA_COB_TIGO', 'AREA_COB_WOM']
    ]
    .sum()
)

# Supongamos que tu DataFrame se llama df
df_resumen = (
    df.groupby(['ANNO','TRIMESTRE','CPOB', 'TECNOLOGIA'], as_index=False)
    .agg({
        'AREA_CPOB': 'first',  # el área total urbana es la misma
        'AREA_COB_CLARO': 'sum',
        'AREA_COB_MOVISTAR': 'sum',
        'AREA_COB_TIGO': 'sum',
        'AREA_COB_WOM': 'sum'
        })
)
print(df_resumen)

df_medellin = df_resumen[df_resumen['CPOB'].str.upper() == 'MEDELLÍN']
print(df_medellin)

df_resumen['PCT_CLARO'] = (df_resumen['AREA_COB_CLARO'] / df_resumen['AREA_CPOB']) * 100
df_resumen['PCT_MOVISTAR'] = (df_resumen['AREA_COB_MOVISTAR'] / df_resumen['AREA_CPOB']) * 100
df_resumen['PCT_TIGO'] = (df_resumen['AREA_COB_TIGO'] / df_resumen['AREA_CPOB']) * 100
df_resumen['PCT_WOM'] = (df_resumen['AREA_COB_WOM'] / df_resumen['AREA_CPOB']) * 100

df_resumen = df_resumen.round(2)

print(df_resumen.head())

df_resumen['PCT_PROMEDIO'] = df_resumen[['PCT_CLARO', 'PCT_MOVISTAR', 'PCT_TIGO', 'PCT_WOM']].mean(axis=1)
df_resumen['PCT_PROMEDIO'] = df_resumen['PCT_PROMEDIO'].round(2)

print(df_resumen[['CPOB', 'TECNOLOGIA', 'PCT_CLARO', 'PCT_MOVISTAR', 'PCT_TIGO', 'PCT_WOM', 'PCT_PROMEDIO']].head())

df_menores = df_resumen.nsmallest(10, 'PCT_PROMEDIO')
print(df_menores[['CPOB', 'TECNOLOGIA', 'PCT_CLARO', 'PCT_MOVISTAR', 'PCT_TIGO', 'PCT_WOM', 'PCT_PROMEDIO']])

df_brecha = df[['DEPARTAMENTO', 'CPOB']].drop_duplicates()
print(df_brecha)

total = (
    df[['DEPARTAMENTO', 'CPOB']]
    .drop_duplicates()
    .groupby('DEPARTAMENTO')
    .size()
    .reset_index(name='NUM_CPOB')
)
print(total)

con_internet = (
    df[df['TECNOLOGIA'].isin(['2G', '3G', '4G', '5G'])]
    [['DEPARTAMENTO', 'CPOB']]
    .drop_duplicates()
    .groupby('DEPARTAMENTO')
    .size()
    .reset_index(name='CPOB_CON_INTERNET')
)
print(con_internet)

df_final = total.merge(con_internet, on='DEPARTAMENTO', how='left')
df_final['CPOB_SIN_INTERNET'] = df_final['NUM_CPOB'] - df_final['CPOB_CON_INTERNET'].fillna(0)
df_final['%_CON_INTERNET'] = (df_final['CPOB_CON_INTERNET'] / df_final['NUM_CPOB']) * 100
df_final['%_SIN_INTERNET'] = (df_final['CPOB_SIN_INTERNET'] / df_final['NUM_CPOB']) * 100

print(df_final)

df_corbetura = df_final.sort_values(by='CPOB_SIN_INTERNET', ascending=False)

df_final_sorted = df_final.sort_values(by='CPOB_SIN_INTERNET', ascending=False)

df_melt = df.melt(
    value_vars=['AREA_COB_CLARO', 'AREA_COB_MOVISTAR', 'AREA_COB_TIGO', 'AREA_COB_WOM'],
    var_name='Operador', value_name='Área Cobertura'
)

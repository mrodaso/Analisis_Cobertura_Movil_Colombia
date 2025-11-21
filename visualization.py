# Gráficos de Análisis de Cobertura Móvil

# Importar librerías
import matplotlib.pyplot as plt
import seaborn as sns
from .code import (
    df, df_final_sorted
)

# --- Gráfico 1 ---
plt.figure(figsize=(8, 5))
sns.countplot(data=df, x='TECNOLOGIA', order=df['TECNOLOGIA'].value_counts().index, palette='viridis')
plt.title('Distribución de Registros por Tipo de Tecnología')
plt.xlabel('Tipo de Tecnología')
plt.ylabel('Cantidad de Registros')
plt.xticks(rotation=45)
plt.grid(True, linestyle='--', alpha=0.5)
plt.show()

# --- Gráfico 2 ---
cols = ['AREA_COB_CLARO', 'AREA_COB_MOVISTAR', 'AREA_COB_TIGO', 'AREA_COB_WOM']
plt.figure(figsize=(8, 5))
sns.boxplot(data=df[cols])
plt.title('Distribución del Área de Cobertura por Operador')
plt.xlabel('Operador')
plt.ylabel('Área de Cobertura')
plt.grid(True, linestyle='--', alpha=0.6)
plt.show()

# --- Gráfico 3: Departamentos con mayor cantidad de CPOB sin Internet ---
plt.figure(figsize=(12,6))
plt.bar(df_final_sorted['DEPARTAMENTO'], df_final_sorted['CPOB_SIN_INTERNET'], color='tomato')
plt.title('Departamentos con mayor cantidad de CPOB sin Internet', fontsize=14)
plt.xlabel('Departamento', fontsize=12)
plt.ylabel('Número de CPOB sin Internet', fontsize=12)
plt.xticks(rotation=90)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.show()



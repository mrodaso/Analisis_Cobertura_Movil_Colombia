# Dashboard de Cobertura Móvil Colombia

Dashboard interactivo desarrollado con Streamlit para analizar la cobertura móvil en Colombia por departamento, operador y tecnología.

Enlace de la página puesta en producción: https://drc28rkqizznwntfjdzxed.streamlit.app/

## 📋 Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

## 🚀 Instalación y Ejecución

### 1. Clonar o descargar el proyecto

```bash
cd dashboard
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

Las dependencias incluyen:
- `streamlit`: Framework para crear la aplicación web
- `pandas`: Procesamiento y análisis de datos
- `plotly`: Visualizaciones interactivas

### 3. Ejecutar el dashboard

```bash
python -m streamlit run app.py
```

El dashboard se abrirá automáticamente en tu navegador en `http://localhost:8501`

## 📁 Estructura del Proyecto

```
dashboard/
├── app.py                          # Aplicación principal
├── requirements.txt                # Dependencias del proyecto
├── README.md                       # Este archivo
├── components/                     # Componentes reutilizables
│   ├── header.py                  # Encabezado con navegación
│   ├── footer.py                  # Pie de página
│   ├── sidebar.py                 # Barra lateral con filtros
│   ├── stat_card.py               # Tarjetas de estadísticas
│   └── grafico_generico.py        # Componente para gráficos
├── css/
│   └── styles.css                 # Estilos personalizados
├── dashboard_code/
│   └── read_csv.py                # Carga y procesamiento de datos
└── data/
    └── Datos_Cobertura Movil_1T_2023 a 4T_2024.csv
```

## 🎯 Características

### Filtros Interactivos
- **Año**: Filtrar datos por año específico
- **Trimestre**: Seleccionar trimestre del año
- **Departamentos**: Filtrar por uno o múltiples departamentos
- **Tecnologías**: Seleccionar tecnologías móviles (2G, 3G, 4G, 5G)

### Visualizaciones

1. **Estadísticas Generales**
   - Total de registros en el dataset
   - Número de departamentos analizados
   - Cantidad de centros poblados (CPOB)

2. **Gráficos de Análisis**
   - Distribución de tecnologías por departamento
   - Área de cobertura por operador
   - Tecnología predominante por CPOB
   - Predominancia de operadores
   - Departamentos sin cobertura móvil
   - Mapa de correlación entre variables
   - Top 10 departamentos sin cobertura
   - Evolución temporal por operador y tecnología
   - Mapas coropléticos de cobertura 4G

### Navegación
- Header con anclas para navegación rápida
- Botón flotante "Volver arriba" para facilitar el desplazamiento

## 📊 Datos

Los datos analizan la cobertura móvil en Colombia desde el primer trimestre de 2023 hasta el cuarto trimestre de 2024, incluyendo:

- **Operadores**: CLARO, MOVISTAR, TIGO, WOM
- **Tecnologías**: 2G, 3G, 4G, 5G
- **Cobertura geográfica**: Todos los departamentos de Colombia
- **Métricas**: Área de cobertura (km²), centros poblados, porcentajes

## 🛠️ Desarrollo

### Modificar estilos

Los estilos CSS se encuentran en `css/styles.css`. 

### Agregar nuevos gráficos

Utiliza el componente `grafico_generico()` en `components/grafico_generico.py` que soporta múltiples tipos de gráficos:
- bar, histogram, line, pie, scatter, area, heatmap, choropleth

### Estructura de datos

El procesamiento de datos se realiza en `dashboard_code/read_csv.py`. Aquí se definen:
- Limpieza de datos
- Transformaciones
- Dataframes procesados para análisis

## 🎨 Personalización

### Colores por operador
```python
COLOR_OPERADORES = {
    'CLARO': '#ED1B24',
    'MOVISTAR': '#66CD00',
    'TIGO': '#001EB4',
    'WOM': '#6F1A7F'
}
```

### Colores por tecnología
```python
COLOR_TECNOLOGIAS = {
    '2G': '#ef4444',
    '3G': '#f97316',
    '4G': '#22c55e',
    '5G': '#3b82f6'
}
```

## 📝 Notas

- Los filtros se aplican en tiempo real a todas las visualizaciones
- El dashboard es completamente responsive
- Los gráficos son interactivos (zoom, pan, hover)
- Incluye efectos visuales modernos con glassmorphism

## 👩‍💻 Desarrollado por

**Marisol Rodas** - 2025

---

Para soporte o consultas, revisa la documentación de:
- [Streamlit](https://docs.streamlit.io/)
- [Plotly](https://plotly.com/python/)
- [Pandas](https://pandas.pydata.org/docs/)

import streamlit as st

def render_sidebar(df):
	"""
	Renderiza el sidebar con filtros interactivos.
	
	Parámetros:
	- df: DataFrame con los datos completos
	
	Retorna:
	- dict con los filtros seleccionados: {
		'ano': str,
		'trimestre': str,
		'departamentos': list,
		'tecnologias': list
	}
	"""
	with st.sidebar:
		st.markdown("### Filtros de Datos")
		st.markdown("---")
		
		# Filtro de Año
		anos_disponibles = sorted(df['ANNO'].unique())
		ano_seleccionado = st.selectbox(
			"Año",
			options=["Todos"] + anos_disponibles,
			index=0
		)
		
		# Filtro de Trimestre
		trimestres_disponibles = sorted(df['TRIMESTRE'].unique())
		trimestre_seleccionado = st.selectbox(
			"Trimestre",
			options=["Todos"] + trimestres_disponibles,
			index=0
		)
		
		st.markdown("---")
		
		# Filtro de Departamento
		departamentos_disponibles = sorted(df['DEPARTAMENTO'].unique())
		departamento_seleccionado = st.multiselect(
			"Departamentos",
			options=departamentos_disponibles,
			default=None,
			placeholder="Seleccionar departamentos..."
		)
		
		# Filtro de Tecnología
		tecnologias_disponibles = [t for t in df['TECNOLOGIA'].unique() if t != 'Ninguna']
		tecnologia_seleccionada = st.multiselect(
			"Tecnologías",
			options=tecnologias_disponibles,
			default=tecnologias_disponibles,
			placeholder="Seleccionar tecnologías..."
		)
		
		st.markdown("---")
		st.markdown("""
			<div style='font-size: 0.85rem; color: #666; text-align: center;'>
				<p><strong>Última actualización:</strong><br/>4T 2024</p>
			</div>
		""", unsafe_allow_html=True)
	
	return {
		'ano': ano_seleccionado,
		'trimestre': trimestre_seleccionado,
		'departamentos': departamento_seleccionado,
		'tecnologias': tecnologia_seleccionada
	}

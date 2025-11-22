import streamlit as st
from pathlib import Path
import sys
import pandas as pd
import plotly.graph_objects as go

sys.path.insert(0, str(Path(__file__).resolve().parent))

from dashboard_code.read_csv import (
	df, df_final_sorted, conteo_operador, conteo_tecnologia, porcentaje_tecnologia,
	df_top, corr_matrix, df_cob_max_depto_4g, counties, df_comparativo
)
from components.header import render_header
from components.footer import render_footer
from components.stat_card import stat_card
from components.sidebar import render_sidebar
from components.grafico_generico import grafico_generico

# Colores por operador y tecnología
COLOR_OPERADORES = {
    'CLARO': '#ED1B24',
    'MOVISTAR': '#66CD00',
    'TIGO': '#001EB4',
    'WOM': '#6F1A7F',
    'OTRO': '#949494'
}

COLOR_TECNOLOGIAS = {
    '2G': '#ef4444',
    '3G': '#f97316',
    '4G': '#22c55e',
    '5G': '#3b82f6',
    'Ninguna': '#6b7280'
}

def load_css():
	css_path = Path(__file__).resolve().parent / "css" / "styles.css"
	if css_path.exists():
		st.markdown(f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)


def main():
	st.set_page_config(page_title="Dashboard Cobertura Móvil Colombia", layout="wide")
	load_css()
	
	# Renderizar sidebar y obtener filtros
	filtros = render_sidebar(df)
	ano_seleccionado = filtros['ano']
	trimestre_seleccionado = filtros['trimestre']
	departamento_seleccionado = filtros['departamentos']
	tecnologia_seleccionada = filtros['tecnologias']

	st.markdown('<div id="header"></div>', unsafe_allow_html=True)
	render_header()
	
	# Aplicar filtros a los datos
	df_filtrado_base = df.copy()
	
	if ano_seleccionado != "Todos":
		df_filtrado_base = df_filtrado_base[df_filtrado_base['ANNO'] == ano_seleccionado]
	
	if trimestre_seleccionado != "Todos":
		df_filtrado_base = df_filtrado_base[df_filtrado_base['TRIMESTRE'] == trimestre_seleccionado]
	
	if departamento_seleccionado:
		df_filtrado_base = df_filtrado_base[df_filtrado_base['DEPARTAMENTO'].isin(departamento_seleccionado)]
	
	# Recalcular estadísticas con los datos filtrados
	if len(df_filtrado_base) > 0:
		total_filtrado = (
			df_filtrado_base[['DEPARTAMENTO', 'CPOB']]
			.drop_duplicates()
			.groupby('DEPARTAMENTO')
			.size()
			.reset_index(name='NUM_CPOB')
		)
		
		con_internet_filtrado = (
			df_filtrado_base[df_filtrado_base['TECNOLOGIA'].isin(['2G', '3G', '4G', '5G'])]
			[['DEPARTAMENTO', 'CPOB']]
			.drop_duplicates()
			.groupby('DEPARTAMENTO')
			.size()
			.reset_index(name='CPOB_CON_INTERNET')
		)
		
		df_final_filtrado = total_filtrado.merge(con_internet_filtrado, on='DEPARTAMENTO', how='left')
		df_final_filtrado['CPOB_SIN_INTERNET'] = df_final_filtrado['NUM_CPOB'] - df_final_filtrado['CPOB_CON_INTERNET'].fillna(0)
		df_final_filtrado = df_final_filtrado.sort_values(by='CPOB_SIN_INTERNET', ascending=False)
	else:
		df_final_filtrado = df_final_sorted
		st.warning("No hay datos disponibles con los filtros seleccionados")
	
	df_filtrado = df_filtrado_base.copy()
	if tecnologia_seleccionada:
		df_filtrado = df_filtrado[df_filtrado['TECNOLOGIA'].isin(tecnologia_seleccionada)]
	st.markdown('<div id="statistics"></div>', unsafe_allow_html=True)
	
	# Calcular métricas
	total_registros = len(df_filtrado)
	total_departamentos = df_filtrado['DEPARTAMENTO'].nunique()
	total_cpob = df_filtrado['CPOB'].nunique()
	
	st.markdown('<div style="margin-bottom: 2rem;"></div>', unsafe_allow_html=True)
    # foto encabezado referencia 
	# Grid Bento - Stats superiores
	cols = st.columns([2, 1, 1], gap="medium")
	with cols[0]:
		stat_card("Total Registros", f"{total_registros:,}", "Registros en el dataset", trend="up", trend_value="", trend_color="#22c55e")
	with cols[1]:
		stat_card("Departamentos", f"{total_departamentos}", "Departamentos analizados", trend="up", trend_value="", trend_color="#3b82f6")
	with cols[2]:
		stat_card("CPOB", f"{total_cpob:,}", "Centros poblados", trend="up", trend_value="", trend_color="#22c55e")

	# Card de atribución de datos (alineada y con acordeón para ver primeros 10 registros)


	st.markdown('<div style="margin: 0rem 0 2rem 0;"></div>', unsafe_allow_html=True)
	st.markdown('<div id="charts"></div>', unsafe_allow_html=True)
	tabla_html = df.head(100).to_html(index=False, border=0, classes='df-table')

	st.markdown(
			f"""
			<div style="width:100%; margin:0.75rem 0 1.5rem 0; padding:14px 20px; background:#ffffff; border:1px solid #e6e6e6; border-radius:10px; box-shadow:0 6px 18px rgba(0,0,0,0.06); color:#444; font-size:14px;">
			  <div style="font-weight:600;">Conjunto de datos obtenidos del Portal de Datos Abiertos del Gobierno Nacional de Colombia</div>
			  <div style="font-size:12px; color:#666; margin-bottom:8px;">Disponible en: https://www.datos.gov.co/dataset/Cobertura-de-servicios-m-viles/hid4-zp69/about_data</div>
			  <details style="margin-top:8px; text-align:left;">
			    <summary style="cursor:pointer; font-weight:600;">Ver conjunto de datos completo</summary>
			    <div style="margin-top:10px; overflow:auto; max-height:340px;">
			      <style>
			        .df-table {{ width:100%; border-collapse:collapse; font-size:13px; }}
			        .df-table th, .df-table td {{ padding:6px 8px; border:1px solid #e6e6e6; text-align:left; }}
			        .df-table thead {{ background:#f6f6f6; font-weight:600; }}
			      </style>
			      {tabla_html}
			    </div>
			  </details>
			</div>
			""",
			unsafe_allow_html=True
		)
	# --- GRÁFICO 1: Distribución de Tecnologías en Top Departamentos ---
	def preprocesar_top_departamentos(datos):
		df_top_filtrado = datos[datos['DEPARTAMENTO'].isin(df_top['DEPARTAMENTO'].unique())]
		# Aplicar filtro de tecnologías si está seleccionado
		if tecnologia_seleccionada:
			df_top_filtrado = df_top_filtrado[df_top_filtrado['TECNOLOGIA'].isin(tecnologia_seleccionada)]
		return df_top_filtrado.groupby(['DEPARTAMENTO', 'TECNOLOGIA']).size().reset_index(name='CANTIDAD')
	
	grafico_generico(
		tipo="bar",
		datos=df_filtrado,
		titulo="                                                      Distribución de Tecnologías por Departamento",
		x="DEPARTAMENTO",
		y="CANTIDAD",
		color="TECNOLOGIA",
		labels={'CANTIDAD': 'Cantidad de Registros', 'DEPARTAMENTO': 'Departamento'},
		color_discrete_map=COLOR_TECNOLOGIAS,
		height=600,
		preprocesar=preprocesar_top_departamentos,
		key="grafico_1_tecnologias",
		layout_updates={
			'xaxis_tickangle': -45,
			'margin': dict(l=60, r=60, t=80, b=120),
			'xaxis': dict(tickfont=dict(size=11)),
			'yaxis': dict(tickfont=dict(size=11)),
			'legend': {
			'orientation': "h",
			'yanchor': "bottom",
			'y': -0.4,
			'xanchor': "center",
			'x': 0.5,
			'itemwidth': 70,
			'title': {'side': 'left'}
		}
		}
	)
	
	# --- GRÁFICO 2 y 3: Layout Bento ---
	st.markdown('<div id="operadores"></div>', unsafe_allow_html=True)
	col1, col2 = st.columns([2, 3], gap="medium")
	
	with col1:
		def preprocesar_operadores(datos):
			df_agg = pd.DataFrame({
				'OPERADOR': ['CLARO', 'MOVISTAR', 'TIGO', 'WOM'],
				'AREA_TOTAL': [
					datos['AREA_COB_CLARO'].sum(),
					datos['AREA_COB_MOVISTAR'].sum(),
					datos['AREA_COB_TIGO'].sum(),
					datos['AREA_COB_WOM'].sum()
				]
			})
			return df_agg
		
		grafico_generico(
			tipo="bar",
			datos=df_filtrado,
			titulo="<br> Área Total de Cobertura por Operador",
			x="OPERADOR",
		y="AREA_TOTAL",
			labels={"AREA_TOTAL": "Área Total (km²)", "OPERADOR": "Operador"},
			preprocesar=preprocesar_operadores,
			height=610,
		key="grafico_operadores",
		color_discrete_map=COLOR_OPERADORES
	)
	
	with col2:
		# Usar conteo_tecnologia que ya tiene las tecnologías predominantes por CPOB
		df_tech_temp = pd.DataFrame({
			'TECNOLOGIA': conteo_tecnologia.index,
			'CANTIDAD': conteo_tecnologia.values,
			'PORCENTAJE': porcentaje_tecnologia.values.round(1)
		})
		
		grafico_generico(
            tipo="bar",
            datos=df_tech_temp,
            titulo="<br> Número de CPOB por Tecnología Predominante",
            x="TECNOLOGIA",
            y="CANTIDAD",
            # quitar color="TECNOLOGIA" para evitar barras duplicadas/desplazadas
            text="CANTIDAD",
            color_discrete_map=COLOR_TECNOLOGIAS,
            height=610,
            key="grafico_3_cpob_tecnologia",
            custom_data=['PORCENTAJE'],
            trace_updates={
                'texttemplate': '%{text}<br>(%{customdata[0]:.1f}%)',
                'textposition': 'outside',
                'textfont': dict(size=12, color='black')
            },
            layout_updates={
                'margin': dict(l=60, r=60, t=80, b=60),
                'xaxis': dict(tickfont=dict(size=11)),
                'yaxis': dict(tickfont=dict(size=11)),
                'showlegend': False
            }
        )
	
	# --- GRÁFICO 4 y 5: Layout Bento ---
	st.markdown('<div id="cobertura"></div>', unsafe_allow_html=True)
	col_a, col_b = st.columns([2, 3], gap="medium")
	
	with col_a:
		# --- GRÁFICO 4: Porcentaje de Predominancia por Operador ---
		# Usar df_max_tecnologia que ya tiene el operador predominante por CPOB
		conteo_operador_data = pd.DataFrame({
			'OPERADOR': conteo_operador.index,
			'CANTIDAD': conteo_operador.values
		})
		
		grafico_generico(
			tipo="pie",
			datos=conteo_operador_data,
			titulo="           Porcentaje de Predominancia<br>                  por Operador (CPOB)",
			x="OPERADOR",
			y="CANTIDAD",
			height=550,
			key="grafico_5_operador_predominancia",
			hole=0.3,
			color_discrete_map=COLOR_OPERADORES,
			layout_updates={
				'margin': dict(l=80, r=80, t=80, b=60),
				'showlegend': True,
				'legend': dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5),
				'title': {
					'text': "Porcentaje de Predominancia<br>por Operador (CPOB)",
					'x': 0.5,
					'xanchor': 'center',
					'yanchor': 'top',
					'font': {'size': 16}
				}
			},
			trace_updates={
				'textinfo': 'label+percent',
				'textposition': 'outside',
				'textfont': dict(size=13, color='black'),
				'domain': {'x': [0.05, 0.95], 'y': [0.05, 0.95]}  # <-- reduce tamaño
			}
		)
	
	with col_b:
		# --- GRÁFICO 5: Departamentos sin Cobertura ---
		def preprocesar_sin_cobertura(datos):
			# Recalcular con datos filtrados
			df_sin_tec = datos[datos['TECNOLOGIA'] == 'Ninguna'].groupby(['ANNO', 'DEPARTAMENTO'])['CPOB'].nunique().reset_index(name='NUM_CPOB_SIN_TEC')
			return df_sin_tec.nlargest(20, 'NUM_CPOB_SIN_TEC')
		
		grafico_generico(
			tipo="bar",
			datos=df_filtrado_base,
			titulo="Departamentos con Más Cabeceras sin Cobertura Móvil",
			x="DEPARTAMENTO",
			y="NUM_CPOB_SIN_TEC",
			color="ANNO",
			labels={'NUM_CPOB_SIN_TEC': 'Número de Poblados sin Tecnología', 'DEPARTAMENTO': 'Departamento'},
			height=550,
			barmode="group",
			preprocesar=preprocesar_sin_cobertura,
			key="grafico_6_sin_cobertura",
			layout_updates={
				'xaxis_tickangle': -45,
				'margin': dict(l=80, r=80, t=100, b=150),
				'xaxis': dict(
					tickfont=dict(size=10),
					tickmode='linear',
					automargin=True
				),
				'yaxis': dict(tickfont=dict(size=11)),
				'legend': dict(
					title=dict(text='Año', font=dict(size=12)),
					orientation="h",
					yanchor="bottom",
					y=-0.35,
					xanchor="center",
					x=0.5,
					font=dict(size=11)
				)
			}
		)	# --- GRÁFICO 6 y 8: Layout Bento ---
	col_x, col_y = st.columns([1, 1], gap="medium")
	
	with col_x:
		# --- GRÁFICO 6: Mapa de Correlación ---
		# Usar corr_matrix precalculada que incluye AREA_CPOB y las 4 áreas de operadores
		grafico_generico(
			tipo="heatmap",
		datos=corr_matrix,
		titulo="     Mapa de Correlación entre Áreas de Cobertura",
		height=550,
		key="grafico_7_correlacion",
			text_auto='.2f',
			color_continuous_scale='RdBu_r',
			layout_updates={
				'margin': dict(l=100, r=100, t=80, b=80),
				'xaxis': dict(tickfont=dict(size=11)),
				'yaxis': dict(tickfont=dict(size=11))
			},
			trace_updates={
				'textfont': dict(size=11)
			}
		)
	
	with col_y:
		# --- GRÁFICO 8: Top 10 Cabeceras sin Cobertura ---
		def preprocesar_top10_sin_cobertura(datos):
			return df_final_filtrado.nlargest(10, 'CPOB_SIN_INTERNET')
		
		grafico_generico(
			tipo="bar",
			datos=df_final_filtrado,
			titulo="          Top 10 Departamentos con Más Cabeceras<br>                             sin Cobertura Móvil",
			x="DEPARTAMENTO",
		y="CPOB_SIN_INTERNET",
		color="CPOB_SIN_INTERNET",
		labels={'CPOB_SIN_INTERNET': '# CPOB sin Internet'},
		height=550,
		preprocesar=preprocesar_top10_sin_cobertura,
			key="grafico_9_top10_sin_cobertura",
			color_continuous_scale='Reds',
			layout_updates={
				'xaxis_tickangle': -45,
				'margin': dict(l=60, r=60, t=80, b=120),
				'xaxis': dict(tickfont=dict(size=11)),
				'yaxis': dict(tickfont=dict(size=11))
			}
		)
	
	# --- GRÁFICO 7: Evolución Temporal con Tabs por Operador ---
	st.markdown('<div id="evolucion"></div>', unsafe_allow_html=True)
	tab1, tab2, tab3, tab4 = st.tabs(["CLARO", "MOVISTAR", "TIGO", "WOM"])
	
	operadores_tabs = ["CLARO", "MOVISTAR", "TIGO", "WOM"]
	tabs = [tab1, tab2, tab3, tab4]
	
	for tab, operador in zip(tabs, operadores_tabs):
		with tab:
			def preprocesar_operador_temporal(datos):
				# Recalcular con datos filtrados
				df_grouped = datos.groupby(['ANNO', 'TRIMESTRE', 'TECNOLOGIA']).agg({
					f'AREA_COB_{operador}': 'sum'
				}).reset_index()
				df_grouped['PERIODO'] = df_grouped['ANNO'] + '-T' + df_grouped['TRIMESTRE']
				df_grouped['OPERADOR'] = operador
				df_grouped['AREA_COBERTURA'] = df_grouped[f'AREA_COB_{operador}']
				return df_grouped[['PERIODO', 'TECNOLOGIA', 'OPERADOR', 'AREA_COBERTURA']]
			
			grafico_generico(
				tipo="line",
				datos=df_filtrado_base,
				titulo=f'Evolución Temporal de {operador} por Tecnología',
				x='PERIODO',
				y='AREA_COBERTURA',
				color='TECNOLOGIA',
			labels={'AREA_COBERTURA': 'Área de Cobertura (km²)', 'PERIODO': 'Periodo'},
			color_discrete_map=COLOR_TECNOLOGIAS,
			height=550,
			markers=True,
				preprocesar=preprocesar_operador_temporal,
				key=f"grafico_8_{operador.lower()}_temporal",
				layout_updates={
					'margin': dict(l=60, r=60, t=80, b=80),
					'font': dict(size=11),
					'xaxis': dict(tickangle=-45, tickfont=dict(size=10)),
					'yaxis': dict(tickfont=dict(size=10)),
					'legend': dict(orientation="h", yanchor="bottom", y=-0.25, xanchor="center", x=0.5)
				}
			)
	
	# --- GRÁFICO 9: Mapas Coropléticos de Cobertura 4G por Operador ---
	st.markdown('<div id="mapas"></div>', unsafe_allow_html=True)
	if counties is not None:
		tab_claro, tab_movistar, tab_tigo, tab_wom = st.tabs(["CLARO", "MOVISTAR", "TIGO", "WOM"])
		
		operadores_mapa = [
			("CLARO", "PCT_MAX_PROMEDIO_CLARO", tab_claro, COLOR_OPERADORES['CLARO']),
			("MOVISTAR", "PCT_MAX_PROMEDIO_MOVISTAR", tab_movistar, COLOR_OPERADORES['MOVISTAR']),
			("TIGO", "PCT_MAX_PROMEDIO_TIGO", tab_tigo, COLOR_OPERADORES['TIGO']),
			("WOM", "PCT_MAX_PROMEDIO_WOM", tab_wom, COLOR_OPERADORES['WOM'])
		]
		
		for operador, columna, tab, color in operadores_mapa:
			with tab:
				grafico_generico(
					tipo="choropleth",
					datos=df_cob_max_depto_4g,
					titulo=f"Cobertura 4G Máxima Promedio de {operador}",
					height=700,
					key=f"grafico_10_mapa_{operador.lower()}",
					geojson=counties,
					locations=df_cob_max_depto_4g['DEPARTAMENTO'],
					z=df_cob_max_depto_4g[columna],
					colorscale='Viridis',
					colorbar_title='Cobertura (%)',
					mapbox_center={"lat": 4.570868, "lon": -74.2973328},
					mapbox_zoom=4.2,
					hover_template='<b>%{location}</b><br>Cobertura: %{z:.1f}%<extra></extra>',
					layout_updates={
						'margin': dict(l=0, r=0, t=60, b=0),
						'title': {
							'text': f"Cobertura 4G Máxima Promedio de {operador}",
							'x': 0.5,
							'xanchor': 'center',
							'yanchor': 'top',
							'font': {'size': 18, 'color': color}
						}
					}
				)

	# --- GRÁFICO COMPARATIVO: Departamentos con mayor y menor cobertura (Plotly horizontal bars)
	# Se muestra justo después de los mapas coropléticos
	st.markdown('<div id="comparativo"></div>', unsafe_allow_html=True)
	try:
		# Preparar orden y categorías
		categorias = list(df_comparativo['DEPARTAMENTO'])

		fig = go.Figure()
		operadores = df_comparativo['OPERADOR_MAX'].unique()
		# Añadir una traza por operador para generar leyenda automática
		for op in operadores:
			sub = df_comparativo[df_comparativo['OPERADOR_MAX'] == op]
			if sub.empty:
				continue
			fig.add_trace(go.Bar(
				x=sub['PORCENTAJE_COBERTURA'],
				y=sub['DEPARTAMENTO'],
				orientation='h',
				name=op,
				marker_color=COLOR_OPERADORES.get(op, COLOR_OPERADORES['OTRO']),
				text=[f"{abs(v):.1f}%" for v in sub['PORCENTAJE_COBERTURA']],
				textposition='outside',
				hovertemplate='<b>%{y}</b><br>Porcentaje: %{x:.1f}%<extra></extra>'
			))

		# Forzar orden de las categorías en el eje Y
		fig.update_yaxes(categoryorder='array', categoryarray=categorias)

		# Línea vertical en 0
		fig.add_vline(x=0, line_width=1, line_color='black')

		# Layout
		fig.update_layout(
			title=dict(text='Departamentos con mayor y menor cobertura móvil promedio (2024)', x=0.5, xanchor='center'),
			xaxis_title='Porcentaje de cobertura promedio (%)',
			yaxis_title='Departamento',
			height=600,
			margin=dict(l=200, r=80, t=100, b=80),
			legend_title_text='Operador predominante'
		)

		# Usar el componente genérico para renderizar y forzar la leyenda de CLARO abajo a la derecha
		grafico_generico(
			tipo='custom',
			datos=df_comparativo,
			fig=fig,
			key='grafico_10_comparativo',
			force_legend=[{'name': 'CLARO', 'color': COLOR_OPERADORES.get('CLARO', '#ED1B24')}],
			height=600
		)
	except Exception as e:
		st.warning(f"No se pudo generar el gráfico comparativo (Plotly): {e}")
		
	st.markdown('<div id="footer"></div>', unsafe_allow_html=True)
	
 
		# Imagen de Colombia por Operador al final
	st.markdown('<div style="margin: 3rem 0 2rem 0;"></div>', unsafe_allow_html=True)
	col_center = st.columns([1, 2, 1])
	with col_center[1]:
		st.markdown('<h3 style="text-align: center; margin-bottom: 1.5rem;">Mapa de Cobertura por Operador</h3>', unsafe_allow_html=True)
		try:
			st.image("assets/colombia_por_oderador.png", width=1000, use_container_width=False)
		except Exception as e:
			st.warning(f"No se pudo cargar la imagen: {e}")
	
	# Botón Scroll to Top
	st.markdown("""
		<a href="#header" class="scroll-to-top" title="Volver arriba">
			<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
				<polyline points="18 15 12 9 6 15"></polyline>
			</svg>
		</a>
	""", unsafe_allow_html=True)
	
	render_footer()
    
if __name__ == "__main__":
	main()


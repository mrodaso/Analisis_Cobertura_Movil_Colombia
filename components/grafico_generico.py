import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

def grafico_generico(
	tipo="bar",
	datos=None,
	titulo=None,
	x=None,
	y=None,
	color=None,
	labels=None,
	template="plotly_white",
	width='stretch',
	key=None,
	category_orders=None,
	preprocesar=None,
	height=None,
	orientation=None,
	barmode=None,
	text=None,
	hover_template=None,
	**kwargs
):
	"""
	Componente genérico para crear gráficos con Plotly.
	
	Parámetros:
	- tipo: str - Tipo de gráfico ('bar', 'histogram', 'line', 'pie', 'scatter', 'area', 'heatmap', 'choropleth', 'custom')
	- datos: DataFrame - Datos para el gráfico
	- titulo: str - Título del gráfico
	- x: str - Columna para el eje X
	- y: str - Columna para el eje Y
	- color: str - Columna para colorear
	- labels: dict - Etiquetas personalizadas para ejes
	- template: str - Tema de Plotly
	- width: str - Ancho del gráfico ('stretch' o 'content')
	- key: str - Key único para el gráfico
	- category_orders: dict - Orden de categorías
	- preprocesar: function - Función para preprocesar los datos
	- height: int - Altura del gráfico en píxeles
	- orientation: str - Orientación del gráfico ('h' para horizontal, 'v' para vertical)
	- barmode: str - Modo de barras ('group', 'stack', etc.)
	- text: str - Columna para mostrar como texto en el gráfico
	- hover_template: str - Template personalizado para el hover
	- **kwargs: Argumentos adicionales para el gráfico específico
	"""
	
	if datos is None:
		st.warning("No se proporcionaron datos para el gráfico")
		return
	
	# Preprocesar datos si se proporciona una función
	if preprocesar:
		datos = preprocesar(datos)
	
	# Extraer layout_updates y trace_updates antes de crear el gráfico
	layout_updates = kwargs.pop('layout_updates', {})
	trace_updates = kwargs.pop('trace_updates', {})
	
	# Crear el gráfico según el tipo
	fig = None
	
	if tipo == "bar":
		# Extraer color_discrete_map de kwargs si existe
		color_discrete_map = kwargs.pop('color_discrete_map', None)
		
		# Si no se especifica color pero hay color_discrete_map, usar x como color
		if color_discrete_map and not color:
			color = x
		
		fig = px.bar(
			datos, 
			x=x, 
			y=y, 
			color=color, 
			labels=labels or {}, 
			template=template,
			category_orders=category_orders,
			color_discrete_map=color_discrete_map,
			orientation=orientation,
			barmode=barmode,
			text=text,
			**kwargs
		)
	
	elif tipo == "histogram":
		fig = px.histogram(
			datos,
			x=x,
			color=color,
			category_orders=category_orders,
			template=template,
			**kwargs
		)
	
	elif tipo == "line":
		markers = kwargs.pop('markers', False)
		fig = px.line(
			datos,
			x=x,
			y=y,
			color=color,
			labels=labels or {},
			template=template,
			markers=markers,
			**kwargs
		)
	
	elif tipo == "pie":
			hole = kwargs.pop('hole', 0)
			# Extraer color_discrete_map si se proporcionó
			color_discrete_map = kwargs.pop('color_discrete_map', None)
			# Si hay un mapa de colores pero no se especificó 'color', usar 'x' como color
			if color_discrete_map and not color:
				color = x
			fig = px.pie(
				datos,
				values=y,
				names=x,
				color=color,
				color_discrete_map=color_discrete_map,
				template=template,
				hole=hole,
				**kwargs
			)
	
	elif tipo == "scatter":
		fig = px.scatter(
			datos,
			x=x,
			y=y,
			color=color,
			labels=labels or {},
			template=template,
			**kwargs
		)
	
	elif tipo == "area":
		fig = px.area(
			datos,
			x=x,
			y=y,
			color=color,
			labels=labels or {},
			template=template,
			**kwargs
		)
	
	elif tipo == "heatmap":
		text_auto = kwargs.pop('text_auto', True)
		color_continuous_scale = kwargs.pop('color_continuous_scale', 'RdBu_r')
		fig = px.imshow(
			datos,
			text_auto=text_auto,
			color_continuous_scale=color_continuous_scale,
			aspect='auto',
			labels=labels or {},
			**kwargs
		)
	
	elif tipo == "choropleth":
		# Tipo especial para mapas coropléticos
		geojson = kwargs.pop('geojson', None)
		locations = kwargs.pop('locations', None)
		z = kwargs.pop('z', None)
		colorscale = kwargs.pop('colorscale', 'Viridis')
		colorbar_title = kwargs.pop('colorbar_title', '')
		mapbox_center = kwargs.pop('mapbox_center', {"lat": 4.570868, "lon": -74.2973328})
		mapbox_zoom = kwargs.pop('mapbox_zoom', 4.2)
		
		fig = go.Figure(go.Choroplethmapbox(
			geojson=geojson,
			locations=locations,
			z=z,
			colorscale=colorscale,
			colorbar_title=colorbar_title,
			marker_line_width=1,
			marker_line_color='white',
			hovertemplate=hover_template or '<b>%{location}</b><br>Cobertura: %{z:.1f}%<extra></extra>'
		))
		fig.update_layout(
			mapbox_style="carto-positron",
			mapbox_zoom=mapbox_zoom,
			mapbox_center=mapbox_center
		)
	
	elif tipo == "custom":
		# Para gráficos personalizados con go.Figure
		fig = kwargs.pop('fig', None)
		if fig is None:
			st.error("Para tipo 'custom' debes proporcionar un objeto 'fig' en kwargs")
			return
	
	else:
		st.error(f"Tipo de gráfico '{tipo}' no soportado")
		return
	
	# Aplicar altura personalizada si se especifica
	if height:
		fig.update_layout(height=height)
	
	# Aplicar layout adicional de kwargs
	if layout_updates:
		fig.update_layout(**layout_updates)
	
	# Aplicar actualizaciones de traces de kwargs
	if trace_updates:
		fig.update_traces(**trace_updates)
	
	# Aplicar título dentro del gráfico
	if titulo:
		fig.update_layout(
			title={
				'text': titulo,
				'x': 0.02,
				'xanchor': 'left',
				'font': {
					'size': 20,
					'color': '#1a1a1a',
					'family': 'Arial, sans-serif'
				}
			}
		)
	
	# Aplicar estilos de card al gráfico con padding, border-radius y box-shadow
	fig.update_layout(
		margin=dict(l=20, r=20, t=60 if titulo else 20, b=20),
		paper_bgcolor='white',
		plot_bgcolor='white'
	)
	
	# Aplicar estilos de card con CSS
	st.markdown("""
		<style>
		.stPlotlyChart {
			background: white;
			padding: 15px;
			border-radius: 12px;
			box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
		}
		</style>
	""", unsafe_allow_html=True)
	
	st.plotly_chart(
		fig, 
		width=width, 
		key=key,
		config={'displayModeBar': True}
	)
	

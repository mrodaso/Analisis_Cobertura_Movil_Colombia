import streamlit as st

def render_header():
	header_html = """
	<header id="header-content">
		<div class="header-bar">
			<nav>
				<a href="#header" class="logo">Analítica</a>
				<ul class="nav-links">
					<li><a href="#statistics">Estadísticas</a></li>
					<li><a href="#charts">Gráficas</a></li>
					<li><a href="#operadores">Operadores</a></li>
					<li><a href="#cobertura">Cobertura</a></li>
					<li><a href="#evolucion">Evolución</a></li>
					<li><a href="#mapas">Mapas</a></li>
					<li><a href="#footer">Pie de Página</a></li>
				</ul>
			</nav>
		</div>
	</header>
	"""
	st.markdown(header_html, unsafe_allow_html=True)

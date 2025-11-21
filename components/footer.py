import streamlit as st

def render_footer():
	st.markdown(
		"""
		<div class="footer-simple">
			<p>© 2025 Dashboard Analytics. Desarrollado por <strong>Marisol Rodas</strong></p>
		</div>
		""",
		unsafe_allow_html=True
	)

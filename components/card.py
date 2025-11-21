import streamlit as st

def card(content_func, title=None, subtitle=None):
	
	st.markdown('<div class="card" style="background: white; border-radius: 12px; box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1); padding: 1.5rem; margin-bottom: 1.5rem;">', unsafe_allow_html=True)
	
	if title:
		st.markdown(f'<h3 style="font-size: 1.25rem; font-weight: 600; color: #1f2937; margin-bottom: 1rem; margin-top: 0;">{title}</h3>', unsafe_allow_html=True)
	
	if subtitle:
		st.markdown(f'<p style="font-size: 0.875rem; color: #6b7280; margin-bottom: 1rem;">{subtitle}</p>', unsafe_allow_html=True)
	
	# Ejecutar la función de contenido dentro del contenedor
	content_func()
	
	st.markdown('</div>', unsafe_allow_html=True)

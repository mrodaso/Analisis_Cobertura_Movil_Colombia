import streamlit as st
import plotly.express as px

def grafico_cabeceras_sin_cobertura(df_final_sorted, width='stretch', key=None):
	st.markdown("## Cabeceras sin Cobertura")
	df_top = df_final_sorted.nlargest(10, "CPOB_SIN_INTERNET")
	fig = px.bar(
		df_top,
		x="DEPARTAMENTO",
		y="CPOB_SIN_INTERNET",
		title="Departamentos con más cabeceras sin cobertura",
		labels={"CPOB_SIN_INTERNET": "Cantidad"},
		template="plotly_white"
	)
	st.plotly_chart(fig, width='stretch', key=key)

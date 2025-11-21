import streamlit as st
import plotly.express as px

def grafico_tecnologias(df, width='stretch', key=None):
	st.markdown("## Distribución de Tecnologías")
	fig = px.histogram(
		df,
		x="TECNOLOGIA",
		color="TECNOLOGIA",
		category_orders={"TECNOLOGIA": df["TECNOLOGIA"].value_counts().index.tolist()},
		title="Distribución de Registros por Tipo de Tecnología",
		template="plotly_white"
	)
	fig.update_layout(xaxis_title="Tipo de Tecnología", yaxis_title="Cantidad de Registros")
	st.plotly_chart(fig, width='stretch', key=key)

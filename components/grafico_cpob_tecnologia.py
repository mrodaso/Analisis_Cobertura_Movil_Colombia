import streamlit as st
import plotly.express as px

def grafico_cpob_tecnologia(df, width='stretch', key=None):
	st.markdown("## CPOB por Tecnología")
	cpob_tec = df.groupby("TECNOLOGIA")["CPOB"].nunique().reset_index()
	fig = px.bar(
		cpob_tec, x="TECNOLOGIA", y="CPOB", color="TECNOLOGIA", labels={"CPOB": "Cantidad de CPOB"}, template="plotly_white"
	)
	st.plotly_chart(fig, width='stretch', key=key)

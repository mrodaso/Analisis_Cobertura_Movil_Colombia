import streamlit as st

def stat_card(title, value, description, trend="up", trend_value=None, trend_color="#22c55e"):
    """
    Muestra una tarjeta de estadística.
    trend: "up" o "down"
    trend_value: porcentaje o valor de tendencia (ej: "25%")
    trend_color: color del indicador de tendencia
    """
    # SVG para tendencia
    if trend == "up":
        svg = f"""
        <svg width="56" height="32" viewBox="0 0 56 32" fill="none" xmlns="http://www.w3.org/2000/svg">
            <polyline points="2,30 12,18 22,22 32,10 42,14 54,4"
                fill="none" stroke="{trend_color}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        """
    else:
        svg = f"""
        <svg width="56" height="32" viewBox="0 0 56 32" fill="none" xmlns="http://www.w3.org/2000/svg">
            <polyline points="2,6 12,18 22,14 32,26 42,22 54,30"
                fill="none" stroke="{trend_color}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        """

    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-card-title">{title}</div>
        <div class="stat-card-content">
            <div class="stat-card-value">{value}</div>
            <div>{svg}</div>
        </div>
        <div class="stat-card-description">{description}</div>
        {"<div class='stat-card-trend' style='background:" + trend_color + "1A;color:" + trend_color + ";'>" + ("↑" if trend=="up" else "↓") + f"&nbsp;{trend_value}</div>" if trend_value else ""}
    </div>
    """, unsafe_allow_html=True)

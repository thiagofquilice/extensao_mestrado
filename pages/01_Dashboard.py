import streamlit as st
from app import ensure_demo_state, render_sidebar, render_kpis, render_last_updates

st.set_page_config(page_title="Dashboard | ExtensãoMP", page_icon="📊", layout="wide")
ensure_demo_state()
render_sidebar()

st.title("Dashboard")
st.caption("Indicadores rápidos e últimas atualizações registradas no session_state.")

render_kpis()

st.divider()
render_last_updates()

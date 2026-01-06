import streamlit as st
from collections import Counter
from app import ensure_demo_state, render_sidebar

st.set_page_config(page_title="Indicadores (PPG) | ExtensãoMP", page_icon="📈", layout="wide")
ensure_demo_state()
render_sidebar()

st.title("Indicadores (nível PPG fictício)")
st.caption("Gráficos simples (sem cores customizadas) com contagens a partir do session_state.")

# Contagem de projetos por status
proj_status = [p.get("status", "N/D") for p in st.session_state.projects]
status_counts = Counter(proj_status)

st.subheader("Projetos por status")
if len(status_counts) == 0:
    st.caption("Sem projetos.")
else:
    st.bar_chart(status_counts)

st.divider()

# Contagem de atividades por tipo
act_types = [a.get("tipo", "N/D") for a in st.session_state.activities]
type_counts = Counter(act_types)

st.subheader("Atividades por tipo")
if len(type_counts) == 0:
    st.caption("Sem atividades.")
else:
    st.bar_chart(type_counts)

st.divider()

st.subheader("Resumo (contagens)")
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Projetos", len(st.session_state.projects))
c2.metric("Atividades", len(st.session_state.activities))
c3.metric("Produtos", len(st.session_state.products))
c4.metric("Devolutivas", len(st.session_state.feedbacks))
c5.metric("Evidências", len(st.session_state.evidences))

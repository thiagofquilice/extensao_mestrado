import streamlit as st
from app import ensure_demo_state, render_sidebar, add_update

st.set_page_config(page_title="Administração | ExtensãoMP", page_icon="⚙️", layout="wide")
ensure_demo_state()
render_sidebar()

st.title("Administração (mock)")
st.caption("Configurações fictícias salvas apenas no session_state.")

cfg = st.session_state.config

with st.form("form_config"):
    ppg_nome = st.text_input("Nome do PPG", value=cfg.get("ppg_nome",""))
    ppg_email = st.text_input("E-mail", value=cfg.get("ppg_email",""))
    ano_ref = st.number_input("Ano de referência", min_value=2000, max_value=2100, value=int(cfg.get("ano_referencia", 2026)), step=1)
    ok = st.form_submit_button("Salvar configurações")

    if ok:
        st.session_state.config["ppg_nome"] = ppg_nome
        st.session_state.config["ppg_email"] = ppg_email
        st.session_state.config["ano_referencia"] = int(ano_ref)
        add_update("Administração", "Configurações atualizadas (session_state).")
        st.success("Configurações salvas no session_state.")

st.divider()
st.subheader("Configuração atual (preview)")
st.json(st.session_state.config)

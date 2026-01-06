import streamlit as st
from app import ensure_demo_state, render_sidebar, add_update, project_options, _new_id

st.set_page_config(page_title="Atividades | ExtensãoMP", page_icon="🧰", layout="wide")
ensure_demo_state()
render_sidebar()

st.title("Atividades")
st.caption("Cadastro (mock) de atividades vinculadas a projetos e listagem por projeto.")

opts = project_options()
if len(opts) == 0:
    st.info("Nenhum projeto cadastrado. Crie um projeto primeiro.")
    st.stop()

label_map = {o["label"]: o["id"] for o in opts}

st.subheader("Nova atividade")
with st.form("form_add_atividade", clear_on_submit=True):
    proj_label = st.selectbox("Projeto", options=list(label_map.keys()))
    project_id = label_map[proj_label]

    data = st.date_input("Data")
    tipo = st.selectbox("Tipo", ["Reunião", "Oficina", "Curso", "Visita técnica", "Mentoria", "Outro"])
    descricao = st.text_area("Descrição")
    participantes = st.number_input("Nº participantes", min_value=0, value=0, step=1)
    resultados = st.text_area("Resultados imediatos")
    proximos = st.text_area("Próximos passos")
    evidencia_link = st.text_input("Evidência (link)")

    ok = st.form_submit_button("Salvar")
    if ok:
        st.session_state.activities.append({
            "id": _new_id("act"),
            "project_id": project_id,
            "data": str(data),
            "tipo": tipo,
            "descricao": descricao,
            "participantes": int(participantes),
            "resultados_imediatos": resultados,
            "proximos_passos": proximos,
            "evidencia_link": evidencia_link,
        })
        add_update("Atividades", f"Atividade criada: {tipo} ({proj_label})")
        st.success("Atividade salva no session_state.")

st.divider()

st.subheader("Atividades por projeto")
proj_label2 = st.selectbox("Selecione um projeto para filtrar", options=list(label_map.keys()), key="proj_filter_acts")
pid = label_map[proj_label2]
acts = [a for a in st.session_state.activities if a.get("project_id") == pid]

st.write("**Registros:**", len(acts))
if acts:
    st.dataframe([{
        "data": a["data"],
        "tipo": a["tipo"],
        "descrição": a["descricao"],
        "participantes": a["participantes"],
        "evidência": a.get("evidencia_link",""),
    } for a in acts], use_container_width=True, hide_index=True)
else:
    st.caption("Sem atividades para este projeto.")

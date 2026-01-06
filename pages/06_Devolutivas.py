import streamlit as st
from app import ensure_demo_state, render_sidebar, add_update, project_options, _new_id

st.set_page_config(page_title="Devolutivas & Feedback | ExtensãoMP", page_icon="💬", layout="wide")
ensure_demo_state()
render_sidebar()

st.title("Devolutivas & Feedback")
st.caption("Registro (mock) de devolutivas por projeto, com nota e comentários.")

opts = project_options()
if len(opts) == 0:
    st.info("Nenhum projeto cadastrado. Crie um projeto primeiro.")
    st.stop()

label_map = {o["label"]: o["id"] for o in opts}

st.subheader("Nova devolutiva")
with st.form("form_add_fb", clear_on_submit=True):
    proj_label = st.selectbox("Projeto", options=list(label_map.keys()))
    project_id = label_map[proj_label]

    data = st.date_input("Data")
    formato = st.selectbox("Formato", ["Reunião", "Seminário", "Documento", "Mensagem", "Outro"])
    descricao = st.text_area("Descrição")
    nota = st.slider("Nota (1 a 5)", min_value=1, max_value=5, value=4)
    comentarios = st.text_area("Comentários")

    ok = st.form_submit_button("Salvar")
    if ok:
        st.session_state.feedbacks.append({
            "id": _new_id("fb"),
            "project_id": project_id,
            "data": str(data),
            "formato": formato,
            "descricao": descricao,
            "nota": int(nota),
            "comentarios": comentarios,
        })
        add_update("Devolutivas", f"Devolutiva criada: {formato} ({proj_label})")
        st.success("Devolutiva salva no session_state.")

st.divider()

st.subheader("Lista de devolutivas")
if len(st.session_state.feedbacks) == 0:
    st.caption("Sem devolutivas cadastradas.")
else:
    st.dataframe([{
        "projeto_id": f["project_id"],
        "data": f["data"],
        "formato": f["formato"],
        "nota": f["nota"],
        "descrição": f.get("descricao",""),
        "comentários": f.get("comentarios",""),
    } for f in st.session_state.feedbacks], use_container_width=True, hide_index=True)

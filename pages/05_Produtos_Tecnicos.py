import streamlit as st
from app import ensure_demo_state, render_sidebar, add_update, project_options, _new_id

st.set_page_config(page_title="Produtos Técnicos | ExtensãoMP", page_icon="🛠️", layout="wide")
ensure_demo_state()
render_sidebar()

st.title("Produtos Técnicos")
st.caption("Cadastro (mock) de produtos técnicos vinculados a projetos.")

opts = project_options()
if len(opts) == 0:
    st.info("Nenhum projeto cadastrado. Crie um projeto primeiro.")
    st.stop()

label_map = {o["label"]: o["id"] for o in opts}

st.subheader("Novo produto técnico")
with st.form("form_add_pt", clear_on_submit=True):
    proj_label = st.selectbox("Projeto", options=list(label_map.keys()))
    project_id = label_map[proj_label]

    tipo = st.selectbox("Tipo", ["Cartilha", "Manual", "Relatório Técnico", "Plataforma/App", "Vídeo", "Outro"])
    descricao = st.text_area("Descrição")
    publico = st.text_input("Público-alvo")
    status = st.selectbox("Status", ["Em desenvolvimento", "Em piloto", "Publicado"])
    link = st.text_input("Link")

    ok = st.form_submit_button("Salvar")
    if ok:
        st.session_state.products.append({
            "id": _new_id("pt"),
            "project_id": project_id,
            "tipo": tipo,
            "descricao": descricao,
            "publico_alvo": publico,
            "status": status,
            "link": link,
        })
        add_update("Produtos", f"Produto técnico criado: {tipo} ({proj_label})")
        st.success("Produto técnico salvo no session_state.")

st.divider()

st.subheader("Lista de produtos técnicos")
if len(st.session_state.products) == 0:
    st.caption("Sem produtos técnicos cadastrados.")
else:
    st.dataframe([{
        "projeto_id": p["project_id"],
        "tipo": p["tipo"],
        "status": p["status"],
        "público-alvo": p["publico_alvo"],
        "descrição": p["descricao"],
        "link": p.get("link",""),
    } for p in st.session_state.products], use_container_width=True, hide_index=True)

import streamlit as st
from app import ensure_demo_state, render_sidebar, add_update, _new_id

st.set_page_config(page_title="Projetos | ExtensãoMP", page_icon="🗂️", layout="wide")
ensure_demo_state()
render_sidebar()

st.title("Projetos")
st.caption("Lista, filtros (mock) e criação de projetos no session_state (sem persistência).")

# Filtros (visuais)
st.subheader("Filtros (mock)")
col1, col2, col3 = st.columns(3)
with col1:
    status_f = st.selectbox("Status", ["(Todos)", "Planejado", "Em execução", "Concluído"], index=0)
with col2:
    territorio_f = st.selectbox("Território", ["(Todos)", "Centro-Oeste", "Sul", "Sudeste", "Norte", "Nordeste"], index=0)
with col3:
    tag_f = st.text_input("Tag (contém)", value="")

st.divider()

# Listagem
st.subheader("Projetos cadastrados")
projects = st.session_state.projects

# filtro leve (opcional)
def _matches(p):
    ok = True
    if status_f != "(Todos)":
        ok = ok and (p.get("status") == status_f)
    if territorio_f != "(Todos)":
        ok = ok and (p.get("territorio") == territorio_f)
    if tag_f.strip():
        ok = ok and any(tag_f.strip().lower() in t.lower() for t in p.get("tags", []))
    return ok

filtered = [p for p in projects if _matches(p)]

if len(filtered) == 0:
    st.info("Nenhum projeto encontrado com os filtros atuais.")
else:
    st.dataframe(
        [{
            "id": p["id"],
            "título": p["titulo"],
            "território": p["territorio"],
            "status": p["status"],
            "tags": ", ".join(p.get("tags", [])),
        } for p in filtered],
        use_container_width=True,
        hide_index=True
    )

st.divider()

# Criar projeto
st.subheader("Criar projeto")
with st.expander("Abrir formulário de criação", expanded=False):
    with st.form("form_criar_projeto", clear_on_submit=True):
        titulo = st.text_input("Título")
        territorio = st.selectbox("Território", ["Centro-Oeste", "Sul", "Sudeste", "Norte", "Nordeste"])
        parceiros = st.text_area("Parceiros (texto)")
        vinculo = st.text_input("Vínculo (linha/área/curso)")
        metodologia = st.text_area("Metodologia (resumo)")
        plano_devolutiva = st.text_area("Plano de devolutiva (resumo)")
        status = st.selectbox("Status", ["Planejado", "Em execução", "Concluído"])
        tags_txt = st.text_input("Tags (separadas por vírgula)", value="")

        submitted = st.form_submit_button("Salvar projeto")
        if submitted:
            tags = [t.strip() for t in tags_txt.split(",") if t.strip()]
            proj = {
                "id": _new_id("proj"),
                "titulo": titulo or "(Sem título)",
                "territorio": territorio,
                "parceiros": parceiros,
                "vinculo": vinculo,
                "metodologia": metodologia,
                "plano_devolutiva": plano_devolutiva,
                "status": status,
                "tags": tags,
                "narrativa_impacto": "",
                "indicadores": [],
            }
            st.session_state.projects.append(proj)
            add_update("Projetos", f"Projeto criado: {proj['titulo']}")
            st.success("Projeto salvo no session_state.")

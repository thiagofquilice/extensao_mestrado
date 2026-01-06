import streamlit as st
from app import (
    ensure_demo_state, render_sidebar, add_update,
    project_options, get_project_by_id, _new_id
)

st.set_page_config(page_title="Projeto (Detalhe) | ExtensãoMP", page_icon="🧩", layout="wide")
ensure_demo_state()
render_sidebar()

st.title("Projeto (Detalhe)")
st.caption("Gerencie itens vinculados a um projeto: atividades, produtos técnicos, devolutivas, evidências, narrativa e indicadores.")

opts = project_options()
if len(opts) == 0:
    st.info("Nenhum projeto cadastrado. Crie um projeto primeiro na página Projetos.")
    st.stop()

label_map = {o["label"]: o["id"] for o in opts}
choice = st.selectbox("Selecione um projeto", options=list(label_map.keys()))
project_id = label_map[choice]
proj = get_project_by_id(project_id)

if not proj:
    st.error("Projeto não encontrado.")
    st.stop()

# Helpers de listagem por projeto
def _items_by_project(items, pid):
    return [x for x in items if x.get("project_id") == pid]

st.subheader("Resumo do projeto")
c1, c2, c3 = st.columns([2, 1, 1])
with c1:
    st.write(f"**Título:** {proj['titulo']}")
    st.write(f"**Território:** {proj['territorio']}")
    st.write(f"**Parceiros:** {proj['parceiros'] or '-'}")
with c2:
    st.write(f"**Status:** {proj['status']}")
    st.write(f"**Vínculo:** {proj['vinculo'] or '-'}")
with c3:
    st.write("**Tags:**")
    st.write(", ".join(proj.get("tags", [])) or "-")

st.divider()

tabs = st.tabs([
    "Visão geral",
    "Atividades",
    "Produtos Técnicos",
    "Devolutivas & Feedback",
    "Evidências",
    "Narrativa de Impacto",
    "Indicadores do Projeto",
])

# 1) Visão geral (editar campos básicos)
with tabs[0]:
    st.subheader("Visão geral")
    with st.form("form_edit_projeto"):
        titulo = st.text_input("Título", value=proj.get("titulo", ""))
        territorio = st.text_input("Território", value=proj.get("territorio", ""))
        parceiros = st.text_area("Parceiros", value=proj.get("parceiros", ""))
        vinculo = st.text_input("Vínculo", value=proj.get("vinculo", ""))
        metodologia = st.text_area("Metodologia", value=proj.get("metodologia", ""))
        plano = st.text_area("Plano de devolutiva", value=proj.get("plano_devolutiva", ""))
        status = st.selectbox("Status", ["Planejado", "Em execução", "Concluído"],
                              index=["Planejado","Em execução","Concluído"].index(proj.get("status","Planejado")))
        tags_txt = st.text_input("Tags (vírgula)", value=", ".join(proj.get("tags", [])))

        ok = st.form_submit_button("Salvar alterações")
        if ok:
            proj["titulo"] = titulo or "(Sem título)"
            proj["territorio"] = territorio
            proj["parceiros"] = parceiros
            proj["vinculo"] = vinculo
            proj["metodologia"] = metodologia
            proj["plano_devolutiva"] = plano
            proj["status"] = status
            proj["tags"] = [t.strip() for t in tags_txt.split(",") if t.strip()]
            add_update("Projeto", f"Projeto atualizado: {proj['titulo']}")
            st.success("Alterações salvas no session_state.")

# 2) Atividades (vinculadas)
with tabs[1]:
    st.subheader("Atividades do projeto")
    with st.form("form_add_atividade_proj", clear_on_submit=True):
        data = st.date_input("Data")
        tipo = st.selectbox("Tipo", ["Reunião", "Oficina", "Curso", "Visita técnica", "Mentoria", "Outro"])
        descricao = st.text_area("Descrição")
        participantes = st.number_input("Nº participantes", min_value=0, value=0, step=1)
        resultados = st.text_area("Resultados imediatos")
        proximos = st.text_area("Próximos passos")
        evidencia_link = st.text_input("Evidência (link)")
        ok = st.form_submit_button("Salvar atividade")

        if ok:
            act = {
                "id": _new_id("act"),
                "project_id": project_id,
                "data": str(data),
                "tipo": tipo,
                "descricao": descricao,
                "participantes": int(participantes),
                "resultados_imediatos": resultados,
                "proximos_passos": proximos,
                "evidencia_link": evidencia_link,
            }
            st.session_state.activities.append(act)
            add_update("Atividades", f"Atividade adicionada em {proj['titulo']}: {tipo}")
            st.success("Atividade salva no session_state.")

    acts = _items_by_project(st.session_state.activities, project_id)
    st.write("**Registros:**", len(acts))
    if acts:
        st.dataframe([{
            "data": a["data"],
            "tipo": a["tipo"],
            "descrição": a["descricao"],
            "participantes": a["participantes"],
            "evidência": a.get("evidencia_link",""),
        } for a in acts], use_container_width=True, hide_index=True)

# 3) Produtos Técnicos
with tabs[2]:
    st.subheader("Produtos técnicos do projeto")
    with st.form("form_add_produto_proj", clear_on_submit=True):
        tipo = st.selectbox("Tipo", ["Cartilha", "Manual", "Relatório Técnico", "Plataforma/App", "Vídeo", "Outro"])
        descricao = st.text_area("Descrição")
        publico = st.text_input("Público-alvo")
        status = st.selectbox("Status", ["Em desenvolvimento", "Em piloto", "Publicado"])
        link = st.text_input("Link")
        ok = st.form_submit_button("Salvar produto técnico")
        if ok:
            pt = {
                "id": _new_id("pt"),
                "project_id": project_id,
                "tipo": tipo,
                "descricao": descricao,
                "publico_alvo": publico,
                "status": status,
                "link": link,
            }
            st.session_state.products.append(pt)
            add_update("Produtos", f"Produto técnico adicionado em {proj['titulo']}: {tipo}")
            st.success("Produto técnico salvo no session_state.")

    pts = _items_by_project(st.session_state.products, project_id)
    st.write("**Registros:**", len(pts))
    if pts:
        st.dataframe([{
            "tipo": x["tipo"],
            "status": x["status"],
            "público-alvo": x["publico_alvo"],
            "descrição": x["descricao"],
            "link": x.get("link",""),
        } for x in pts], use_container_width=True, hide_index=True)

# 4) Devolutivas & Feedback
with tabs[3]:
    st.subheader("Devolutivas & Feedback")
    with st.form("form_add_fb_proj", clear_on_submit=True):
        data = st.date_input("Data", key="fb_data")
        formato = st.selectbox("Formato", ["Reunião", "Seminário", "Documento", "Mensagem", "Outro"])
        descricao = st.text_area("Descrição", key="fb_desc")
        nota = st.slider("Nota (1 a 5)", min_value=1, max_value=5, value=4)
        comentarios = st.text_area("Comentários", key="fb_com")
        ok = st.form_submit_button("Salvar devolutiva")
        if ok:
            fb = {
                "id": _new_id("fb"),
                "project_id": project_id,
                "data": str(data),
                "formato": formato,
                "descricao": descricao,
                "nota": int(nota),
                "comentarios": comentarios,
            }
            st.session_state.feedbacks.append(fb)
            add_update("Devolutivas", f"Devolutiva registrada em {proj['titulo']}: {formato}")
            st.success("Devolutiva salva no session_state.")

    fbs = _items_by_project(st.session_state.feedbacks, project_id)
    st.write("**Registros:**", len(fbs))
    if fbs:
        st.dataframe([{
            "data": x["data"],
            "formato": x["formato"],
            "nota": x["nota"],
            "descrição": x.get("descricao",""),
            "comentários": x.get("comentarios",""),
        } for x in fbs], use_container_width=True, hide_index=True)

# 5) Evidências
with tabs[4]:
    st.subheader("Evidências")
    with st.form("form_add_evidencia_proj", clear_on_submit=True):
        tipo = st.selectbox("Tipo", ["Foto/Álbum", "Ata", "Lista de presença", "Link externo", "Outro"])
        descricao = st.text_area("Descrição")
        link = st.text_input("Link")
        ok = st.form_submit_button("Salvar evidência")
        if ok:
            ev = {
                "id": _new_id("ev"),
                "project_id": project_id,
                "tipo": tipo,
                "descricao": descricao,
                "link": link,
            }
            st.session_state.evidences.append(ev)
            add_update("Evidências", f"Evidência adicionada em {proj['titulo']}: {tipo}")
            st.success("Evidência salva no session_state.")

    evs = _items_by_project(st.session_state.evidences, project_id)
    st.write("**Registros:**", len(evs))
    if evs:
        with st.expander("Ver evidências cadastradas", expanded=True):
            for e in evs:
                st.write(f"- **{e['tipo']}** — {e['descricao']}  \n  {e.get('link','')}".strip())

# 6) Narrativa de Impacto
with tabs[5]:
    st.subheader("Narrativa de Impacto")
    st.caption("Campo livre (mock) para consolidar resultados e mudanças percebidas.")
    with st.form("form_narrativa"):
        narrativa = st.text_area("Narrativa", value=proj.get("narrativa_impacto", ""), height=180)
        ok = st.form_submit_button("Salvar narrativa")
        if ok:
            proj["narrativa_impacto"] = narrativa
            add_update("Narrativa", f"Narrativa atualizada em {proj['titulo']}")
            st.success("Narrativa salva no session_state.")

    if proj.get("narrativa_impacto"):
        st.info("Narrativa atual (preview):")
        st.write(proj["narrativa_impacto"])

# 7) Indicadores do Projeto
with tabs[6]:
    st.subheader("Indicadores do Projeto")
    st.caption("Indicadores simples (mock) no formato chave-valor, vinculados ao projeto.")
    if "indicadores" not in proj:
        proj["indicadores"] = []

    with st.form("form_add_indicador", clear_on_submit=True):
        nome = st.text_input("Nome do indicador (ex.: participantes totais)")
        valor = st.text_input("Valor (ex.: 120)")
        ok = st.form_submit_button("Adicionar indicador")
        if ok:
            proj["indicadores"].append({"nome": nome or "(sem nome)", "valor": valor})
            add_update("Indicadores", f"Indicador adicionado em {proj['titulo']}: {nome}")
            st.success("Indicador salvo no session_state.")

    if proj["indicadores"]:
        st.dataframe(proj["indicadores"], use_container_width=True, hide_index=True)
    else:
        st.caption("Sem indicadores cadastrados para este projeto.")

import streamlit as st
from app import ensure_demo_state, render_sidebar, get_project_by_id

st.set_page_config(page_title="Portfólio Anual | ExtensãoMP", page_icon="🗓️", layout="wide")
ensure_demo_state()
render_sidebar()

st.title("Portfólio Anual (mock)")
st.caption("Gera um texto (st.markdown) com base no session_state. Sem exportação/sem copiar.")

ano = st.selectbox("Selecione o ano (visual)", options=[2024, 2025, 2026, 2027], index=2)

if st.button("Gerar portfólio"):
    projects = st.session_state.projects
    activities = st.session_state.activities
    products = st.session_state.products
    evidences = st.session_state.evidences

    lines = []
    cfg = st.session_state.config
    lines.append(f"# Portfólio Anual de Extensão — {ano}")
    lines.append("")
    lines.append(f"**PPG (fictício):** {cfg.get('ppg_nome','-')}")
    lines.append(f"**E-mail (fictício):** {cfg.get('ppg_email','-')}")
    lines.append("")
    lines.append("## Resumo (mock)")
    lines.append(f"- Projetos: {len(projects)}")
    lines.append(f"- Atividades: {len(activities)}")
    lines.append(f"- Produtos técnicos: {len(products)}")
    lines.append(f"- Evidências: {len(evidences)}")
    lines.append("")

    lines.append("## Projetos")
    if not projects:
        lines.append("_Sem projetos cadastrados._")
    else:
        for p in projects:
            lines.append(f"### {p.get('titulo','(sem título)')}")
            lines.append(f"- Status: {p.get('status','-')}")
            lines.append(f"- Território: {p.get('territorio','-')}")
            tags = ", ".join(p.get("tags", [])) or "-"
            lines.append(f"- Tags: {tags}")
            lines.append("")

            narrativa = (p.get("narrativa_impacto") or "").strip()
            if narrativa:
                lines.append("**Narrativa curta (se houver):**")
                lines.append(narrativa)
                lines.append("")
            else:
                lines.append("**Narrativa curta (se houver):** _não cadastrada_")
                lines.append("")

            # Evidências do projeto
            evs = [e for e in evidences if e.get("project_id") == p["id"]]
            if evs:
                lines.append("**Evidências (links):**")
                for e in evs[:5]:
                    link = e.get("link", "")
                    lines.append(f"- {e.get('tipo','Evidência')}: {link}")
            else:
                lines.append("**Evidências (links):** _nenhuma cadastrada_")
            lines.append("")

    portfolio_md = "\n".join(lines)
    st.subheader("Texto gerado")
    st.markdown(portfolio_md)

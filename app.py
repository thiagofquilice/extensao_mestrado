import streamlit as st
from datetime import datetime
from uuid import uuid4
from typing import Dict, Any, List, Optional

# -----------------------------
# Helpers (IDs, timestamps)
# -----------------------------
def _new_id(prefix: str) -> str:
    return f"{prefix}_{uuid4().hex[:10]}"


def _now_str() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# -----------------------------
# Demo state
# -----------------------------
def ensure_demo_state() -> None:
    """Inicializa dados demo no st.session_state, se ainda não existirem."""
    if "projects" not in st.session_state:
        st.session_state.projects = []
    if "activities" not in st.session_state:
        st.session_state.activities = []
    if "products" not in st.session_state:
        st.session_state.products = []
    if "feedbacks" not in st.session_state:
        st.session_state.feedbacks = []
    if "evidences" not in st.session_state:
        st.session_state.evidences = []
    if "updates" not in st.session_state:
        st.session_state.updates = []
    if "config" not in st.session_state:
        st.session_state.config = {
            "ppg_nome": "PPG Fictício em Gestão (Demo)",
            "ppg_email": "ppg.demo@instituicao.br",
            "ano_referencia": datetime.now().year,
        }

    # Popular com dados demo apenas 1x (quando está vazio)
    if len(st.session_state.projects) == 0:
        p1 = {
            "id": _new_id("proj"),
            "titulo": "Rede de Extensão em Territórios Criativos",
            "territorio": "Centro-Oeste",
            "parceiros": "Prefeitura, Associação comunitária, Escola técnica",
            "vinculo": "Linha 1 (Inovação e Desenvolvimento)",
            "metodologia": "Diagnóstico participativo + oficinas + prototipação",
            "plano_devolutiva": "Devolutivas trimestrais com relatórios curtos e rodas de conversa",
            "status": "Em execução",
            "tags": ["território", "inovação", "oficinas"],
            "narrativa_impacto": "",
            "indicadores": [],
        }
        p2 = {
            "id": _new_id("proj"),
            "titulo": "Laboratório de Soluções para Agricultura Familiar",
            "territorio": "Sul",
            "parceiros": "Cooperativa, Emater, ONG local",
            "vinculo": "Linha 2 (Sustentabilidade e Transformação)",
            "metodologia": "Aulas-oficina + visitas técnicas + co-criação",
            "plano_devolutiva": "Seminário final + cartilha digital + feedback estruturado",
            "status": "Planejado",
            "tags": ["agro", "sustentabilidade"],
            "narrativa_impacto": "",
            "indicadores": [],
        }
        st.session_state.projects.extend([p1, p2])

        # atividades demo
        st.session_state.activities.append({
            "id": _new_id("act"),
            "project_id": p1["id"],
            "data": datetime.now().strftime("%Y-%m-%d"),
            "tipo": "Oficina",
            "descricao": "Oficina de mapeamento de necessidades com lideranças locais.",
            "participantes": 18,
            "resultados_imediatos": "Lista priorizada de problemas e oportunidades.",
            "proximos_passos": "Desenhar protótipos de solução para 2 problemas.",
            "evidencia_link": "https://exemplo.com/evidencia/oficina1",
        })

        # produto demo
        st.session_state.products.append({
            "id": _new_id("pt"),
            "project_id": p1["id"],
            "tipo": "Cartilha",
            "descricao": "Cartilha de boas práticas para iniciativas territoriais.",
            "publico_alvo": "Agentes locais e gestores públicos",
            "status": "Em desenvolvimento",
            "link": "https://exemplo.com/cartilha",
        })

        # devolutiva demo
        st.session_state.feedbacks.append({
            "id": _new_id("fb"),
            "project_id": p1["id"],
            "data": datetime.now().strftime("%Y-%m-%d"),
            "formato": "Reunião",
            "descricao": "Devolutiva parcial do diagnóstico com validação coletiva.",
            "nota": 4,
            "comentarios": "Boa aderência. Pediram mais exemplos práticos.",
        })

        # evidência demo
        st.session_state.evidences.append({
            "id": _new_id("ev"),
            "project_id": p1["id"],
            "tipo": "Foto/Álbum",
            "descricao": "Registro fotográfico da oficina.",
            "link": "https://exemplo.com/album/oficina",
        })

        add_update("Sistema", "Dados demo carregados no session_state.")


def add_update(origem: str, mensagem: str) -> None:
    ensure_demo_state()
    st.session_state.updates.insert(0, {
        "ts": _now_str(),
        "origem": origem,
        "mensagem": mensagem,
    })
    # manter lista curta (mock)
    st.session_state.updates = st.session_state.updates[:20]


# -----------------------------
# Lookups
# -----------------------------
def get_project_by_id(project_id: str) -> Optional[Dict[str, Any]]:
    ensure_demo_state()
    for p in st.session_state.projects:
        if p["id"] == project_id:
            return p
    return None


def project_options() -> List[Dict[str, str]]:
    ensure_demo_state()
    return [{"id": p["id"], "label": f'{p["titulo"]} ({p["status"]})'} for p in st.session_state.projects]


# -----------------------------
# Sidebar (menu + status)
# -----------------------------
def render_sidebar() -> None:
    ensure_demo_state()
    st.sidebar.title("ExtensãoMP")

    st.sidebar.caption("Navegação")
    # Links explícitos (além do menu padrão do multipage)
    try:
        st.sidebar.page_link("app.py", label="Home (Início)", icon="🏠")
        st.sidebar.page_link("pages/01_Dashboard.py", label="Dashboard", icon="📊")
        st.sidebar.page_link("pages/02_Projetos.py", label="Projetos", icon="🗂️")
        st.sidebar.page_link("pages/03_Projeto_Detalhe.py", label="Projeto (Detalhe)", icon="🧩")
        st.sidebar.page_link("pages/04_Atividades.py", label="Atividades", icon="🧰")
        st.sidebar.page_link("pages/05_Produtos_Tecnicos.py", label="Produtos Técnicos", icon="🛠️")
        st.sidebar.page_link("pages/06_Devolutivas.py", label="Devolutivas & Feedback", icon="💬")
        st.sidebar.page_link("pages/07_Indicadores.py", label="Indicadores (PPG)", icon="📈")
        st.sidebar.page_link("pages/08_Portfolio_Anual.py", label="Portfólio Anual", icon="🗓️")
        st.sidebar.page_link("pages/09_Administracao.py", label="Administração", icon="⚙️")
    except Exception:
        st.sidebar.info("Use o menu padrão do Streamlit (multipage) para navegar.")

    st.sidebar.divider()
    st.sidebar.subheader("Status do demo")

    st.sidebar.metric("Projetos", len(st.session_state.projects))
    st.sidebar.metric("Atividades", len(st.session_state.activities))
    st.sidebar.metric("Devolutivas", len(st.session_state.feedbacks))
    st.sidebar.metric("Produtos Técnicos", len(st.session_state.products))
    st.sidebar.metric("Evidências", len(st.session_state.evidences))

    st.sidebar.divider()
    cfg = st.session_state.config
    st.sidebar.caption(f"PPG: {cfg.get('ppg_nome','(não definido)')}")
    st.sidebar.caption(f"Ano ref.: {cfg.get('ano_referencia','-')}")


# -----------------------------
# Dashboard UI
# -----------------------------
def render_kpis() -> None:
    ensure_demo_state()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Projetos", len(st.session_state.projects))
    c2.metric("Atividades", len(st.session_state.activities))
    c3.metric("Devolutivas", len(st.session_state.feedbacks))
    c4.metric("Produtos Técnicos", len(st.session_state.products))


def render_last_updates() -> None:
    ensure_demo_state()
    st.subheader("Últimas atualizações")
    if len(st.session_state.updates) == 0:
        st.caption("Sem atualizações ainda.")
        return
    for u in st.session_state.updates[:10]:
        st.write(f"- **{u['ts']}** · *{u['origem']}* — {u['mensagem']}")


def main() -> None:
    st.set_page_config(page_title="ExtensãoMP", page_icon="🧩", layout="wide")
    ensure_demo_state()
    render_sidebar()

    st.title("ExtensãoMP")
    st.caption("MVP de demonstração (somente estrutura). Sem banco de dados, sem autenticação e sem persistência.")

    st.subheader("Visão rápida")
    render_kpis()

    st.divider()
    render_last_updates()


if __name__ == "__main__":
    main()

# ─────────────────────────────────────────────────────────────────────────────
#  World Cup Squad Builder — Streamlit Chat UI
#  Run:  streamlit run app.py
# ─────────────────────────────────────────────────────────────────────────────

import os, json, glob, hashlib, time, warnings, re
import requests
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup
from dotenv import load_dotenv

warnings.filterwarnings("ignore")
load_dotenv()

# ── LangChain ─────────────────────────────────────────────────────────────────
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_core.tools import tool
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory

# ─────────────────────────────────────────────────────────────────────────────
#  Page config
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="WC Squad Builder",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
#  Custom CSS — dark football theme
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    /* ── Global ── */
    .stApp { background: #0d1117; color: #e6edf3; }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: #161b22;
        border-right: 1px solid #30363d;
    }

    /* ── Chat container ── */
    .chat-wrapper {
        max-height: 62vh;
        overflow-y: auto;
        padding: 0 4px;
        margin-bottom: 8px;
    }

    /* ── Message bubbles ── */
    .msg-user {
        background: #1f6feb;
        color: #fff;
        border-radius: 18px 18px 4px 18px;
        padding: 12px 16px;
        margin: 6px 0 6px 20%;
        font-size: 0.95rem;
        line-height: 1.5;
        word-wrap: break-word;
    }
    .msg-bot {
        background: #21262d;
        color: #e6edf3;
        border: 1px solid #30363d;
        border-radius: 18px 18px 18px 4px;
        padding: 12px 16px;
        margin: 6px 20% 6px 0;
        font-size: 0.95rem;
        line-height: 1.5;
        word-wrap: break-word;
    }
    .msg-system {
        background: #1a2330;
        color: #8b949e;
        border-radius: 8px;
        padding: 8px 14px;
        margin: 4px 10%;
        font-size: 0.82rem;
        text-align: center;
        border: 1px dashed #30363d;
    }
    .avatar { font-size: 1.3rem; margin-right: 6px; }

    /* ── Input row ── */
    .stTextInput > div > div > input {
        background: #21262d;
        border: 1px solid #30363d;
        border-radius: 24px;
        color: #e6edf3;
        padding: 10px 18px;
        font-size: 0.95rem;
    }
    .stTextInput > div > div > input:focus {
        border-color: #1f6feb;
        box-shadow: 0 0 0 2px rgba(31,111,235,0.3);
    }

    /* ── Buttons ── */
    .stButton > button {
        background: #238636;
        color: #fff;
        border: none;
        border-radius: 20px;
        padding: 8px 22px;
        font-weight: 600;
        transition: background 0.2s;
    }
    .stButton > button:hover { background: #2ea043; }

    /* ── Stat cards ── */
    .stat-card {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 10px;
        padding: 14px;
        text-align: center;
    }
    .stat-num { font-size: 1.6rem; font-weight: 700; color: #58a6ff; }
    .stat-lbl { font-size: 0.78rem; color: #8b949e; margin-top: 2px; }

    /* ── Player table ── */
    .player-row {
        display: flex;
        align-items: center;
        padding: 6px 10px;
        border-bottom: 1px solid #21262d;
        font-size: 0.88rem;
    }
    .pos-badge {
        display: inline-block;
        padding: 2px 8px;
        border-radius: 10px;
        font-size: 0.75rem;
        font-weight: 700;
        margin-right: 8px;
    }
    .pos-GK { background:#6e40c9; color:#fff; }
    .pos-DF { background:#1f6feb; color:#fff; }
    .pos-MF { background:#238636; color:#fff; }
    .pos-FW { background:#b83030; color:#fff; }

    /* ── Divider ── */
    hr { border-color: #30363d; }

    /* ── Scrollbar ── */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #0d1117; }
    ::-webkit-scrollbar-thumb { background: #30363d; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
#  Session-state initialisation
# ─────────────────────────────────────────────────────────────────────────────
def init_state():
    defaults = {
        "messages":      [],          # [{role, content, squad?, charts?}]
        "players_df":    None,
        "vector_store":  None,
        "embeddings":    None,
        "llm":           None,
        "last_squad":    None,
        "pipeline_ran":  False,
        "api_key_ok":    False,
        "csv_loaded":    False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

init_state()


# ─────────────────────────────────────────────────────────────────────────────
#  Constants & config
# ─────────────────────────────────────────────────────────────────────────────
CACHE_DIR      = Path("cache")
FAISS_INDEX    = "faiss_index"
MAX_SQUAD      = 23
POSITION_SLOTS = {"GK": (3, 3), "DF": (5, 7), "MF": (5, 8), "FW": (4, 6)}
CACHE_DIR.mkdir(exist_ok=True)

QUICK_PROMPTS = [
    "Clinical strikers with xG > 10, creative midfielders, fast defenders",
    "Dominant defenders, sweeper keepers with high save%, disciplined midfielders",
    "Young talent under 23 with high progressive passes and high SCA",
    "Best value squad under €400M budget with high G+A per minute",
    "High-press forwards, box-to-box midfielders, aggressive full-backs",
]


# ─────────────────────────────────────────────────────────────────────────────
#  Data helpers
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_player_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, low_memory=False)
    keep = ["Player","Nation","Pos","Squad","Comp","Age",
            "Gls","Ast","G+A","xG","xAG","PrgC","PrgP","PrgR",
            "SCA","GCA","Tkl","Int","Clr","CrdY","CrdR",
            "MP","Starts","Min","GA90","Save%","CS%"]
    keep = [c for c in keep if c in df.columns]
    df = df[keep].copy()
    for col in [c for c in keep if c not in ("Player","Nation","Pos","Squad","Comp")]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df = (df.sort_values("Min", ascending=False)
            .drop_duplicates(subset="Player")
            .reset_index(drop=True))
    df["PrimaryPos"] = df["Pos"].str.split(",").str[0]
    df["MarketValue"] = (
        (df["Gls"].fillna(0)*2.5) + (df["Ast"].fillna(0)*1.5) +
        (df["xG"].fillna(0)*1.0)  + (df["SCA"].fillna(0)*0.05) +
        (df["Tkl"].fillna(0)*0.1) -
        (df["Age"].fillna(27)-24).clip(-5,5)*1.2 +
        (df["Min"].fillna(0)/90)*0.3 + 5
    ).clip(lower=1).round(1)
    return df


def player_description(row: pd.Series) -> str:
    pos, squad, age = row.get("Pos","?"), row.get("Squad","?"), row.get("Age","?")
    desc = f"{row['Player']} is a {pos} for {squad}, age {age}, "
    desc += f"{int(row.get('MP',0) or 0)} matches ({int(row.get('Min',0) or 0)} mins). "
    if row.get("PrimaryPos") == "GK":
        ga90, sv, cs = row.get("GA90"), row.get("Save%"), row.get("CS%")
        if all(pd.notna(x) for x in [ga90, sv, cs]):
            desc += f"Goalkeeper: GA/90={ga90:.2f}, Save%={sv:.1f}%, CS%={cs:.1f}%."
        else:
            desc += "Goalkeeper."
    else:
        g,a,xg,xag = (row.get(k,0) or 0 for k in ["Gls","Ast","xG","xAG"])
        tk,it,sca  = (row.get(k,0) or 0 for k in ["Tkl","Int","SCA"])
        pc,pp      = (row.get(k,0) or 0 for k in ["PrgC","PrgP"])
        desc += (f"Goals={int(g)}, Assists={int(a)}, xG={xg:.1f}, xAG={xag:.1f}. "
                 f"Tackles={int(tk)}, Interceptions={int(it)}, SCA={int(sca)}. "
                 f"ProgCarries={int(pc)}, ProgPasses={int(pp)}.")
    desc += f" Market value ~€{row.get('MarketValue',0):.1f}M."
    return desc


@st.cache_resource(show_spinner=False)
def build_vector_store(csv_path: str, openai_key: str):
    emb = OpenAIEmbeddings(openai_api_key=openai_key)
    df  = load_player_csv(csv_path)
    if os.path.exists(FAISS_INDEX):
        return FAISS.load_local(FAISS_INDEX, emb, allow_dangerous_deserialization=True), emb, df
    docs = [
        Document(
            page_content=player_description(row),
            metadata={
                "player":        row["Player"],
                "pos":           row.get("Pos",""),
                "primary_pos":   row.get("PrimaryPos",""),
                "squad":         row.get("Squad",""),
                "nation":        row.get("Nation",""),
                "age":           float(row.get("Age",0) or 0),
                "goals":         float(row.get("Gls",0) or 0),
                "assists":       float(row.get("Ast",0) or 0),
                "xg":            float(row.get("xG",0) or 0),
                "xag":           float(row.get("xAG",0) or 0),
                "tackles":       float(row.get("Tkl",0) or 0),
                "interceptions": float(row.get("Int",0) or 0),
                "sca":           float(row.get("SCA",0) or 0),
                "prgp":          float(row.get("PrgP",0) or 0),
                "market_value":  float(row.get("MarketValue",0) or 0),
            }
        ) for _, row in df.iterrows()
    ]
    vs = FAISS.from_documents(docs, emb)
    vs.save_local(FAISS_INDEX)
    return vs, emb, df


def composite_score(p: dict) -> float:
    return (p.get("goals",0)*2.5 + p.get("assists",0)*1.8 +
            p.get("xg",0)*1.2   + p.get("xag",0)*1.0 +
            p.get("sca",0)*0.12  + p.get("prgp",0)*0.08 +
            p.get("tackles",0)*0.25 + p.get("interceptions",0)*0.25)


def retrieve_candidates(vs, criteria: str, pos: str, k: int = 80) -> list:
    pos_prefix = {"GK":"goalkeeper","DF":"defender","MF":"midfielder","FW":"forward striker"}
    query   = f"{pos_prefix.get(pos,'')} {criteria}".strip()
    results = vs.similarity_search(query, k=k)
    cands   = [r.metadata for r in results]
    return [c for c in cands if pos.upper() in c.get("pos","").upper()]


def build_squad(candidates_by_pos: dict, budget=None) -> tuple[list, list]:
    squad, report = [], []
    for pos, (mn, mx) in POSITION_SLOTS.items():
        pool     = sorted(candidates_by_pos.get(pos,[]), key=composite_score, reverse=True)
        selected = 0
        for p in pool:
            if selected >= mx: break
            if budget is not None:
                spent = sum(x["market_value"] for x in squad)
                if spent + p.get("market_value",0) > budget:
                    continue
            squad.append({**p, "slot_pos": pos, "score": round(composite_score(p),2)})
            selected += 1
        icon = "[OK]" if selected >= mn else "[!]"
        report.append(f"{icon} {pos}: {selected}/{mn}-{mx}")
    return squad[:MAX_SQUAD], report


def llm_justify(squad: list, criteria: str, llm) -> str:
    prompt = PromptTemplate(
        input_variables=["criteria","squad_json"],
        template="""
You are a world-class football analytics expert.

USER CRITERIA: {criteria}

SQUAD (JSON):
{squad_json}

Write a concise squad report grouped by GK → DF → MF → FW.
For EACH player: one sentence grounded in their stats.
End with a 2-sentence TACTICAL SUMMARY.

FORMAT:
=== GOALKEEPERS ===
- [Name] ([Nation short] | [Club]): [justification]
...
=== TACTICAL SUMMARY ===
[2 sentences]
""")
    chain = LLMChain(llm=llm, prompt=prompt)
    slim  = [
        {k: p[k] for k in
         ["player","nation","squad","slot_pos","age","goals","assists","xg","tackles","sca","market_value"]}
        for p in squad
    ]
    result = chain.invoke({"criteria": criteria, "squad_json": json.dumps(slim, indent=2)})
    return result.get("text","") if isinstance(result, dict) else str(result)


# ─────────────────────────────────────────────────────────────────────────────
#  Charts
# ─────────────────────────────────────────────────────────────────────────────
def make_charts(squad: list):
    df = pd.DataFrame(squad)

    # 1. Market value bar
    fig1 = px.bar(
        df.sort_values("market_value", ascending=False),
        x="player", y="market_value", color="slot_pos",
        title="Market Value by Player (€M)",
        labels={"player":"Player","market_value":"€M","slot_pos":"Position"},
        height=320,
        color_discrete_map={"GK":"#6e40c9","DF":"#1f6feb","MF":"#238636","FW":"#b83030"}
    )
    fig1.update_layout(
        paper_bgcolor="#161b22", plot_bgcolor="#161b22",
        font_color="#e6edf3", xaxis_tickangle=-40,
        legend_title_text="Pos"
    )

    # 2. Budget pie
    pos_val = df.groupby("slot_pos")["market_value"].sum().reset_index()
    fig2 = px.pie(
        pos_val, names="slot_pos", values="market_value",
        title="Budget Split by Position",
        color_discrete_map={"GK":"#6e40c9","DF":"#1f6feb","MF":"#238636","FW":"#b83030"},
        height=300,
    )
    fig2.update_layout(paper_bgcolor="#161b22", font_color="#e6edf3")

    # 3. Radar — FW vs DF
    cats = ["Goals","Assists","xG","SCA","Tackles","Interceptions"]
    fws  = df[df["slot_pos"]=="FW"]
    dfs  = df[df["slot_pos"]=="DF"]
    fig3 = go.Figure()
    for label, grp, color in [("Forwards",fws,"#b83030"),("Defenders",dfs,"#1f6feb")]:
        if grp.empty: continue
        vals = [grp["goals"].mean(), grp["assists"].mean(), grp["xg"].mean(),
                grp["sca"].mean(),   grp["tackles"].mean(), grp["interceptions"].mean()]
        fig3.add_trace(go.Scatterpolar(
            r=vals+[vals[0]], theta=cats+[cats[0]],
            fill="toself", name=label, line_color=color
        ))
    fig3.update_layout(
        title="Avg Profile: FW vs DF",
        polar=dict(radialaxis=dict(visible=True,gridcolor="#30363d"),
                   angularaxis=dict(gridcolor="#30363d"),
                   bgcolor="#21262d"),
        paper_bgcolor="#161b22", font_color="#e6edf3",
        showlegend=True, height=320
    )

    # 4. Age distribution
    fig4 = px.histogram(
        df, x="age", color="slot_pos", nbins=10,
        title="Age Distribution",
        labels={"age":"Age","slot_pos":"Position"},
        color_discrete_map={"GK":"#6e40c9","DF":"#1f6feb","MF":"#238636","FW":"#b83030"},
        height=280,
    )
    fig4.update_layout(paper_bgcolor="#161b22", plot_bgcolor="#161b22",
                       font_color="#e6edf3")

    return [fig1, fig2, fig3, fig4]


# ─────────────────────────────────────────────────────────────────────────────
#  Parse user message for budget
# ─────────────────────────────────────────────────────────────────────────────
def extract_budget(text: str):
    m = re.search(
        r'(?:budget|cap|under|max|less\s+than)\s*(?:\w+\s+){0,2}[€$]?\s*(\d+(?:\.\d+)?)\s*[mM]?(?:illion)?',
        text, re.I
    )
    if m:
        val = float(m.group(1))
        return val
    return None


# ─────────────────────────────────────────────────────────────────────────────
#  Main pipeline function
# ─────────────────────────────────────────────────────────────────────────────
def run_squad_pipeline(criteria: str, budget, vs, df, llm, status_cb):
    status_cb("Retrieving candidates from FAISS vector store…")
    cands = {}
    for pos in ["GK","DF","MF","FW"]:
        cands[pos] = retrieve_candidates(vs, criteria, pos)

    status_cb("Applying squad constraints (23-player rule, position slots)…")
    squad, report = build_squad(cands, budget)

    status_cb("Generating LLM justifications…")
    narrative = llm_justify(squad, criteria, llm)

    status_cb("Building visualisations…")
    charts = make_charts(squad)

    return squad, report, narrative, charts


# ─────────────────────────────────────────────────────────────────────────────
#  Sidebar
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## Squad Builder")
    st.markdown("---")

    # API Key
    api_key_input = st.text_input(
        "OpenAI API Key",
        value=os.getenv("OPENAI_API_KEY",""),
        type="password",
        placeholder="sk-proj-..."
    )
    if api_key_input:
        st.session_state["api_key_ok"] = True

    # CSV Upload
    st.markdown("### Player Data")
    csv_file = st.file_uploader(
        "Upload FBRef CSV", type=["csv"],
        help="Upload your players_data-2024_2025.csv"
    )
    csv_path_input = st.text_input(
        "Or enter local path:",
        placeholder="/path/to/players_data-2024_2025.csv"
    )

    # Build index button
    if st.button("Load Data & Build Index", use_container_width=True):
        if not api_key_input:
            st.error("Please enter your OpenAI API Key first.")
        else:
            path = None
            if csv_file is not None:
                save_path = Path("uploaded_players.csv")
                save_path.write_bytes(csv_file.read())
                path = str(save_path)
            elif csv_path_input and os.path.exists(csv_path_input):
                path = csv_path_input

            if path:
                with st.spinner("Building FAISS index (1-2 min first run)…"):
                    try:
                        vs, emb, df = build_vector_store(path, api_key_input)
                        st.session_state["vector_store"] = vs
                        st.session_state["embeddings"]   = emb
                        st.session_state["players_df"]   = df
                        st.session_state["llm"] = ChatOpenAI(
                            model="gpt-4o-mini",
                            temperature=0.3,
                            openai_api_key=api_key_input
                        )
                        st.session_state["csv_loaded"] = True
                        st.success(f"{len(df):,} players loaded!")
                    except Exception as e:
                        st.error(f"Error: {e}")
            else:
                st.warning("Please provide a valid CSV path or upload a file.")

    st.markdown("---")

    # Status
    if st.session_state["csv_loaded"]:
        df = st.session_state["players_df"]
        st.markdown("### Dataset Stats")
        cols = st.columns(2)
        cols[0].metric("Players", f"{len(df):,}")
        cols[1].metric("Leagues", df["Comp"].nunique() if "Comp" in df.columns else "—")
        pos_counts = df["PrimaryPos"].value_counts()
        for pos, cnt in pos_counts.items():
            color = pos
            st.caption(f"{pos}: {cnt} players")

    st.markdown("---")
    st.markdown("### Quick Prompts")
    for qp in QUICK_PROMPTS:
        if st.button(qp, key=f"qp_{qp[:20]}", use_container_width=True):
            st.session_state["_pending_prompt"] = qp
            st.rerun()

    st.markdown("---")
    if st.button("Clear Chat", use_container_width=True):
        st.session_state["messages"]     = []
        st.session_state["last_squad"]   = None
        st.session_state["pipeline_ran"] = False
        st.rerun()


# ─────────────────────────────────────────────────────────────────────────────
#  Main content area
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("## World Cup 2026 — Dream Squad Builder")
st.markdown(
    "Chat with the AI to build your perfect 23-player squad. "
    "Describe your ideal players and let the pipeline do the rest."
)

# ── Welcome message ───────────────────────────────────────────────────────────
if not st.session_state["messages"]:
    st.session_state["messages"].append({
        "role": "assistant",
        "content": (
            "**Welcome to the WC 2026 Squad Builder!**\n\n"
            "Tell me what kind of squad you want to build. For example:\n\n"
            "- *\"Build me a squad with clinical strikers (xG > 10), creative midfielders "
            "with high assist rates, and fast defenders with many interceptions\"*\n\n"
            "- *\"I want a budget squad under €400M with the best young talent under 25\"*\n\n"
            "- *\"Defensive fortress — high save% keepers, dominant defenders, disciplined midfielders\"*\n\n"
            "**Before you start:** Load your player CSV and API key in the sidebar.\n\n"
            "Then just type your criteria below!"
        )
    })


# ── Render chat history ───────────────────────────────────────────────────────
chat_html = '<div class="chat-wrapper" id="chat-end">'
for msg in st.session_state["messages"]:
    role    = msg["role"]
    content = msg["content"]
    if role == "user":
        chat_html += f'<div class="msg-user">{content}</div>'
    elif role == "system":
        chat_html += f'<div class="msg-system">{content}</div>'
    else:
        # Convert markdown-ish bold/newlines for HTML
        html_content = (content
                        .replace("\n\n", "<br><br>")
                        .replace("\n", "<br>")
                        .replace("**", "<b>", 1))
        # Alternate closing bold
        while "**" in html_content:
            html_content = html_content.replace("**", "</b>", 1).replace("**", "<b>", 1)
        chat_html += f'<div class="msg-bot">{html_content}</div>'
chat_html += '</div>'

st.markdown(chat_html, unsafe_allow_html=True)

# Auto-scroll JS
st.markdown("""
<script>
const chatEnd = document.getElementById('chat-end');
if (chatEnd) chatEnd.scrollTop = chatEnd.scrollHeight;
</script>
""", unsafe_allow_html=True)

# ── Squad results (charts + table) ────────────────────────────────────────────
if st.session_state["last_squad"]:
    squad  = st.session_state["last_squad"]["squad"]
    charts = st.session_state["last_squad"]["charts"]
    report = st.session_state["last_squad"]["report"]

    with st.expander("Squad Analytics Dashboard", expanded=True):
        # Constraint badges
        badge_cols = st.columns(len(report))
        for i, line in enumerate(report):
            color = "#238636" if "[OK]" in line else "#b83030"
            badge_cols[i].markdown(
                f'<div style="background:{color};border-radius:8px;padding:6px 10px;'
                f'text-align:center;font-size:0.82rem;font-weight:600;">{line}</div>',
                unsafe_allow_html=True
            )

        st.markdown("<br>", unsafe_allow_html=True)

        # Stat summary cards
        sq_df = pd.DataFrame(squad)
        m1, m2, m3, m4, m5 = st.columns(5)
        m1.markdown(f'<div class="stat-card"><div class="stat-num">{len(squad)}</div><div class="stat-lbl">Players</div></div>', unsafe_allow_html=True)
        m2.markdown(f'<div class="stat-card"><div class="stat-num">€{sq_df["market_value"].sum():.0f}M</div><div class="stat-lbl">Total Value</div></div>', unsafe_allow_html=True)
        m3.markdown(f'<div class="stat-card"><div class="stat-num">{sq_df["goals"].mean():.1f}</div><div class="stat-lbl">Avg Goals</div></div>', unsafe_allow_html=True)
        m4.markdown(f'<div class="stat-card"><div class="stat-num">{sq_df["xg"].mean():.1f}</div><div class="stat-lbl">Avg xG</div></div>', unsafe_allow_html=True)
        m5.markdown(f'<div class="stat-card"><div class="stat-num">{sq_df["age"].mean():.1f}</div><div class="stat-lbl">Avg Age</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Charts grid
        c1, c2 = st.columns(2)
        c1.plotly_chart(charts[0], use_container_width=True)
        c2.plotly_chart(charts[1], use_container_width=True)
        c3, c4 = st.columns(2)
        c3.plotly_chart(charts[2], use_container_width=True)
        c4.plotly_chart(charts[3], use_container_width=True)

        # Player table
        st.markdown("### Selected Squad")
        pos_order = {"GK":0,"DF":1,"MF":2,"FW":3}
        sorted_squad = sorted(squad, key=lambda x: (pos_order.get(x["slot_pos"],9), -x["score"]))

        table_html = '<div style="background:#161b22;border-radius:10px;overflow:hidden;border:1px solid #30363d;">'
        table_html += '<div class="player-row" style="background:#21262d;font-weight:700;font-size:0.8rem;color:#8b949e;">'
        table_html += '<span style="width:50px">POS</span><span style="flex:1">PLAYER</span>'
        table_html += '<span style="width:120px">CLUB</span><span style="width:60px;text-align:right">GOALS</span>'
        table_html += '<span style="width:60px;text-align:right">AST</span><span style="width:60px;text-align:right">xG</span>'
        table_html += '<span style="width:70px;text-align:right">SCORE</span><span style="width:70px;text-align:right">€M</span></div>'

        for p in sorted_squad:
            pos   = p["slot_pos"]
            badge = f'<span class="pos-badge pos-{pos}">{pos}</span>'
            table_html += (
                f'<div class="player-row">'
                f'{badge}'
                f'<span style="flex:1;font-weight:600">{p["player"]}</span>'
                f'<span style="width:120px;color:#8b949e;font-size:0.83rem">{p["squad"]}</span>'
                f'<span style="width:60px;text-align:right">{int(p["goals"])}</span>'
                f'<span style="width:60px;text-align:right">{int(p["assists"])}</span>'
                f'<span style="width:60px;text-align:right">{p["xg"]:.1f}</span>'
                f'<span style="width:70px;text-align:right;color:#58a6ff">{p["score"]:.1f}</span>'
                f'<span style="width:70px;text-align:right;color:#3fb950">€{p["market_value"]:.1f}M</span>'
                f'</div>'
            )
        table_html += '</div>'
        st.markdown(table_html, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
#  Input area
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("---")

# Handle quick-prompt injection — reset last_processed so it can fire
if "_pending_prompt" in st.session_state:
    pending = st.session_state.pop("_pending_prompt")
    st.session_state["_prefill"] = pending
    st.session_state["last_processed"] = ""  # allow this new prompt to process

col_input, col_send = st.columns([9, 1])

with col_input:
    prefill = st.session_state.pop("_prefill", "")
    user_input = st.text_input(
        label="",
        value=prefill,
        placeholder="Describe your dream squad… e.g. 'clinical strikers with xG > 10, fast defenders'",
        key="chat_input",
        label_visibility="collapsed",
    )

with col_send:
    send_clicked = st.button("Send", use_container_width=True)


# ─────────────────────────────────────────────────────────────────────────────
#  Process user message
# ─────────────────────────────────────────────────────────────────────────────
# Only process once per click/enter using a "already processed" guard
if "last_processed" not in st.session_state:
    st.session_state["last_processed"] = ""

should_process = (
    send_clicked and
    user_input.strip() and
    user_input.strip() != st.session_state["last_processed"]
)

if should_process:
    user_text = user_input.strip()

    # Mark this input as processed so it won't fire again on rerun
    st.session_state["last_processed"] = user_text

    # Append user message
    st.session_state["messages"].append({"role": "user", "content": user_text})

    # Check if data is loaded
    if not st.session_state["csv_loaded"]:
        st.session_state["messages"].append({
            "role": "assistant",
            "content": (
                "**Data not loaded yet!**\n\n"
                "Please go to the sidebar and:\n"
                "1. Enter your **OpenAI API Key**\n"
                "2. Upload your **FBRef CSV** or provide a local path\n"
                "3. Click **Load Data & Build Index**\n\n"
                "Then try your prompt again!"
            )
        })
        st.rerun()

    # Detect intent — conversation or squad build
    build_keywords = ["build","squad","select","choose","find","create","make","want","give me",
                      "striker","defender","midfielder","goalkeeper","forward","clinical","fast",
                      "xg","assists","goals","creative","dominant","budget","cap","pressing","aerial"]
    is_build = any(kw in user_text.lower() for kw in build_keywords)

    if is_build:
        budget = extract_budget(user_text)
        budget_note = f"€{budget:.0f}M cap" if budget else "No budget limit"

        # Show typing indicator
        with st.spinner("Building your squad… (this may take 30-60 seconds)"):
            status_msgs = []
            def status_cb(msg):
                status_msgs.append(msg)

            try:
                squad, report, narrative, charts = run_squad_pipeline(
                    criteria  = user_text,
                    budget    = budget,
                    vs        = st.session_state["vector_store"],
                    df        = st.session_state["players_df"],
                    llm       = st.session_state["llm"],
                    status_cb = status_cb,
                )

                st.session_state["last_squad"] = {
                    "squad":     squad,
                    "report":    report,
                    "narrative": narrative,
                    "charts":    charts,
                }

                total_val = sum(p["market_value"] for p in squad)
                constraint_summary = " · ".join(report)

                bot_reply = (
                    f"**Squad built successfully!** ({len(squad)} players · €{total_val:.0f}M)\n\n"
                    f"**Constraints:** {constraint_summary}\n\n"
                    f"**Budget:** {budget_note}\n\n"
                    f"---\n\n"
                    f"{narrative}\n\n"
                    f"---\n"
                    f"*Scroll down to see the full analytics dashboard below.*"
                )

            except Exception as e:
                bot_reply = f"**Pipeline error:** `{e}`\n\nPlease check your API key and CSV file."

    else:
        # General conversation — use LLM directly
        try:
            llm  = st.session_state["llm"]
            resp = llm.invoke(
                f"You are a football analytics expert assistant for a World Cup 2026 squad builder app. "
                f"Answer this question concisely: {user_text}"
            )
            bot_reply = resp.content if hasattr(resp,"content") else str(resp)
        except Exception as e:
            bot_reply = (
                f"I can help you build your dream squad! Try asking me to:\n\n"
                f"- *\"Build a squad with clinical strikers and fast defenders\"*\n"
                f"- *\"Give me a budget squad under €400M\"*\n"
                f"- *\"Select the best young midfielders with high progressive passes\"*"
            )

    st.session_state["messages"].append({"role": "assistant", "content": bot_reply})
    st.rerun()
import streamlit as st
import re

# ─── Page Config ──────────────────────────────────────────────
st.set_page_config(
    page_title="DeepResearch · AI Multi-Agent Research",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CSS ──────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=DM+Sans:ital,wght@0,400;0,500;0,700;1,400&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    /* ── Fiery palette ── */
    --ember:       #e8530e;
    --flame:       #ff6a1a;
    --molten:      #ff9234;
    --gold:        #ffb740;
    --sun:         #ffd97a;
    --crimson:     #c9290e;
    --cherry:      #9e1b0e;

    /* ── Darks — warm tinted ── */
    --void:        #0b0a08;
    --deep:        #111010;
    --surface:     #1a1815;
    --surface-2:   #232019;
    --surface-3:   #2e2a21;
    --border:      rgba(232, 83, 14, 0.12);
    --border-warm: rgba(255, 146, 52, 0.10);

    /* ── Text — warm whites ── */
    --text:        #f0ebe4;
    --text-2:      #c4b9a8;
    --text-dim:    #8a7e6d;
    --text-muted:  #5e554a;

    /* ── Glows ── */
    --glow-ember:  0 0 40px rgba(232,83,14,0.12), 0 0 80px rgba(232,83,14,0.04);
    --glow-gold:   0 0 30px rgba(255,183,64,0.10);
}

/* ═══ RESET ═══ */
html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    font-family: 'DM Sans', -apple-system, sans-serif !important;
    background: var(--void) !important;
    color: var(--text) !important;
}
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stMainBlockContainer"] { padding-top: 0; position: relative; z-index: 1; }
#MainMenu, footer { visibility: hidden; }

/* ── Warm ambient glow on page ── */
[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    top: -20%;
    left: -10%;
    width: 60%;
    height: 70%;
    background: radial-gradient(ellipse at center, rgba(232,83,14,0.04) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
}
[data-testid="stAppViewContainer"]::after {
    content: '';
    position: fixed;
    bottom: -30%;
    right: -15%;
    width: 70%;
    height: 60%;
    background: radial-gradient(ellipse at center, rgba(255,146,52,0.03) 0%, transparent 70%);
    pointer-events: none;
    z-index: 0;
}

/* ═══ SIDEBAR ═══ */
section[data-testid="stSidebar"] {
    background: var(--deep) !important;
    border-right: 1px solid var(--border) !important;
}
section[data-testid="stSidebar"] * { color: var(--text) !important; }

.sb-brand {
    padding: 0.25rem 0 0.5rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1.25rem;
}
.sb-name {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.35rem;
    font-weight: 700;
    letter-spacing: -0.3px;
    color: var(--text) !important;
}
.sb-name span {
    color: var(--ember) !important;
}
.sb-tag {
    font-size: 0.7rem;
    color: var(--text-dim) !important;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: 2px;
}

/* Agent list in sidebar */
.ag-item {
    display: flex;
    align-items: center;
    gap: 0.65rem;
    padding: 0.5rem 0.6rem;
    border-radius: 8px;
    margin-bottom: 0.25rem;
    transition: background 0.25s ease;
    cursor: default;
}
.ag-item:hover { background: var(--surface); }
.ag-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    flex-shrink: 0;
}
.ag-label {
    font-size: 0.82rem;
    font-weight: 500;
    color: var(--text-2) !important;
}
.ag-label strong { color: var(--text) !important; font-weight: 600; }

.sb-tech {
    display: flex;
    flex-wrap: wrap;
    gap: 0.3rem;
    margin-top: 0.25rem;
}
.sb-chip {
    font-size: 0.65rem;
    font-weight: 500;
    padding: 0.18rem 0.55rem;
    border-radius: 4px;
    background: var(--surface);
    border: 1px solid var(--border);
    color: var(--text-dim) !important;
    letter-spacing: 0.3px;
}

/* ═══ HERO ═══ */
.hero {
    padding: 3rem 0 1.5rem;
    max-width: 740px;
}
.hero-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    font-weight: 500;
    color: var(--ember);
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 0.75rem;
}
.hero h1 {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 3rem;
    font-weight: 700;
    letter-spacing: -1.5px;
    line-height: 1.05;
    color: var(--text);
    margin: 0 0 0.75rem;
}
.hero h1 em {
    font-style: normal;
    background: linear-gradient(135deg, var(--ember) 0%, var(--flame) 40%, var(--molten) 70%, var(--gold) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero p {
    font-size: 1.05rem;
    line-height: 1.7;
    color: var(--text-2);
    margin: 0;
    max-width: 560px;
}

/* ═══ TABS — minimal underline style ═══ */
.stTabs [data-baseweb="tab-list"] {
    gap: 0;
    background: transparent !important;
    border-bottom: 1px solid var(--border) !important;
    padding: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--text-dim) !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
    padding: 0.7rem 1.5rem !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    border-radius: 0 !important;
    transition: all 0.25s ease !important;
}
.stTabs [data-baseweb="tab"]:hover {
    color: var(--text-2) !important;
}
.stTabs [aria-selected="true"] {
    color: var(--ember) !important;
    border-bottom: 2px solid var(--ember) !important;
    background: transparent !important;
}
.stTabs [data-baseweb="tab-border"],
.stTabs [data-baseweb="tab-highlight"] { display: none !important; }

/* ═══ TEXT INPUT ═══ */
.stTextInput input {
    background: var(--surface) !important;
    color: var(--text) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    padding: 0.8rem 1rem !important;
    font-size: 1rem !important;
    font-family: 'DM Sans', sans-serif !important;
    caret-color: var(--ember) !important;
    transition: border-color 0.25s ease, box-shadow 0.25s ease !important;
}
.stTextInput input:focus {
    border-color: var(--ember) !important;
    box-shadow: 0 0 0 3px rgba(232,83,14,0.08) !important;
}
.stTextInput input::placeholder { color: var(--text-muted) !important; }

/* ═══ TEXT AREA ═══ */
.stTextArea textarea {
    background: var(--surface) !important;
    color: var(--text) !important;
    border: 1px solid var(--border) !important;
    border-radius: 8px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.92rem !important;
    line-height: 1.7 !important;
    caret-color: var(--ember) !important;
    transition: border-color 0.25s ease !important;
}
.stTextArea textarea:focus {
    border-color: var(--ember) !important;
    box-shadow: 0 0 0 3px rgba(232,83,14,0.08) !important;
}

/* ═══ BUTTONS ═══ */
.stButton > button {
    background: var(--ember) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.7rem 2rem !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.92rem !important;
    letter-spacing: 0.2px;
    transition: all 0.3s ease !important;
    box-shadow: 0 2px 12px rgba(232,83,14,0.20) !important;
}
.stButton > button:hover {
    background: var(--flame) !important;
    box-shadow: 0 4px 24px rgba(232,83,14,0.30) !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

.stDownloadButton > button {
    background: transparent !important;
    color: var(--ember) !important;
    border: 1px solid var(--ember) !important;
    border-radius: 8px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    box-shadow: none !important;
    transition: all 0.25s ease !important;
}
.stDownloadButton > button:hover {
    background: rgba(232,83,14,0.08) !important;
    box-shadow: 0 2px 12px rgba(232,83,14,0.12) !important;
}

/* ═══ STATUS CONTAINERS ═══ */
[data-testid="stStatusWidget"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
}

/* ═══ PIPELINE TRACKER ═══ */
.tracker {
    display: flex;
    align-items: stretch;
    gap: 0;
    margin: 1.5rem 0 1rem;
    border: 1px solid var(--border);
    border-radius: 10px;
    overflow: hidden;
    background: var(--deep);
}
.tracker-step {
    flex: 1;
    padding: 0.75rem 0.6rem;
    text-align: center;
    border-right: 1px solid var(--border);
    transition: background 0.4s ease;
    position: relative;
}
.tracker-step:last-child { border-right: none; }

.tracker-step .t-num {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.62rem;
    font-weight: 500;
    color: var(--text-muted);
    letter-spacing: 1px;
    text-transform: uppercase;
    display: block;
    margin-bottom: 0.2rem;
}
.tracker-step .t-name {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.78rem;
    font-weight: 600;
    color: var(--text-dim);
    display: block;
}
.tracker-step .t-dot {
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--text-muted);
    display: inline-block;
    margin-top: 0.4rem;
    transition: all 0.3s ease;
}

/* States */
.tracker-step.active {
    background: rgba(232,83,14,0.06);
}
.tracker-step.active .t-name { color: var(--ember); }
.tracker-step.active .t-num  { color: var(--ember); }
.tracker-step.active .t-dot  {
    background: var(--ember);
    box-shadow: 0 0 8px rgba(232,83,14,0.5);
    animation: throb 1.5s ease-in-out infinite;
}

.tracker-step.done {
    background: rgba(232,83,14,0.03);
}
.tracker-step.done .t-name { color: var(--molten); }
.tracker-step.done .t-num  { color: var(--text-dim); }
.tracker-step.done .t-dot  {
    background: var(--molten);
    box-shadow: 0 0 6px rgba(255,146,52,0.3);
}

@keyframes throb {
    0%, 100% { transform: scale(1); opacity: 1; }
    50%      { transform: scale(1.8); opacity: 0.6; }
}

/* ═══ REPORT CARD ═══ */
.report-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 2rem;
    margin: 1rem 0;
    line-height: 1.85;
    font-size: 0.95rem;
    color: var(--text-2);
    max-height: 550px;
    overflow-y: auto;
    position: relative;
}
.report-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 3px;
    height: 100%;
    background: linear-gradient(180deg, var(--ember), var(--gold), transparent);
    border-radius: 10px 0 0 10px;
}

/* ═══ SECTION HEADING ═══ */
.sec-heading {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin: 2.5rem 0 1rem;
}
.sec-heading .sec-line {
    flex: 1;
    height: 1px;
    background: var(--border);
}
.sec-heading .sec-label {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.75rem;
    font-weight: 600;
    color: var(--text-dim);
    letter-spacing: 2px;
    text-transform: uppercase;
    white-space: nowrap;
}

/* ═══ SCORE DISPLAY ═══ */
.score-block {
    text-align: center;
    padding: 1.5rem 1rem;
}
.score-num {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 3.5rem;
    font-weight: 700;
    line-height: 1;
    background: linear-gradient(135deg, var(--ember), var(--gold));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.score-denom {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.2rem;
    font-weight: 500;
    color: var(--text-muted);
    margin-left: 2px;
}
.score-bar {
    width: 80%;
    max-width: 160px;
    height: 4px;
    background: var(--surface-2);
    border-radius: 2px;
    margin: 0.75rem auto 0.5rem;
    overflow: hidden;
}
.score-bar-fill {
    height: 100%;
    border-radius: 2px;
    background: linear-gradient(90deg, var(--crimson), var(--ember), var(--gold));
    transition: width 1.2s cubic-bezier(0.4, 0, 0.2, 1);
}
.score-caption {
    font-size: 0.7rem;
    color: var(--text-muted);
    letter-spacing: 1.5px;
    text-transform: uppercase;
    font-weight: 500;
}

/* ═══ FEEDBACK COLUMNS ═══ */
.fb-box {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 1.1rem;
}
.fb-box.good { border-top: 2px solid var(--molten); }
.fb-box.warn { border-top: 2px solid var(--cherry); }

.fb-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 0.65rem;
}
.fb-title.good { color: var(--molten); }
.fb-title.warn { color: var(--cherry); }

.fb-item {
    font-size: 0.87rem;
    color: var(--text-2);
    padding: 0.35rem 0 0.35rem 0.75rem;
    border-left: 2px solid var(--surface-3);
    margin-bottom: 0.35rem;
    line-height: 1.5;
}

.verdict-bar {
    background: var(--surface);
    border: 1px solid var(--border);
    border-left: 3px solid var(--ember);
    border-radius: 0 8px 8px 0;
    padding: 0.85rem 1.1rem;
    margin-top: 1rem;
    font-size: 0.95rem;
    font-style: italic;
    color: var(--text-2);
}

/* ═══ PASTE SECTION ═══ */
.paste-header {
    padding: 2rem 0 0.5rem;
}
.paste-header h2 {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.5rem;
    font-weight: 700;
    letter-spacing: -0.5px;
    color: var(--text);
    margin: 0 0 0.35rem;
}
.paste-header p {
    font-size: 0.95rem;
    color: var(--text-dim);
    margin: 0;
    line-height: 1.6;
}

/* ═══ EXPANDER ═══ */
.streamlit-expanderHeader {
    background: var(--surface) !important;
    color: var(--text-2) !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
    font-size: 0.85rem !important;
}

/* ═══ SCROLLBAR ═══ */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--surface-3); border-radius: 2px; }
::-webkit-scrollbar-thumb:hover { background: var(--text-muted); }
</style>
""", unsafe_allow_html=True)


# ─── SIDEBAR ──────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="sb-brand">
        <div class="sb-name">deep<span>research</span></div>
        <div class="sb-tag">Multi-Agent System</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### Agents")
    agents = [
        ("var(--ember)",  "Search",  "Tavily API"),
        ("var(--flame)",  "Reader",  "Web Scraper"),
        ("var(--molten)", "Writer",  "LLM Report"),
        ("var(--gold)",   "Critic",  "Quality Review"),
    ]
    for color, name, desc in agents:
        st.markdown(f"""
        <div class="ag-item">
            <div class="ag-dot" style="background:{color};box-shadow:0 0 6px {color};"></div>
            <div class="ag-label"><strong>{name}</strong> · {desc}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(
        '<div style="font-size:0.72rem;color:var(--text-muted);letter-spacing:1px;'
        'text-transform:uppercase;margin-bottom:0.5rem;font-weight:600;">Stack</div>',
        unsafe_allow_html=True,
    )
    st.markdown("""
    <div class="sb-tech">
        <span class="sb-chip">LangChain</span>
        <span class="sb-chip">Groq</span>
        <span class="sb-chip">Tavily</span>
        <span class="sb-chip">Streamlit</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(
        '<div style="font-size:0.72rem;color:var(--text-muted);letter-spacing:1px;'
        'text-transform:uppercase;margin-bottom:0.5rem;font-weight:600;">Models (auto-fallback)</div>',
        unsafe_allow_html=True,
    )
    from agents import MODELS
    for i, m in enumerate(MODELS):
        tag = "primary" if i == 0 else f"fallback {i}"
        color = "var(--ember)" if i == 0 else "var(--text-dim)"
        st.markdown(
            f'<div class="ag-item" style="padding:0.3rem 0.6rem;">'
            f'<div class="ag-dot" style="background:{color};width:6px;height:6px;"></div>'
            f'<div class="ag-label" style="font-size:0.75rem;">'
            f'<strong style="font-family:JetBrains Mono,monospace;font-size:0.7rem;">{m}</strong>'
            f' <span style="color:var(--text-muted);font-size:0.65rem;">· {tag}</span></div></div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")
    if st.button("↻  Reset", use_container_width=True):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()


# ─── HELPERS ──────────────────────────────────────────────────

STEPS = [
    ("01", "Search"),
    ("02", "Reader"),
    ("03", "Writer"),
    ("04", "Critic"),
]

def render_tracker(current: int, done_all: bool = False):
    """Horizontal tracker bar. current = 0-indexed active step."""
    cells = ""
    for i, (num, name) in enumerate(STEPS):
        if done_all or i < current:
            cls = "done"
        elif i == current:
            cls = "active"
        else:
            cls = ""
        cells += (
            f'<div class="tracker-step {cls}">'
            f'<span class="t-num">Step {num}</span>'
            f'<span class="t-name">{name}</span>'
            f'<span class="t-dot"></span>'
            f'</div>'
        )
    st.markdown(f'<div class="tracker">{cells}</div>', unsafe_allow_html=True)


def section_heading(label: str):
    st.markdown(
        f'<div class="sec-heading">'
        f'<div class="sec-line"></div>'
        f'<div class="sec-label">{label}</div>'
        f'<div class="sec-line"></div>'
        f'</div>',
        unsafe_allow_html=True,
    )


def parse_critic(text: str) -> dict:
    result = {"score": None, "strengths": [], "improve": [], "verdict": None, "raw": text}
    m = re.search(r"score\s*:\s*(\d+(?:\.\d+)?)\s*/\s*10", text, re.IGNORECASE)
    if m:
        result["score"] = m.group(1)
    sections = re.split(
        r"\n(?=(?:strengths|areas?\s+to\s+improve|one[- ]line\s+verdict)\s*:)",
        text, flags=re.IGNORECASE,
    )
    for sec in sections:
        low = sec.strip().lower()
        bullets = re.findall(r"[-•]\s*(.+)", sec)
        if low.startswith("strength"):
            result["strengths"] = bullets
        elif low.startswith("area"):
            result["improve"] = bullets
        elif "verdict" in low[:25]:
            parts = sec.split(":", 1)
            if len(parts) > 1:
                result["verdict"] = parts[1].strip().strip("-•").strip()
    return result


def render_score(parsed: dict):
    """Render score block + feedback columns."""
    col_s, col_fb = st.columns([1, 2.5])

    with col_s:
        score = parsed["score"] or "–"
        pct = 0
        try:
            pct = float(parsed["score"]) * 10
        except (TypeError, ValueError):
            pass
        st.markdown(f"""
        <div class="score-block">
            <div>
                <span class="score-num">{score}</span><span class="score-denom">/10</span>
            </div>
            <div class="score-bar"><div class="score-bar-fill" style="width:{pct}%;"></div></div>
            <div class="score-caption">Quality Score</div>
        </div>
        """, unsafe_allow_html=True)

    with col_fb:
        c1, c2 = st.columns(2)
        with c1:
            items = ""
            if parsed["strengths"]:
                for s in parsed["strengths"]:
                    items += f'<div class="fb-item">{s}</div>'
            else:
                items = '<div class="fb-item" style="color:var(--text-muted);">See raw output</div>'
            st.markdown(
                f'<div class="fb-box good">'
                f'<div class="fb-title good">Strengths</div>{items}</div>',
                unsafe_allow_html=True,
            )
        with c2:
            items = ""
            if parsed["improve"]:
                for s in parsed["improve"]:
                    items += f'<div class="fb-item">{s}</div>'
            else:
                items = '<div class="fb-item" style="color:var(--text-muted);">See raw output</div>'
            st.markdown(
                f'<div class="fb-box warn">'
                f'<div class="fb-title warn">Improve</div>{items}</div>',
                unsafe_allow_html=True,
            )

    if parsed["verdict"]:
        st.markdown(f'<div class="verdict-bar">"{parsed["verdict"]}"</div>', unsafe_allow_html=True)


# ─── HERO ─────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-label">// multi-agent research pipeline</div>
    <h1>Research that<br><em>thinks for itself.</em></h1>
    <p>Four AI agents — search, read, write, critique — working together
    to deliver deep, reliable research reports from a single topic.</p>
</div>
""", unsafe_allow_html=True)


# ─── TABS ─────────────────────────────────────────────────────
tab_research, tab_critic = st.tabs(["Research Pipeline", "Critic Review"])


# ═══ TAB 1 — RESEARCH ════════════════════════════════════════
with tab_research:
    topic = st.text_input(
        "topic",
        placeholder="What do you want to research? e.g. Quantum computing breakthroughs 2026",
        key="topic_input",
        label_visibility="collapsed",
    )

    col_go, col_spacer = st.columns([1, 3])
    with col_go:
        start = st.button("Run Pipeline →", disabled=not topic, use_container_width=True)

    if start and topic:
        st.session_state["pipe"] = {}
        st.session_state["pipe_done"] = False
        st.session_state["pipe_topic"] = topic
        state = st.session_state["pipe"]

        from agents import build_search_agent, build_reader_agent, writer_chain, Critic_chain

        tracker_ph = st.empty()
        output = st.container()

        try:
            # Step 1 — Search
            with tracker_ph.container():
                render_tracker(0)
            with output:
                with st.status("Search Agent — finding sources…", expanded=True) as s:
                    agent = build_search_agent()
                    res = agent.invoke({
                        "messages": [{"role": "user", "content": f"Find recent, reliable and detailed information about: {topic}"}]
                    })
                    state["search"] = res["messages"][-1].content
                    s.update(label="Search Agent — done", state="complete", expanded=False)
                    st.markdown(state["search"][:2000])

            # Step 2 — Reader
            with tracker_ph.container():
                render_tracker(1)
            with output:
                with st.status("Reader Agent — scraping content…", expanded=True) as s:
                    agent = build_reader_agent()
                    res = agent.invoke({
                        "messages": [{
                            "role": "user",
                            "content": (
                                f"Based on the following search results about '{topic}', "
                                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                                f"Search Results:\n{state['search'][:800]}"
                            ),
                        }]
                    })
                    state["scraped"] = res["messages"][-1].content
                    s.update(label="Reader Agent — done", state="complete", expanded=False)
                    st.markdown(state["scraped"][:2000])

            # Step 3 — Writer
            with tracker_ph.container():
                render_tracker(2)
            with output:
                with st.status("Writer — drafting report…", expanded=True) as s:
                    combined = (
                        f"SEARCH RESULTS :\n{state['search'][:3000]}\n\n"
                        f"DETAILED SCRAPED CONTENT :\n{state['scraped'][:3000]}"
                    )
                    state["report"] = writer_chain.invoke({"topic": topic, "research": combined})
                    s.update(label="Writer — done", state="complete", expanded=False)
                    st.markdown(state["report"][:800] + "…")

            # Step 4 — Critic
            with tracker_ph.container():
                render_tracker(3)
            with output:
                with st.status("Critic — reviewing report…", expanded=True) as s:
                    state["feedback"] = Critic_chain.invoke({"report": state["report"]})
                    s.update(label="Critic — done", state="complete", expanded=False)

            with tracker_ph.container():
                render_tracker(4, done_all=True)
            st.session_state["pipe_done"] = True

        except Exception as e:
            st.error(f"Pipeline error: {e}")
            st.exception(e)

    # ── Persisted results ──
    if st.session_state.get("pipe_done"):
        state = st.session_state["pipe"]
        t = st.session_state.get("pipe_topic", "research")

        section_heading("Research Report")
        st.markdown(f'<div class="report-card">{state["report"]}</div>', unsafe_allow_html=True)

        st.download_button(
            "↓  Download as Markdown",
            data=state["report"],
            file_name=f"deepresearch_{t.replace(' ', '_')[:30]}.md",
            mime="text/markdown",
        )

        section_heading("Critic Review")
        parsed = parse_critic(state["feedback"])
        render_score(parsed)

        with st.expander("Raw critic output"):
            st.code(state["feedback"], language=None)


# ═══ TAB 2 — CRITIC REVIEW ═══════════════════════════════════
with tab_critic:
    st.markdown("""
    <div class="paste-header">
        <h2>Instant Critique</h2>
        <p>Paste any report — your own or AI-generated — and the critic agent
        will score it, surface strengths, and flag weak spots.</p>
    </div>
    """, unsafe_allow_html=True)

    user_report = st.text_area(
        "report",
        height=260,
        placeholder="Paste the full report text here…",
        key="critic_paste",
        label_visibility="collapsed",
    )

    col1, col2, col3 = st.columns([1.2, 1, 1.2])
    with col2:
        go_critic = st.button("Analyze →", disabled=not user_report, key="critic_btn", use_container_width=True)

    if go_critic and user_report:
        from agents import Critic_chain
        with st.status("Critic analyzing…", expanded=True) as sc:
            try:
                fb = Critic_chain.invoke({"report": user_report})
                st.session_state["solo_fb"] = fb
                sc.update(label="Analysis complete", state="complete", expanded=False)
            except Exception as e:
                sc.update(label="Failed", state="error")
                st.error(f"Error: {e}")

    if st.session_state.get("solo_fb"):
        section_heading("Critic Feedback")
        parsed = parse_critic(st.session_state["solo_fb"])
        render_score(parsed)
        with st.expander("Raw critic output"):
            st.code(st.session_state["solo_fb"], language=None)

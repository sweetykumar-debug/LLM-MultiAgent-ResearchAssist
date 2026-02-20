import streamlit as st
import ast


# ── Helper ────────────────────────────────────────────────────────────────────
def parse_terms(terms_str: str):
    try:
        return ast.literal_eval(terms_str)
    except:
        return []


# ══════════════════════════════════════════════════════════════════════════════
# 1. CSS
# ══════════════════════════════════════════════════════════════════════════════
def inject_css():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Google+Sans:wght@400;500;700&family=Roboto:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Roboto', sans-serif;
    background: #0f1117;
    color: #e8eaed;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #1a1c23 !important;
    border-right: 1px solid #2d2f3a;
    width: 260px !important;
}
section[data-testid="stSidebar"] .block-container { padding: 1rem !important; }

/* ── Top bar ── */
.top-bar {
    position: fixed; top: 0; left: 260px; right: 0; z-index: 999;
    background: #0f1117;
    border-bottom: 1px solid #2d2f3a;
    display: flex; align-items: center; justify-content: space-between;
    padding: 12px 32px;
    height: 60px;
}
.top-bar .logo {
    display: flex; align-items: center; gap: 10px;
    font-family: 'Google Sans', sans-serif;
    font-size: 22px; font-weight: 700;
    background: linear-gradient(135deg, #4285f4, #34a853, #fbbc04, #ea4335);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
}
.top-bar .badge {
    background: linear-gradient(135deg, #4285f4, #6c47ff);
    color: white; padding: 4px 12px; border-radius: 20px;
    font-size: 11px; font-weight: 600; letter-spacing: 0.5px;
}

/* ── Sidebar typography ── */
.sidebar-title {
    font-family: 'Google Sans', sans-serif;
    font-size: 13px; font-weight: 700; color: #9aa0a6;
    text-transform: uppercase; letter-spacing: 1px;
    padding: 8px 0 4px 0; margin-top: 12px;
}
.chat-history-item {
    padding: 8px 12px; border-radius: 10px;
    color: #bdc1c6; font-size: 13px;
    cursor: pointer; margin: 2px 0;
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}

/* ── Welcome screen ── */
.welcome-wrap {
    display: flex; flex-direction: column; align-items: center;
    justify-content: center; height: 65vh; text-align: center; gap: 16px;
}
.welcome-logo {
    font-family: 'Google Sans', sans-serif; font-size: 42px; font-weight: 700;
    background: linear-gradient(135deg, #4285f4, #34a853, #fbbc04, #ea4335);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin-bottom: 8px;
}
.welcome-sub { color: #9aa0a6; font-size: 17px; max-width: 520px; line-height: 1.6; }
.suggestion-chips { display: flex; flex-wrap: wrap; gap: 10px; justify-content: center; margin-top: 8px; }
.chip {
    background: #1e2030; border: 1px solid #3c4043;
    border-radius: 20px; padding: 10px 18px;
    color: #bdc1c6; font-size: 13px; cursor: pointer;
    transition: all 0.2s;
}

/* ── Badges ── */
.research-badge {
    display: inline-flex; align-items: center; gap: 6px;
    background: rgba(66,133,244,0.15); color: #8ab4f8;
    border: 1px solid rgba(66,133,244,0.3);
    padding: 3px 10px; border-radius: 20px; font-size: 11px;
    font-weight: 600; margin-bottom: 10px; letter-spacing: 0.5px;
}
.dataset-badge {
    display: inline-flex; align-items: center; gap: 6px;
    background: rgba(52,168,83,0.15); color: #81c995;
    border: 1px solid rgba(52,168,83,0.3);
    padding: 3px 10px; border-radius: 20px; font-size: 11px;
    font-weight: 600; margin-bottom: 10px; letter-spacing: 0.5px;
}

/* ── INPUT BAR ── */
.input-wrapper {
    position: fixed;
    bottom: 0; left: 260px; right: 0;
    z-index: 998;
    background: linear-gradient(to top, #0f1117 85%, transparent);
    padding: 0 15% 20px 15%;
}
.filter-chips-row {
    display: flex; gap: 8px; margin-bottom: 10px;
    flex-wrap: wrap; align-items: center;
}
.filter-chip {
    display: inline-flex; align-items: center; gap: 5px;
    background: #1a1c23; border: 1px solid #3c4043;
    border-radius: 20px; padding: 5px 14px;
    color: #9aa0a6; font-size: 12px; font-weight: 500;
    cursor: pointer; transition: all 0.2s;
    user-select: none; white-space: nowrap;
}
.filter-chip.active { background: rgba(66,133,244,0.18); border-color: #4285f4; color: #8ab4f8; }
.filter-chip:hover  { border-color: #4285f4; color: #8ab4f8; }

.search-input-box {
    display: flex; align-items: center;
    background: #1a1c23; border: 1.5px solid #3c4043;
    border-radius: 32px; padding: 6px 8px 6px 20px;
    gap: 8px; box-shadow: 0 4px 24px rgba(0,0,0,0.4);
    transition: border 0.2s, box-shadow 0.2s;
}
.search-input-box:focus-within {
    border-color: #4285f4;
    box-shadow: 0 4px 24px rgba(66,133,244,0.18);
}
.search-input-box textarea {
    flex: 1; background: transparent !important; border: none !important;
    outline: none !important; color: #e8eaed !important;
    font-size: 15px !important; font-family: 'Roboto', sans-serif !important;
    resize: none !important; line-height: 1.6 !important;
    padding: 6px 0 !important; min-height: 28px; max-height: 120px;
}

[data-testid="stChatInput"] {
    background: #1a1c23 !important; border: 1.5px solid #3c4043 !important;
    border-radius: 32px !important; box-shadow: 0 4px 24px rgba(0,0,0,0.4) !important;
    padding: 4px 4px 4px 16px !important;
    transition: border 0.2s, box-shadow 0.2s !important;
}
[data-testid="stChatInput"]:focus-within {
    border-color: #4285f4 !important;
    box-shadow: 0 4px 24px rgba(66,133,244,0.2) !important;
}
[data-testid="stChatInput"] textarea {
    background: transparent !important; border: none !important;
    color: #e8eaed !important; font-size: 15px !important;
    font-family: 'Roboto', sans-serif !important; padding: 10px 8px !important;
}
[data-testid="stChatInput"] textarea::placeholder { color: #5f6368 !important; }
[data-testid="stChatInputSubmitButton"] button {
    background: linear-gradient(135deg, #4285f4, #6c47ff) !important;
    border-radius: 50% !important; width: 40px !important; height: 40px !important;
    border: none !important; box-shadow: 0 2px 8px rgba(66,133,244,0.4) !important;
}
[data-testid="stChatInputSubmitButton"] button:hover {
    opacity: 0.88 !important; transform: scale(1.05) !important;
}

.input-toolbar {
    display: flex; align-items: center; justify-content: space-between;
    padding: 0 4px; margin-bottom: 8px;
}
.toolbar-left  { display: flex; gap: 6px; align-items: center; }
.toolbar-right { display: flex; gap: 6px; align-items: center; }
.toolbar-btn {
    display: inline-flex; align-items: center; gap: 5px;
    background: transparent; border: 1px solid #2d2f3a;
    border-radius: 16px; padding: 4px 12px;
    color: #9aa0a6; font-size: 12px; cursor: pointer;
    transition: all 0.15s; user-select: none;
}
.toolbar-btn:hover  { background: rgba(255,255,255,0.05); border-color: #5f6368; color: #bdc1c6; }
.toolbar-btn.active { background: rgba(66,133,244,0.12); border-color: rgba(66,133,244,0.5); color: #8ab4f8; }
.toolbar-dot {
    width: 6px; height: 6px; border-radius: 50%;
    background: #34a853; display: inline-block;
    animation: pulse 2s infinite;
}
@keyframes pulse { 0%,100% { opacity:1; } 50% { opacity:0.4; } }
.char-hint { font-size: 11px; color: #5f6368; }

/* ── Chat messages ── */
[data-testid="stChatMessage"] {
    background: transparent !important;
    padding: 10px 15% !important;
    border-radius: 0 !important;
}
[data-testid="stChatMessage"]:nth-child(odd) { background: rgba(255,255,255,0.02) !important; }
[data-testid="stChatMessageContent"] {
    font-size: 15px !important; line-height: 1.7 !important; color: #e8eaed !important;
}
[data-testid="stChatMessageContent"] p { color: #e8eaed !important; font-size: 15px !important; }
[data-testid="stChatMessageContent"] h1,
[data-testid="stChatMessageContent"] h2,
[data-testid="stChatMessageContent"] h3 { color: #8ab4f8 !important; }
[data-testid="stChatMessageContent"] code {
    background: #2d2f3a !important; border-radius: 4px !important;
    padding: 2px 6px !important; font-size: 13px !important; color: #f28b82 !important;
}
[data-testid="stChatMessageContent"] pre {
    background: #2d2f3a !important; border-radius: 8px !important; padding: 16px !important;
}
[data-testid="stChatMessageContent"] blockquote {
    border-left: 3px solid #4285f4 !important;
    padding-left: 16px !important; color: #9aa0a6 !important;
}
[data-testid="stChatMessageContent"] li { color: #e8eaed !important; }
[data-testid="stChatMessageAvatarUser"]      { background: linear-gradient(135deg,#4285f4,#6c47ff) !important; }
[data-testid="stChatMessageAvatarAssistant"] { background: linear-gradient(135deg,#34a853,#1a73e8) !important; }

/* ── Paper cards ── */
.paper-card {
    background: rgba(255,255,255,0.03); border: 1px solid #2d2f3a;
    border-radius: 12px; padding: 14px 18px; margin: 8px 0; transition: border 0.2s;
}
.paper-card:hover { border-color: #4285f4; }
.paper-title   { color: #8ab4f8; font-size: 14px; font-weight: 600; margin-bottom: 6px; }
.paper-summary { color: #9aa0a6; font-size: 13px; line-height: 1.6; }
.paper-tags    { margin-top: 8px; display: flex; gap: 6px; flex-wrap: wrap; }
.paper-tag {
    background: rgba(66,133,244,0.1); color: #8ab4f8;
    border: 1px solid rgba(66,133,244,0.25);
    border-radius: 10px; padding: 2px 8px; font-size: 11px;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #3c4043; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# 2. SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
def render_sidebar(papers: list):
    with st.sidebar:
        st.markdown("""
        <div style='display:flex;align-items:center;gap:10px;margin-bottom:20px;'>
            <span style='font-size:28px;'>🔬</span>
            <div>
                <div style='font-family:Google Sans,sans-serif;font-weight:700;font-size:16px;
                            background:linear-gradient(135deg,#4285f4,#34a853);
                            -webkit-background-clip:text;-webkit-text-fill-color:transparent;'>
                    ResearchMind
                </div>
                <div style='font-size:11px;color:#9aa0a6;'>Multi-Agent AI</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("✏️  New Chat", use_container_width=True):
            st.session_state.messages = []
            st.session_state.last_research_topic = ""
            st.session_state.last_research_content = ""
            st.rerun()

        st.markdown("<div class='sidebar-title'>Recent Chats</div>", unsafe_allow_html=True)
        for chat in st.session_state.chat_history[:8]:
            st.markdown(f"<div class='chat-history-item'>💬 {chat}</div>", unsafe_allow_html=True)

        st.divider()
        st.markdown("<div class='sidebar-title'>Dataset Status</div>", unsafe_allow_html=True)
        if papers:
            st.markdown(f"""
            <div style='font-size:12px;color:#9aa0a6;line-height:1.9;'>
                <span style='color:#34a853;font-weight:600;'>✅ Loaded</span><br>
                📄 <b style='color:#bdc1c6;'>Papers:</b> {len(papers):,}<br>
                🗂️ <b style='color:#bdc1c6;'>Source:</b> ArXiv CSV<br>
                🔍 <b style='color:#bdc1c6;'>Search:</b> Keyword + Context
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style='font-size:12px;color:#9aa0a6;line-height:1.9;'>
                <span style='color:#ea4335;font-weight:600;'>⚠️ Not Found</span><br>
                Place <code>arxiv_data.csv</code> next to <code>app.py</code>
            </div>
            """, unsafe_allow_html=True)

        st.divider()
        st.markdown("<div class='sidebar-title'>Project Info</div>", unsafe_allow_html=True)
        st.markdown("""
        <div style='font-size:12px;color:#9aa0a6;line-height:1.8;'>
            🤖 <b style='color:#bdc1c6;'>Model:</b> Llama 3.2 (Ollama)<br>
            🧠 <b style='color:#bdc1c6;'>Mode:</b> Multi-Agent RAG<br>
            📚 <b style='color:#bdc1c6;'>Project:</b> LLM Academic Research<br>
            🔍 <b style='color:#bdc1c6;'>Auto-detect:</b> Research queries
        </div>
        """, unsafe_allow_html=True)

        st.divider()
        st.markdown("<div class='sidebar-title'>Capabilities</div>", unsafe_allow_html=True)
        st.markdown("""
        <div style='font-size:12px;color:#9aa0a6;line-height:2;'>
            ✅ General conversation<br>
            ✅ ArXiv dataset search (51K papers)<br>
            ✅ Academic research reports<br>
            ✅ PDF export<br>
            ✅ Category filtering<br>
            ✅ Multi-agent reasoning
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# 3. TOP BAR
# ══════════════════════════════════════════════════════════════════════════════
def render_topbar():
    st.markdown("""
<div class='top-bar'>
    <div class='logo'>🔬 ResearchMind AI</div>
    <div style='display:flex;align-items:center;gap:12px;'>
        <span style='color:#9aa0a6;font-size:13px;'>LLM-Based Multi-Agent Academic Research</span>
        <span class='badge'>RESEARCH MODE</span>
    </div>
</div>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# 4. WELCOME SCREEN
# ══════════════════════════════════════════════════════════════════════════════
def render_welcome(papers: list):
    paper_count = f"{len(papers):,}" if papers else "0"
    st.markdown(f"""
    <div class='welcome-wrap'>
        <div class='welcome-logo'>ResearchMind AI 🔬</div>
        <div class='welcome-sub'>
            Powered by <b>{paper_count} ArXiv papers</b>. Ask research questions and get answers
            grounded in real academic literature — plus PDF export.
        </div>
        <div class='suggestion-chips'>
            <div class='chip'>🧠 What is a multi-agent LLM system?</div>
            <div class='chip'>📄 Generate a PDF on RAG architecture</div>
            <div class='chip'>🔬 Survey on transformer attention</div>
            <div class='chip'>💬 How are you today?</div>
            <div class='chip'>📊 Compare GPT-4 vs LLaMA</div>
            <div class='chip'>🖼️ Find papers on computer vision</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# 5. CHAT MESSAGES
# ══════════════════════════════════════════════════════════════════════════════
def render_messages(papers: list):
    for i, msg in enumerate(st.session_state.messages):
        role = msg["role"]
        content = msg["content"]
        is_research = msg.get("research", False)
        retrieved_papers = msg.get("retrieved_papers", [])
        avatar = "🧑" if role == "user" else "🔬"

        with st.chat_message(role, avatar=avatar):
            if is_research and role == "assistant":
                st.markdown("<span class='research-badge'>🔬 RESEARCH REPORT</span>", unsafe_allow_html=True)
            if retrieved_papers and role == "assistant":
                count = len(retrieved_papers)
                st.markdown(
                    f"<span class='dataset-badge'>📚 {count} ArXiv Papers Retrieved</span>",
                    unsafe_allow_html=True
                )

            st.markdown(content)

            if retrieved_papers and role == "assistant":
                with st.expander(f"📚 View {len(retrieved_papers)} Retrieved ArXiv Papers"):
                    for p in retrieved_papers:
                        terms = parse_terms(p["terms"])
                        tags_html = "".join(f"<span class='paper-tag'>{t}</span>" for t in terms[:4])
                        summary_preview = p['summary'][:280].replace('\n', ' ')
                        st.markdown(f"""
                        <div class='paper-card'>
                            <div class='paper-title'>📄 {p['title']}</div>
                            <div class='paper-summary'>{summary_preview}...</div>
                            <div class='paper-tags'>{tags_html}</div>
                        </div>
                        """, unsafe_allow_html=True)

            if msg.get("image_url"):
                st.image(msg["image_url"], width=480)

            if msg.get("pdf_bytes"):
                st.download_button(
                    label="📥 Download Research PDF",
                    data=msg["pdf_bytes"],
                    file_name=f"research_{msg.get('pdf_topic','report').replace(' ','_')[:40]}.pdf",
                    mime="application/pdf",
                    key=f"dl_{i}"
                )


# ══════════════════════════════════════════════════════════════════════════════
# 6. INPUT PANEL  (returns user_input string or None)
# ══════════════════════════════════════════════════════════════════════════════
def render_input_panel(papers: list, categories: list) -> str | None:

    st.markdown("<div style='height: 120px;'></div>", unsafe_allow_html=True)

    with st.container():
        st.markdown("""
        <div class='input-toolbar'>
            <div class='toolbar-left'>
                <span style='font-size:12px;color:#5f6368;margin-right:4px;'>Filter:</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        cols = st.columns(len(categories))
        for idx, cat in enumerate(categories):
            with cols[idx]:
                is_active = st.session_state.selected_category == cat
                label = f"{'✦ ' if is_active else ''}{cat}"
                if st.button(label, key=f"cat_{cat}", use_container_width=True,
                             type="primary" if is_active else "secondary"):
                    st.session_state.selected_category = cat
                    st.rerun()

        active_cat = st.session_state.selected_category
        paper_count_display = f"{len(papers):,}" if papers else "0"
        st.markdown(f"""
        <div style='display:flex;justify-content:space-between;align-items:center;
                    padding:4px 2px 8px 2px;'>
            <div style='display:flex;gap:12px;align-items:center;'>
                <span class='toolbar-btn'>
                    <span class='toolbar-dot'></span> {paper_count_display} papers indexed
                </span>
                <span class='toolbar-btn active'>📂 {active_cat}</span>
            </div>
            <span class='char-hint'>Press Enter to send · Shift+Enter for new line</span>
        </div>
        """, unsafe_allow_html=True)

        user_input = st.chat_input(
            placeholder="Ask about any research topic, find papers, or just chat...",
        )

    return user_input

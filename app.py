import streamlit as st
import re
import csv
import ast
import datetime
from io import BytesIO

# ── Page config (must be first) ──────────────────────────────────────────────
st.set_page_config(
    page_title="ResearchMind AI",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Load UI styles ────────────────────────────────────────────────────────────
from ui import inject_css, render_sidebar, render_topbar, render_welcome, render_messages, render_input_panel

inject_css()

# ── Imports ───────────────────────────────────────────────────────────────────
from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# ═════════════════════════════════════════════════════════════════════════════
# DATASET
# ═════════════════════════════════════════════════════════════════════════════
DATASET_PATH = "arxiv_data.csv"

@st.cache_data(show_spinner=False)
def load_dataset(path: str):
    papers = []
    try:
        with open(path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                papers.append({
                    "title":   row.get("titles",    "").strip(),
                    "summary": row.get("summaries", "").strip(),
                    "terms":   row.get("terms",     "[]").strip(),
                })
    except FileNotFoundError:
        pass
    return papers

def parse_terms(terms_str: str):
    try:
        return ast.literal_eval(terms_str)
    except:
        return []

def search_papers(query: str, papers: list, top_k: int = 5, category_filter: str = None):
    if not papers or not query.strip():
        return []
    query_words = set(re.findall(r'\b\w{3,}\b', query.lower()))
    stop_words  = {'the','and','for','that','this','with','are','from','have',
                   'what','how','does','explain','tell','me','about','please'}
    query_words -= stop_words

    scored = []
    for paper in papers:
        text  = (paper["title"] + " " + paper["summary"]).lower()
        terms = parse_terms(paper["terms"])

        if category_filter and category_filter != "All":
            cat_map = {
                "Machine Learning": ["cs.LG", "stat.ML"],
                "Computer Vision":  ["cs.CV"],
                "NLP":              ["cs.CL", "cs.IR"],
                "Robotics":         ["cs.RO"],
                "AI":               ["cs.AI"],
                "Systems":          ["cs.DC", "cs.OS", "cs.NI"],
            }
            allowed = cat_map.get(category_filter, [])
            if not any(t in terms for t in allowed):
                continue

        score = 0
        for word in query_words:
            count = text.count(word)
            if count:
                score += count
                if word in paper["title"].lower():
                    score += 5
        if score > 0:
            scored.append((score, paper))

    scored.sort(key=lambda x: x[0], reverse=True)
    return [p for _, p in scored[:top_k]]

def build_context_from_papers(papers: list) -> str:
    if not papers:
        return ""
    ctx = "RELEVANT PAPERS FROM ARXIV DATASET:\n\n"
    for i, p in enumerate(papers, 1):
        terms = parse_terms(p["terms"])
        ctx += f"[Paper {i}] {p['title']}\n"
        ctx += f"Categories: {', '.join(terms)}\n"
        ctx += f"Abstract: {p['summary'][:600]}...\n\n"
    return ctx

# ═════════════════════════════════════════════════════════════════════════════
# SUMMARISATION
# ═════════════════════════════════════════════════════════════════════════════
SUMMARISE_SYSTEM = """You are ResearchMind AI — an expert academic summariser.

Given one or more ArXiv paper abstracts, produce a clean structured summary in this format:

## Executive Summary
[3-4 sentence high-level summary of all retrieved papers combined]

## Papers Covered
[Numbered list: paper title — one-line description]

## Core Themes & Findings
[Bullet points of the most important shared or distinct findings]

## Key Contributions
[What is novel or significant about these works]

## Practical Implications
[Real-world relevance and applications]

## Conclusion
[2-3 sentence closing synthesis]

Be concise, accurate, and academic. Only use what is in the provided abstracts — do not hallucinate."""

def summarise_papers(papers: list, llm) -> str:
    """Ask the LLM to summarise the retrieved papers."""
    if not papers:
        return "No papers found to summarise."

    paper_block = ""
    for i, p in enumerate(papers, 1):
        terms = parse_terms(p["terms"])
        paper_block += f"[Paper {i}] {p['title']}\n"
        paper_block += f"Categories: {', '.join(terms)}\n"
        paper_block += f"Abstract: {p['summary']}\n\n"

    prompt = (
        f"Please summarise the following {len(papers)} ArXiv paper(s):\n\n"
        f"{paper_block}"
        f"\nProduce the full structured summary as instructed."
    )

    messages = [
        SystemMessage(content=SUMMARISE_SYSTEM),
        HumanMessage(content=prompt),
    ]
    response = llm.invoke(messages)
    return response.content

# ═════════════════════════════════════════════════════════════════════════════
# PDF GENERATION
# ═════════════════════════════════════════════════════════════════════════════
def generate_pdf(title: str, content: str, paper_meta: list = None) -> bytes:
    """
    Generate a formatted A4 PDF from the AI response content.
    paper_meta: optional list of paper dicts appended as an Appendix section.
    """
    try:
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm
        from reportlab.lib import colors
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
        from reportlab.lib.enums import TA_CENTER

        buf = BytesIO()
        doc = SimpleDocTemplate(
            buf, pagesize=A4,
            leftMargin=2.5*cm, rightMargin=2.5*cm,
            topMargin=2.5*cm,  bottomMargin=2.5*cm
        )

        styles   = getSampleStyleSheet()
        clr_blue = colors.HexColor('#1a73e8')
        clr_grey = colors.HexColor('#5f6368')
        clr_div  = colors.HexColor('#dadce0')

        title_style = ParagraphStyle(
            'RMTitle', parent=styles['Title'],
            fontSize=22, textColor=clr_blue,
            spaceAfter=6, alignment=TA_CENTER
        )
        subtitle_style = ParagraphStyle(
            'RMSub', parent=styles['Normal'],
            fontSize=12, textColor=clr_blue,
            spaceAfter=4, alignment=TA_CENTER,
            fontName='Helvetica-BoldOblique'
        )
        meta_style = ParagraphStyle(
            'RMMeta', parent=styles['Normal'],
            fontSize=10, textColor=clr_grey,
            alignment=TA_CENTER, spaceAfter=16
        )
        h2_style = ParagraphStyle(
            'RMH2', parent=styles['Heading2'],
            fontSize=14, textColor=clr_blue,
            spaceBefore=18, spaceAfter=6
        )
        h3_style = ParagraphStyle(
            'RMH3', parent=styles['Heading3'],
            fontSize=12, textColor=colors.HexColor('#34a853'),
            spaceBefore=12, spaceAfter=4
        )
        body_style = ParagraphStyle(
            'RMBody', parent=styles['Normal'],
            fontSize=11, leading=18, spaceAfter=8
        )
        bullet_style = ParagraphStyle(
            'RMBullet', parent=styles['Normal'],
            fontSize=11, leading=18, spaceAfter=6, leftIndent=16
        )
        small_style = ParagraphStyle(
            'RMSmall', parent=styles['Normal'],
            fontSize=9, textColor=clr_grey, leading=14, spaceAfter=6
        )

        story = []

        # ── Cover block ──
        story.append(Spacer(1, 0.5*cm))
        story.append(Paragraph("ResearchMind AI", title_style))
        story.append(Paragraph("ArXiv Research Summary Report", subtitle_style))
        story.append(Spacer(1, 0.3*cm))
        story.append(Paragraph(f"<b>Topic:</b> {title}", meta_style))
        story.append(Paragraph(
            f"Generated: {datetime.datetime.now().strftime('%B %d, %Y  %H:%M')}",
            meta_style
        ))
        story.append(HRFlowable(width="100%", thickness=1.5, color=clr_blue))
        story.append(Spacer(1, 0.4*cm))

        # ── Main content ──
        for line in content.split('\n'):
            line = line.strip()
            if not line:
                story.append(Spacer(1, 0.18*cm))
                continue
            if line.startswith('### '):
                story.append(Paragraph(line[4:].strip(), h3_style))
            elif line.startswith('## ') or line.startswith('# '):
                story.append(Paragraph(line.lstrip('#').strip(), h2_style))
            elif line.startswith('- ') or line.startswith('* '):
                clean = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line[2:])
                clean = re.sub(r'\*(.*?)\*',    r'<i>\1</i>', clean)
                story.append(Paragraph(f"• {clean}", bullet_style))
            elif re.match(r'^\d+\.\s', line):
                clean = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line)
                clean = re.sub(r'\*(.*?)\*',    r'<i>\1</i>', clean)
                story.append(Paragraph(clean, bullet_style))
            else:
                clean = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line)
                clean = re.sub(r'\*(.*?)\*',    r'<i>\1</i>', clean)
                story.append(Paragraph(clean, body_style))

        # ── Appendix: full paper abstracts ──
        if paper_meta:
            story.append(Spacer(1, 0.6*cm))
            story.append(HRFlowable(width="100%", thickness=1, color=clr_div))
            story.append(Spacer(1, 0.2*cm))
            story.append(Paragraph("Appendix — Retrieved ArXiv Papers", h2_style))
            story.append(Spacer(1, 0.2*cm))
            for idx, p in enumerate(paper_meta, 1):
                terms = parse_terms(p["terms"])
                story.append(Paragraph(f"{idx}. {p['title']}", h3_style))
                story.append(Paragraph(
                    f"<b>Categories:</b> {', '.join(terms)}", small_style
                ))
                story.append(Paragraph(
                    p["summary"].replace('\n', ' '), small_style
                ))
                story.append(Spacer(1, 0.2*cm))

        # ── Footer ──
        story.append(Spacer(1, 0.5*cm))
        story.append(HRFlowable(width="100%", thickness=0.5, color=clr_div))
        story.append(Paragraph(
            "Generated by ResearchMind AI — LLM-Based Multi-Agent Academic Research System",
            meta_style
        ))

        doc.build(story)
        return buf.getvalue()

    except ImportError:
        return b""

# ═════════════════════════════════════════════════════════════════════════════
# QUERY CLASSIFICATION
# ═════════════════════════════════════════════════════════════════════════════
RESEARCH_KEYWORDS = [
    "research","study","paper","literature","review","analysis","explain",
    "what is","how does","theory","algorithm","model","neural","machine learning",
    "deep learning","nlp","llm","transformer","attention","rag","agent",
    "multi-agent","embedding","dataset","benchmark","methodology","findings",
    "abstract","introduction","conclusion","survey","overview","compare",
    "difference between","advantages","disadvantages","applications","future",
    "challenges","limitations","quantum","blockchain","computer vision",
    "reinforcement","fine-tuning","prompt","vector","knowledge graph",
    "semantic","ontology","arxiv","find papers","search papers",
]

def is_research_query(text: str) -> bool:
    return any(kw in text.lower() for kw in RESEARCH_KEYWORDS)

def wants_pdf(text: str) -> bool:
    return any(w in text.lower() for w in
               ["pdf","download","export","report","document","save"])

def wants_summarise(text: str) -> bool:
    return any(w in text.lower() for w in
               ["summarise","summarize","summary","summarization",
                "brief","overview of papers","tldr","tl;dr"])

def wants_image(text: str) -> bool:
    return any(w in text.lower() for w in
               ["image","picture","diagram","figure","show me","visualize"])

# ═════════════════════════════════════════════════════════════════════════════
# SYSTEM PROMPTS
# ═════════════════════════════════════════════════════════════════════════════
NORMAL_SYSTEM = """You are ResearchMind AI — a smart, friendly assistant specialised in academic research.
For casual conversation, respond naturally and concisely. Be warm, clear, and helpful."""

RESEARCH_SYSTEM_TEMPLATE = """You are ResearchMind AI — an expert academic research assistant powered by a database of 51,000+ ArXiv papers.

{context}

Using the papers above (if any were found) AND your own knowledge, answer the user's question in this structure:

## Overview
[2-3 sentence summary]

## Key Concepts
[Bullet points of main ideas]

## Detailed Explanation
[In-depth explanation with examples]

## Insights from ArXiv Dataset
[Reference the provided papers where relevant, mention their titles]

## Applications & Current Research
[Recent developments, trends, benchmarks]

## References & Further Reading
[Suggest key papers or resources]

Be thorough, academic, yet accessible. Always connect findings to the retrieved ArXiv papers."""

# ═════════════════════════════════════════════════════════════════════════════
# LLM
# ═════════════════════════════════════════════════════════════════════════════
@st.cache_resource
def get_llm():
    return ChatOllama(model="llama3.2", temperature=0.7)

# ═════════════════════════════════════════════════════════════════════════════
# SESSION STATE
# ═════════════════════════════════════════════════════════════════════════════
defaults = {
    "messages":              [],
    "chat_history":          ["Welcome Chat"],
    "last_research_topic":   "",
    "last_research_content": "",
    "selected_category":     "All",
    "dataset_loaded":        False,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ═════════════════════════════════════════════════════════════════════════════
# LOAD DATA
# ═════════════════════════════════════════════════════════════════════════════
papers = load_dataset(DATASET_PATH)
if papers and not st.session_state.dataset_loaded:
    st.session_state.dataset_loaded = True

# ═════════════════════════════════════════════════════════════════════════════
# RENDER UI SHELL
# ═════════════════════════════════════════════════════════════════════════════
render_sidebar(papers)
render_topbar()

st.markdown("<div style='margin-top:60px;'></div>", unsafe_allow_html=True)

if not st.session_state.messages:
    render_welcome(papers)

render_messages(papers)

CATEGORIES = ["All", "Machine Learning", "Computer Vision", "NLP", "AI", "Robotics", "Systems"]
user_input = render_input_panel(papers, CATEGORIES)

# ═════════════════════════════════════════════════════════════════════════════
# HANDLE INPUT
# ═════════════════════════════════════════════════════════════════════════════
if user_input and user_input.strip():
    query           = user_input.strip()
    research_mode   = is_research_query(query)
    pdf_requested   = wants_pdf(query)
    summarise_mode  = wants_summarise(query)
    image_requested = wants_image(query)
    category_filter = st.session_state.selected_category

    # ── Update sidebar chat history label ──
    if len(st.session_state.chat_history) == 1 and st.session_state.chat_history[0] == "Welcome Chat":
        st.session_state.chat_history[0] = query[:40] + ("..." if len(query) > 40 else "")
    else:
        st.session_state.chat_history.insert(0, query[:40] + ("..." if len(query) > 40 else ""))

    st.session_state.messages.append({"role": "user", "content": query, "research": False})

    # ── Search dataset ──
    retrieved_papers = []
    context_str      = ""
    if papers and (research_mode or summarise_mode):
        retrieved_papers = search_papers(
            query, papers, top_k=5,
            category_filter=category_filter if category_filter != "All" else None
        )
        context_str = build_context_from_papers(retrieved_papers)

    llm     = get_llm()
    ai_text = ""

    # ── SUMMARISE path ──
    if summarise_mode and retrieved_papers:
        with st.spinner("📝 Summarising retrieved papers..."):
            try:
                ai_text       = summarise_papers(retrieved_papers, llm)
                research_mode = True   # enables PDF + research badge
            except Exception as e:
                ai_text          = f"⚠️ Summarisation failed: {e}"
                research_mode    = False
                retrieved_papers = []

    # ── RESEARCH / NORMAL path ──
    else:
        system_content = (
            RESEARCH_SYSTEM_TEMPLATE.format(
                context=context_str or "No papers retrieved from dataset for this query."
            )
            if research_mode else NORMAL_SYSTEM
        )

        lc_messages = [SystemMessage(content=system_content)]
        for m in st.session_state.messages[:-1]:
            if m["role"] == "user":
                lc_messages.append(HumanMessage(content=m["content"]))
            else:
                lc_messages.append(AIMessage(content=m["content"]))
        lc_messages.append(HumanMessage(content=query))

        spinner_msg = "🔬 Searching dataset & generating answer..." if research_mode else "💬 Thinking..."
        with st.spinner(spinner_msg):
            try:
                response = llm.invoke(lc_messages)
                ai_text  = response.content
            except Exception as e:
                ai_text          = (
                    f"⚠️ Could not connect to Ollama. Make sure it is running with "
                    f"`ollama serve` and the model is pulled with `ollama pull llama3.2`.\n\nError: {e}"
                )
                research_mode    = False
                retrieved_papers = []

    # ── Cache research content for future PDF requests ──
    if research_mode:
        st.session_state.last_research_topic   = query
        st.session_state.last_research_content = ai_text

    # ── Image ──
    img_url = None
    if image_requested:
        try:
            search_term = re.sub(
                r'(show|image|picture|diagram|figure|of|me|a|an|the)', '', query.lower()
            ).strip().replace(' ', ',')
            img_url = f"https://source.unsplash.com/800x400/?{search_term}"
        except:
            img_url = None

    # ── PDF ──
    # Triggers when: user asks for pdf/download/export/save/report/document
    #             OR when summarise produced a result (auto PDF)
    pdf_bytes = None
    pdf_topic = ""

    should_make_pdf = pdf_requested or (summarise_mode and research_mode and ai_text)

    if should_make_pdf:
        topic           = st.session_state.last_research_topic   or query
        content_for_pdf = st.session_state.last_research_content or ai_text

        with st.spinner("📄 Generating PDF..."):
            pdf_bytes = generate_pdf(
                title      = topic,
                content    = content_for_pdf,
                paper_meta = retrieved_papers if retrieved_papers else None,
            )
        pdf_topic = topic

        if not pdf_bytes:
            ai_text += (
                "\n\n> ⚠️ PDF generation requires `reportlab`."
                " Install with: `pip install reportlab`"
            )

    # ── Save assistant message ──
    msg_obj = {
        "role":             "assistant",
        "content":          ai_text,
        "research":         research_mode,
        "retrieved_papers": retrieved_papers,
    }
    if img_url:
        msg_obj["image_url"] = img_url
    if pdf_bytes:
        msg_obj["pdf_bytes"] = pdf_bytes
        msg_obj["pdf_topic"] = pdf_topic

    st.session_state.messages.append(msg_obj)
    st.rerun()

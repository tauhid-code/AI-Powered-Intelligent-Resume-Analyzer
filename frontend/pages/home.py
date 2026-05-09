import datetime
import streamlit as st
import sys, os
from pathlib import Path
_FRONTEND_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_PROJECT_ROOT = os.path.dirname(_FRONTEND_DIR)
_RESUME_DIR   = os.path.join(_PROJECT_ROOT, "uploads", "resumes")
for _p in (_PROJECT_ROOT, _FRONTEND_DIR):
    if _p not in sys.path:
        sys.path.insert(0, _p)

st.set_page_config(
    page_title="Hirelytics AI — Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)

if not st.session_state.get("jwt_token"):
    st.switch_page("app.py")
    st.stop()

from components.sidebar import render_sidebar


_GLOBAL_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

/* ── Palette ──────────────────────────────────────────────────────────────
   Background : #0e1117
   Accent     : #FA4B4C  (buttons, headings, rings, focus)
   Input bg   : #1F1F1F
   Text       : #ffffff / rgba(255,255,255,0.xx)
   ─────────────────────────────────────────────────────────────────────── */

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}
.stApp {
    background: #0e1117;
    color: #e8e8f0;
}

/* ── Cards ── */
.card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 28px 28px 24px;
    height: 100%;
}
.card-title {
    font-family: 'Syne', sans-serif;
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: rgba(255,255,255,0.35);
    margin-bottom: 8px;
}
.card-value {
    font-family: 'Syne', sans-serif;
    font-size: 2.6rem;
    font-weight: 800;
    color: #ffffff;
    line-height: 1;
}
.card-sub {
    font-size: 0.78rem;
    color: rgba(255,255,255,0.35);
    margin-top: 6px;
}

/* ── Section headings ── */
.section-heading {
    font-family: 'Syne', sans-serif;
    font-size: 1.15rem;
    font-weight: 700;
    color: #FA4B4C;
    margin-bottom: 4px;
}
.section-sub {
    font-size: 0.82rem;
    color: rgba(255,255,255,0.35);
    margin-bottom: 18px;
}

/* ── Welcome banner ── */
.welcome-banner {
    background: rgba(250,75,76,0.08);
    border: 1px solid rgba(250,75,76,0.25);
    border-radius: 16px;
    padding: 28px 32px;
    margin-bottom: 28px;
    display: flex;
    align-items: center;
    gap: 20px;
}
.welcome-greeting {
    font-family: 'Syne', sans-serif;
    font-size: 1.6rem;
    font-weight: 800;
    color: #ffffff;
}
.welcome-tagline {
    font-size: 0.88rem;
    color: rgba(255,255,255,0.5);
    margin-top: 4px;
}
.avatar {
    background: #FA4B4C;
    border-radius: 50%;
    width: 52px;
    height: 52px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    flex-shrink: 0;
}

/* ── Score ring ── */
.score-ring {
    background: conic-gradient(#FA4B4C 0deg, #FA4B4C 252deg, rgba(255,255,255,0.06) 252deg 360deg);
    border-radius: 50%;
    width: 120px;
    height: 120px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 12px auto;
}
.score-inner {
    background: #0e1117;
    border-radius: 50%;
    width: 90px;
    height: 90px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
}
.score-num {
    font-family: 'Syne', sans-serif;
    font-size: 1.6rem;
    font-weight: 800;
    color: #FA4B4C;
    line-height: 1;
}
.score-label {
    font-size: 0.65rem;
    color: rgba(255,255,255,0.35);
    letter-spacing: 0.08em;
}

/* ── Skill chips ── */
.chip-row { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 6px; }
.chip {
    background: rgba(250,75,76,0.12);
    border: 1px solid rgba(250,75,76,0.30);
    border-radius: 999px;
    padding: 4px 12px;
    font-size: 0.78rem;
    color: #fca5a5;
}
.chip-match {
    background: rgba(34,197,94,0.12);
    border: 1px solid rgba(34,197,94,0.25);
    color: #86efac;
}

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.03) !important;
    border: 1.5px dashed rgba(250,75,76,0.40) !important;
    border-radius: 12px !important;
    padding: 8px !important;
}
[data-testid="stFileUploader"] label { color: rgba(255,255,255,0.55) !important; }

/* ── Text area ── */
.stTextArea textarea {
    background: #1F1F1F !important;
    border: 1px solid rgba(255,255,255,0.10) !important;
    border-radius: 10px !important;
    color: #ffffff !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.88rem !important;
}
.stTextArea textarea:focus {
    border-color: #FA4B4C !important;
    box-shadow: 0 0 0 3px rgba(250,75,76,0.18) !important;
}

/* ── Text inputs (selectbox / text_input in main area) ── */
[data-testid="stTextInput"] input,
[data-testid="stSelectbox"] > div,
div[data-baseweb="select"] > div {
    background: #1F1F1F !important;
    color: #ffffff !important;
    border-color: rgba(255,255,255,0.10) !important;
    border-radius: 10px !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: #FA4B4C !important;
    box-shadow: 0 0 0 3px rgba(250,75,76,0.18) !important;
}

/* ── All primary buttons ── */
div[data-testid="stButton"] button[kind="primary"],
[data-testid="stFormSubmitButton"] button {
    background:    #FA4B4C !important;
    border:        none !important;
    border-radius: 10px !important;
    color:         #ffffff !important;
    font-family:   'Syne', sans-serif !important;
    font-weight:   700 !important;
    font-size:     1rem !important;
    letter-spacing: 0.03em !important;
    padding:       14px 0 !important;
    box-shadow:    0 4px 14px rgba(250,75,76,0.30) !important;
    transition:    all 0.18s ease !important;
}
div[data-testid="stButton"] button[kind="primary"]:hover,
[data-testid="stFormSubmitButton"] button:hover {
    background: #e03e3f !important;
    box-shadow: 0 6px 20px rgba(250,75,76,0.45) !important;
    transform:  translateY(-1px) !important;
}

/* Secondary buttons */
div[data-testid="stButton"] button[kind="secondary"] {
    background:  rgba(255,255,255,0.04) !important;
    border:      1px solid rgba(255,255,255,0.12) !important;
    color:       rgba(255,255,255,0.65) !important;
    border-radius: 10px !important;
}
div[data-testid="stButton"] button[kind="secondary"]:hover {
    background:   rgba(250,75,76,0.08) !important;
    border-color: rgba(250,75,76,0.45) !important;
    color:        #ffffff !important;
}

/* ── Divider ── */
hr { border-color: rgba(255,255,255,0.06) !important; }

/* ── File list item ── */
.file-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 10px 14px;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 10px;
    margin-bottom: 8px;
    font-size: 0.86rem;
    color: #c8c8dd;
}
.file-icon { font-size: 1.1rem; }
</style>
"""



def _load_stored_resumes() -> None:
    """Scan _RESUME_DIR and populate session_state["stored_resumes"] on first load."""
    if "stored_resumes" in st.session_state:
        return
    os.makedirs(_RESUME_DIR, exist_ok=True)
    resumes = []
    for f in sorted(Path(_RESUME_DIR).glob("*.pdf"), key=lambda p: p.stat().st_mtime, reverse=True):
        stat = f.stat()
        resumes.append({
            "name":     f.name,
            "path":     str(f),
            "saved_at": datetime.datetime.fromtimestamp(stat.st_mtime).strftime("%d %b %Y"),
            "size":     f"{stat.st_size // 1024} KB",
        })
    st.session_state["stored_resumes"] = resumes


def _save_resume_to_disk(uploaded_file) -> dict:
    """Persist an UploadedFile to _RESUME_DIR and refresh stored_resumes."""
    os.makedirs(_RESUME_DIR, exist_ok=True)
    dest = os.path.join(_RESUME_DIR, uploaded_file.name)
    buf  = uploaded_file.getbuffer()
    with open(dest, "wb") as fh:
        fh.write(buf)
    entry = {
        "name":     uploaded_file.name,
        "path":     dest,
        "saved_at": datetime.datetime.now().strftime("%d %b %Y"),
        "size":     f"{len(buf) // 1024} KB",
    }
    resumes = [r for r in st.session_state.get("stored_resumes", [])
               if r["name"] != uploaded_file.name]   # remove duplicate
    resumes.insert(0, entry)
    st.session_state["stored_resumes"] = resumes
    return entry


def _delete_resume(entry: dict) -> None:
    """Delete a stored resume from disk and session state."""
    try:
        os.remove(entry["path"])
    except FileNotFoundError:
        pass
    # Remove selection if this resume was selected
    sel = st.session_state.get("selected_resume")
    if sel and sel["path"] == entry["path"]:
        st.session_state["selected_resume"] = None
    resumes = [r for r in st.session_state.get("stored_resumes", [])
               if r["path"] != entry["path"]]
    st.session_state["stored_resumes"] = resumes


def _save_to_history(resume_name: str, jd_text: str, result) -> None:
    """Append an ATSResult to analysis_history; keep the most recent 5."""
    jd_preview = jd_text.strip().replace("\n", " ")[:110]
    if len(jd_text.strip()) > 110:
        jd_preview += "…"
    entry = {
        "resume_name":    resume_name,
        "jd_preview":     jd_preview,
        "ats_score":      result.ats_score,
        "keyword_score":  result.keyword_score,
        "semantic_score": result.semantic_score,
        "section_score":  result.section_score,
        "matched":        result.matched_skills,
        "missing":        result.missing_skills,
        "timestamp":      datetime.datetime.now().strftime("%d %b %Y, %H:%M"),
    }
    history = st.session_state.get("analysis_history", [])
    history.append(entry)
    st.session_state["analysis_history"] = history[-5:]   # keep last 5

def show_home():
    st.markdown(_GLOBAL_CSS, unsafe_allow_html=True)

    # ── Sidebar ───
    active_page = render_sidebar()

    # ── Route sub-pages ───
    if active_page == "dashboard":
        _page_dashboard()
    elif active_page == "analysis":
        _page_analysis()
    elif active_page == "interview_coach":
        _page_interview_coach()


# PAGE: Dashboard (main)
def _page_dashboard():
    _load_stored_resumes()

    name    = st.session_state.get("user_name", "User")
    initial = name[0].upper() if name else "U"

    # ── Welcome banner ────
    st.markdown(f"""
    <div class="welcome-banner">
        <div class="avatar">{initial}</div>
        <div>
            <div class="welcome-greeting">Hello, {name} </div>
            <div class="welcome-tagline">Let's optimize your resume and land that dream job.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Live stats row ───
    stored  = st.session_state.get("stored_resumes",   [])
    history = st.session_state.get("analysis_history", [])
    n_res   = len(stored)
    n_hist  = len(history)
    best    = max((h["ats_score"] for h in history), default=None)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f"""
        <div class="card">
            <div class="card-title">Resumes Stored</div>
            <div class="card-value">{n_res}</div>
            <div class="card-sub">{"Upload your first resume ↓" if n_res == 0 else f"{n_res} resume(s) ready to use"}</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class="card">
            <div class="card-title">Analyses Run</div>
            <div class="card-value">{n_hist}</div>
            <div class="card-sub">{"No analysis yet" if n_hist == 0 else "View history in sidebar"}</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        score_disp = f"{best:.0f}" if best is not None else "—"
        score_sub  = "Run an analysis to see" if best is None else "Your personal best"
        st.markdown(f"""
        <div class="card">
            <div class="card-title">Best ATS Score</div>
            <div class="card-value">{score_disp}</div>
            <div class="card-sub">{score_sub}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)
    st.markdown("---")

  
    # SAVED RESUMES TABLE
    st.markdown("""
    <div class="section-heading"> Saved Resumes</div>
    <div class="section-sub">Select a resume to reuse it — no need to upload again.</div>
    """, unsafe_allow_html=True)

    selected = st.session_state.get("selected_resume")

    if stored:
        # Column headers
        hc1, hc2, hc3, hc4, hc5 = st.columns([4, 2, 1, 1, 1])
        hc1.markdown('<span style="font-size:0.72rem;color:rgba(255,255,255,0.3);text-transform:uppercase;letter-spacing:.08em">Resume</span>', unsafe_allow_html=True)
        hc2.markdown('<span style="font-size:0.72rem;color:rgba(255,255,255,0.3);text-transform:uppercase;letter-spacing:.08em">Saved</span>', unsafe_allow_html=True)
        hc3.markdown('<span style="font-size:0.72rem;color:rgba(255,255,255,0.3);text-transform:uppercase;letter-spacing:.08em">Size</span>', unsafe_allow_html=True)
        hc4.markdown("")  
        hc5.markdown("")  

        for i, r in enumerate(stored):
            is_sel = selected and selected["path"] == r["path"]
            rc1, rc2, rc3, rc4, rc5 = st.columns([4, 2, 1, 1, 1])

            label = f"{'✅ ' if is_sel else '📄 '}**{r['name']}**"
            if is_sel:
                label += "  ← *active*"
            rc1.markdown(label)
            rc2.markdown(f'<span style="font-size:0.82rem;color:rgba(255,255,255,0.45)">{r["saved_at"]}</span>', unsafe_allow_html=True)
            rc3.markdown(f'<span style="font-size:0.82rem;color:rgba(255,255,255,0.35)">{r["size"]}</span>', unsafe_allow_html=True)

            with rc4:
                if is_sel:
                    if st.button("Deselect", key=f"desel_{i}", use_container_width=True):
                        st.session_state["selected_resume"] = None
                        st.rerun()
                else:
                    if st.button("▶ Select", key=f"sel_{i}", use_container_width=True):
                        st.session_state["selected_resume"] = r
                        st.rerun()

            with rc5:
                if st.button("🗑", key=f"del_{i}", help="Delete this resume", use_container_width=True):
                    _delete_resume(r)
                    st.rerun()

    else:
        st.info("No resumes saved yet. Upload one below and it will appear here.")

    # Upload new resume
    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    new_up = st.file_uploader(
        "  Upload a new resume (saved automatically)",
        type=["pdf"],
        key="dash_new_upload",
    )
    if new_up:
        already = any(r["name"] == new_up.name for r in st.session_state.get("stored_resumes", []))
        if not already:
            entry = _save_resume_to_disk(new_up)
            st.success(f" **{entry['name']}** saved!  Select it above to use it.")
            st.rerun()
        else:
            st.info(f"'{new_up.name}' is already in your library. Select it from the table above.")

    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
    st.markdown("---")

    # QUICK ANALYZE

    selected = st.session_state.get("selected_resume")   # refresh after potential rerun

    st.markdown("""
    <div class="section-heading"> Quick Analyze</div>
    <div class="section-sub">Paste a job description and get your ATS score instantly.</div>
    """, unsafe_allow_html=True)

    if selected:
        # Resume already chosen — only JD needed 
        st.markdown(f"""
        <div style="background:rgba(250,75,76,0.08);border:1px solid rgba(250,75,76,0.25);
                    border-radius:12px;padding:12px 18px;margin-bottom:16px;display:flex;
                    align-items:center;gap:12px;">
            <span style="font-size:1.3rem"></span>
            <div>
                <span style="color:#FA4B4C;font-weight:600">{selected["name"]}</span>
                <span style="color:rgba(255,255,255,0.35);font-size:0.8rem;margin-left:8px">selected</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        jd = st.text_area(
            " Job Description",
            height=200,
            placeholder="Paste the full job description here…",
            key="dash_jd_selected",
        )

        if st.button("  Analyze Resume", type="primary", use_container_width=True):
            if not jd.strip():
                st.warning("Please paste a job description first.")
            else:
                _run_real_analysis(jd_text=jd, file_path=selected["path"],
                                   resume_name=selected["name"])

    else:
        st.info(" **Tip:** Select a saved resume above so you don't have to upload it every time.")

        left, right = st.columns([1, 1], gap="large")
        with left:
            st.markdown("** Resume (PDF)**")
            uploaded = st.file_uploader(
                "Drop PDF here",
                type=["pdf"],
                key="dash_upload_quick",
                label_visibility="collapsed",
            )
            if uploaded:
                st.success(f" {uploaded.name} ready")

        with right:
            st.markdown("** Job Description**")
            jd = st.text_area(
                "Paste JD",
                height=180,
                placeholder="Paste the full job description here…",
                key="dash_jd_quick",
                label_visibility="collapsed",
            )

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

        if st.button("  Analyze Resume", type="primary", use_container_width=True):
            if not uploaded:
                st.warning("Please upload a resume PDF first.")
            elif not jd.strip():
                st.warning("Please enter a job description.")
            else:
                # Auto-save this resume for future use
                entry = _save_resume_to_disk(uploaded)
                _run_real_analysis(jd_text=jd, uploaded_file=uploaded,
                                   resume_name=uploaded.name)



# PAGE: Resume Upload

def _page_resume_upload():
    st.markdown("""
    <div class="section-heading"> Resume Upload</div>
    <div class="section-sub">Manage all your resume versions here.</div>
    """, unsafe_allow_html=True)

    uploaded = st.file_uploader(
        "Upload PDF",
        type=["pdf"],
        accept_multiple_files=True,
        key="page_upload",
    )

    if uploaded:
        for f in uploaded:
            st.session_state.setdefault("uploaded_files", [])
            if f.name not in st.session_state["uploaded_files"]:
                st.session_state["uploaded_files"].append(f.name)
        st.success(f"{len(uploaded)} file(s) added.")

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    files = st.session_state.get("uploaded_files", [])
    if files:
        st.markdown("**Uploaded files:**")
        for fname in files:
            st.markdown(
                f'<div class="file-item"><span class="file-icon"></span>{fname}</div>',
                unsafe_allow_html=True,
            )
    else:
        st.info("No resumes uploaded yet. Use the uploader above.")



# PAGE: Analysis History  (last 5 comparisons)

def _page_analysis():
    st.markdown("""
    <div class="section-heading"> Analysis History</div>
    <div class="section-sub">Your last 5 resume vs JD comparisons — matched skills, missing skills, and ATS scores.</div>
    """, unsafe_allow_html=True)

    history = list(reversed(st.session_state.get("analysis_history", [])))   # newest first

    if not history:
        st.info(" No analyses yet. Run your first analysis from the **Dashboard**.")
        return

    # Score colour helper 
    def _score_color(s):
        if s >= 80: return "#22c55e"
        if s >= 60: return "#FA4B4C"
        if s >= 40: return "#f59e0b"
        return "#ef4444"

    def _score_label(s):
        if s >= 80: return "Excellent"
        if s >= 60: return "Good"
        if s >= 40: return "Fair"
        return "Poor"

    def _chips_html(skills, css_class="chip"):
        if not skills:
            return '<span style="color:rgba(255,255,255,0.3);font-size:0.8rem">None</span>'
        return "".join(f'<span class="{css_class}">{s}</span>' for s in skills[:15])

    total = len(history)

    for idx, entry in enumerate(history):
        score  = entry["ats_score"]
        color  = _score_color(score)
        label  = _score_label(score)
        n_mat  = len(entry["matched"])
        n_mis  = len(entry["missing"])
        rank   = total - idx

        header = (
            f"#{rank}  •   {entry['resume_name']}  "
            f"  |  ATS: {score:.0f}/100 ({label})"
        )

        with st.expander(header, expanded=(idx == 0)):

            m1, m2, m3, m4 = st.columns(4)
            with m1:
                st.markdown(f"""
                <div class="card" style="text-align:center;padding:16px;">
                    <div class="card-title" style="text-align:center">ATS Score</div>
                    <div style="font-family:'Syne',sans-serif;font-size:2rem;font-weight:800;
                                color:{color};line-height:1;">{score:.0f}</div>
                    <div class="card-sub" style="text-align:center">{label}</div>
                </div>""", unsafe_allow_html=True)
            with m2:
                st.metric("Keyword Match",    f"{entry['keyword_score']*100:.1f}%",
                          help="50% weight in ATS score")
            with m3:
                st.metric("Semantic Match",   f"{entry['semantic_score']*100:.1f}%",
                          help="25% weight in ATS score")
            with m4:
                st.metric("Section Coverage", f"{entry['section_score']*100:.1f}%",
                          help="25% weight in ATS score")


            st.markdown(
                f'<div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);'
                f'border-radius:8px;padding:10px 14px;font-size:0.8rem;color:rgba(255,255,255,0.4);'
                f'margin:12px 0;"> JD: {entry["jd_preview"]}</div>',
                unsafe_allow_html=True,
            )

            sc1, sc2 = st.columns(2)
            with sc1:
                st.markdown(f"""
                <div class="card" style="padding:16px;">
                    <div class="card-title"> Matched Skills ({n_mat})</div>
                    <div class="chip-row" style="margin-top:8px">
                        {_chips_html(entry["matched"], "chip chip-match")}
                    </div>
                </div>""", unsafe_allow_html=True)
            with sc2:
                st.markdown(f"""
                <div class="card" style="padding:16px;">
                    <div class="card-title"> Missing Skills ({n_mis})</div>
                    <div class="chip-row" style="margin-top:8px">
                        {_chips_html(entry["missing"], "chip")}
                    </div>
                </div>""", unsafe_allow_html=True)

            tips = []
            if entry["missing"]:
                tips.append(f"Add these missing skills if you have them: **{', '.join(entry['missing'][:5])}**")
            if entry["keyword_score"] < 0.5:
                tips.append("Keyword match < 50% — mirror the JD's exact skill names in your resume.")
            if entry["semantic_score"] < 0.4:
                tips.append("Semantic similarity is low — tailor your summary to match the JD's language.")
            if score >= 80:
                tips.append("Great match! Quantify achievements to stand out further.")

            if tips:
                st.markdown("** Improvement Tips:**")
                for t in tips:
                    st.markdown(f"- {t}")

        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)



# PAGE: Interview Coach (placeholder)

def _page_interview_coach():
    from src.interview_coach import generate_interview_questions, extract_projects_from_text
    from src.parser import parse_resume

    st.markdown("""
    <div class="section-heading"> AI Interview Coach</div>
    <div class="section-sub">Personalized interview questions generated by AI — based on your resume, skills, and Job Description.</div>
    """, unsafe_allow_html=True)

    _load_stored_resumes()
    stored  = st.session_state.get("stored_resumes",   [])
    history = st.session_state.get("analysis_history", [])

    # Setup panel 
    st.markdown("####  Setup")

    col1, col2 = st.columns([1, 1], gap="large")

    with col1:
        if stored:
            resume_names = [r["name"] for r in stored]
           
            default_idx = 0
            sel = st.session_state.get("selected_resume")
            if sel:
                try:
                    default_idx = resume_names.index(sel["name"])
                except ValueError:
                    pass
            chosen_name   = st.selectbox(" Select Resume", resume_names, index=default_idx)
            chosen_resume = next(r for r in stored if r["name"] == chosen_name)
        else:
            st.warning(" No resumes saved. Upload one from the Dashboard first.")
            chosen_resume = None

    with col2:
        role = st.text_input(
            " Target Role",
            placeholder="e.g. Machine Learning Engineer, FrontEnd Developer…",
        )

    # ── Analysis selector + skills preview ───
    matched_skills: list = []
    missing_skills: list = []
    ats_score: float     = 0.0

    if history:
        history_reversed = list(reversed(history))
        selector_labels  = [
            f"{e['resume_name']}  —  ATS {e.get('ats_score', 0):.0f}/100  —  {e['timestamp']}"
            for e in history_reversed
        ]

        st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
        selected_label = st.selectbox(
            "Select Previous Analysis to generate Interview Questions",
            selector_labels,
            index=0,
            help="Choose any past analysis — questions will be tailored to those matched & missing skills.",
        )

        selected_entry = history_reversed[selector_labels.index(selected_label)]
        matched_skills = selected_entry.get("matched", [])
        missing_skills = selected_entry.get("missing", [])
        ats_score      = selected_entry.get("ats_score", 0.0)

        st.markdown("####  Skills from Selected Analysis")

        sc1, sc2 = st.columns(2)
        with sc1:
            chips = "".join(
                f'<span class="chip chip-match">{s}</span>'
                for s in matched_skills[:10]
            ) or '<span style="color:rgba(255,255,255,0.3);font-size:0.8rem">None</span>'
            st.markdown(f"""
            <div class="card" style="padding:14px">
                <div class="card-title"> Matched Skills ({len(matched_skills)})</div>
                <div class="chip-row" style="margin-top:6px">{chips}</div>
                <div class="card-sub" style="margin-top:8px">Will generate MEDIUM–HARD questions</div>
            </div>""", unsafe_allow_html=True)
        with sc2:
            miss = "".join(
                f'<span class="chip">{s}</span>'
                for s in missing_skills[:10]
            ) or '<span style="color:rgba(255,255,255,0.3);font-size:0.8rem">None</span>'
            st.markdown(f"""
            <div class="card" style="padding:14px">
                <div class="card-title"> Gap Skills ({len(missing_skills)})</div>
                <div class="chip-row" style="margin-top:6px">{miss}</div>
                <div class="card-sub" style="margin-top:8px">Will generate EASY–MEDIUM questions</div>
            </div>""", unsafe_allow_html=True)

        st.markdown(
            f'<div class="card-sub" style="margin-top:6px"> Based on: '
            f'<b>{selected_entry["resume_name"]}</b> — ATS {ats_score:.0f}/100 — {selected_entry["timestamp"]}</div>',
            unsafe_allow_html=True,
        )
    else:
        st.info(
            " No analysis found. Run a **Quick Analyze** from the Dashboard first "
            "so the coach has your matched & missing skills to work with."
        )

    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)
    st.markdown("---")

    # ── Generate button ───
    if st.button("  Generate Interview Questions", type="primary", use_container_width=True):
        if not chosen_resume:
            st.error("Please upload and select a resume from the Dashboard first.")
        elif not role.strip():
            st.error("Please enter your target role above.")
        elif not matched_skills and not missing_skills:
            st.error(
                "No skills data found. Run a resume analysis from the Dashboard "
                "before using the Interview Coach."
            )
        else:
            with st.spinner(
                " AI is crafting your personalised questions… "
                "(first run may take 30–60 s while the model loads)"
            ):
                try:
                    resume_text = parse_resume(chosen_resume["path"])
                    projects    = extract_projects_from_text(resume_text)

                    result = generate_interview_questions(
                        role           = role.strip(),
                        matched_skills = matched_skills,
                        missing_skills = missing_skills,
                        projects       = projects,
                        ats_score      = ats_score,
                    )
                    st.session_state["interview_result"] = {
                        "data": result,
                        "role": role.strip(),
                        "resume": chosen_resume["name"],
                    }
                    st.rerun()

                except Exception as exc:
                    err = str(exc)
                    if "ConnectionError" in type(exc).__name__ or "Connection refused" in err:
                        st.error(
                            " Cannot reach Ollama. Make sure it is running:\n\n"
                            "```\nollama serve\nollama pull llama3\n```"
                        )
                    elif "Timeout" in type(exc).__name__:
                        st.error(" Groq timed out. The model may still be loading — try again in 30 s.")
                    else:
                        st.error(f" {exc}")

    # ── Results ─────
    cached = st.session_state.get("interview_result")
    if cached:
        _show_interview_results(cached["data"], cached["role"], cached["resume"])


# HELPER: Render interview question results
def _show_interview_results(result: dict, role: str = "", resume: str = "") -> None:
    """Render the 4-section interview Q&A card layout."""


    _DIFF_COLOR = {
        "easy":   ("#22c55e", "rgba(34,197,94,0.12)",  "rgba(34,197,94,0.25)"),
        "medium": ("#f59e0b", "rgba(245,158,11,0.12)", "rgba(245,158,11,0.25)"),
        "hard":   ("#ef4444", "rgba(239,68,68,0.12)",  "rgba(239,68,68,0.25)"),
    }

    def _diff_badge(difficulty: str) -> str:
        d = difficulty.lower()
        color, bg, border = _DIFF_COLOR.get(d, ("#FA4B4C", "rgba(250,75,76,0.12)", "rgba(250,75,76,0.25)"))
        label = d.upper()
        return (
            f'<span style="background:{bg};border:1px solid {border};border-radius:999px;'
            f'padding:2px 10px;font-size:0.7rem;font-weight:700;color:{color};'
            f'letter-spacing:0.06em">{label}</span>'
        )

    def _q_card(q: dict, idx: int, show_skill: bool = False) -> str:
        diff     = q.get("difficulty", "medium")
        badge    = _diff_badge(diff)
        skill_line = ""
        if show_skill and q.get("skill"):
            skill_line = (
                f'<div style="font-size:0.72rem;color:rgba(255,255,255,0.3);'
                f'margin-top:4px">Skill: {q["skill"]}</div>'
            )
        return (
            f'<div style="background:rgba(255,255,255,0.03);border:1px solid '
            f'rgba(255,255,255,0.07);border-radius:10px;padding:12px 16px;margin-bottom:10px">'
            f'<div style="display:flex;align-items:flex-start;gap:10px">'
            f'<span style="color:rgba(255,255,255,0.25);font-size:0.8rem;min-width:20px;'
            f'padding-top:1px">Q{idx}</span>'
            f'<div style="flex:1">'
            f'<div style="font-size:0.9rem;color:#e8e8f0;line-height:1.5">{q.get("question","")}</div>'
            f'{skill_line}'
            f'</div>'
            f'<div style="flex-shrink:0">{badge}</div>'
            f'</div></div>'
        )

    st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)
    st.markdown("---")

    st.markdown(f"""
    <div style="background:rgba(250,75,76,0.08);
                border:1px solid rgba(250,75,76,0.25);border-radius:14px;padding:20px 24px;
                margin-bottom:24px;">
        <div style="font-family:'Syne',sans-serif;font-size:1.15rem;font-weight:800;color:#fff">
             Interview Questions — {role}
        </div>
        <div style="font-size:0.82rem;color:rgba(255,255,255,0.4);margin-top:4px">
            Resume: {resume} &nbsp;·&nbsp; Generated by Hirelytics AI
        </div>
    </div>
    """, unsafe_allow_html=True)

    #  1. Technical Questions 
    tech_qs = result.get("technical_questions", [])
    with st.expander(f" Technical Questions ({len(tech_qs)})  —  MEDIUM to HARD", expanded=True):
        if tech_qs:
            for i, q in enumerate(tech_qs):
                st.markdown(_q_card(q, i + 1, show_skill=True), unsafe_allow_html=True)
                answer = q.get("answer", "").strip()
                if answer:
                    show = st.toggle(" Show Answer", key=f"tech_ans_{i}")
                    if show:
                        st.markdown(
                            f'<div style="background:rgba(250,75,76,0.07);border-left:3px solid #FA4B4C;'
                            f'border-radius:0 8px 8px 0;padding:12px 16px;margin:4px 0 8px;'
                            f'font-size:0.88rem;color:rgba(255,255,255,0.80);line-height:1.7">'
                            f'{answer}</div>',
                            unsafe_allow_html=True,
                        )
                st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
        else:
            st.info("No technical questions generated.")

    #  2. Gap / Missing Skill Questions 
    gap_qs = result.get("gap_questions", [])
    with st.expander(f"📚 Gap Questions ({len(gap_qs)})  —  EASY to MEDIUM", expanded=True):
        if gap_qs:
            for i, q in enumerate(gap_qs):
                st.markdown(_q_card(q, i + 1, show_skill=True), unsafe_allow_html=True)
                answer = q.get("answer", "").strip()
                if answer:
                    show = st.toggle(" Show Answer", key=f"gap_ans_{i}")
                    if show:
                        st.markdown(
                            f'<div style="background:rgba(34,197,94,0.07);border-left:3px solid #22c55e;'
                            f'border-radius:0 8px 8px 0;padding:12px 16px;margin:4px 0 8px;'
                            f'font-size:0.88rem;color:rgba(255,255,255,0.80);line-height:1.7">'
                            f'{answer}</div>',
                            unsafe_allow_html=True,
                        )
                st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
        else:
            st.info("No gap questions generated.")

    # 3. Project Section 
    project = result.get("project", {})
    proj_qs = project.get("questions", [])
    proj_name = project.get("project_name", "Your Project")
    with st.expander(f" Project Deep-Dive — {proj_name}", expanded=True):
        summary = project.get("summary", "")
        if summary:
            st.markdown(f"""
            <div style="background:rgba(250,75,76,0.07);border:1px solid rgba(250,75,76,0.20);
                        border-radius:10px;padding:14px 18px;margin-bottom:14px;
                        font-size:0.88rem;color:rgba(255,255,255,0.75);line-height:1.6">
                <div style="font-size:0.72rem;color:#FA4B4C;font-weight:700;
                            letter-spacing:0.08em;margin-bottom:6px">PROJECT SUMMARY</div>
                {summary}
            </div>""", unsafe_allow_html=True)
        if proj_qs:
            html = "".join(_q_card(q, i + 1) for i, q in enumerate(proj_qs))
            st.markdown(html, unsafe_allow_html=True)
        else:
            st.info("No project questions generated.")

    #  4. Behavioral Questions 
    beh_qs = result.get("behavioral_questions", [])
    with st.expander(f" Behavioral Questions ({len(beh_qs)})", expanded=False):
        if beh_qs:
            for i, q in enumerate(beh_qs):
                st.markdown(f"""
                <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);
                            border-radius:10px;padding:12px 16px;margin-bottom:10px">
                    <div style="display:flex;gap:10px;align-items:flex-start">
                        <span style="color:rgba(255,255,255,0.25);font-size:0.8rem;min-width:20px">Q{i+1}</span>
                        <div style="font-size:0.9rem;color:#e8e8f0;line-height:1.5">{q.get("question","")}</div>
                    </div>
                </div>""", unsafe_allow_html=True)
        else:
            st.info("No behavioral questions generated.")

    #  Clear / Regenerate 
    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
    if st.button("  Clear & Generate New Questions", use_container_width=True):
        st.session_state.pop("interview_result", None)
        st.rerun()


# SHARED: Real ATS Pipeline

def _run_real_analysis(
    jd_text: str,
    uploaded_file=None,
    file_path: str = None,
    resume_name: str = None,
) -> None:
    """
    Full pipeline: PDF → text → skill extraction → ATS scoring → display.

    Accepts either:
      • uploaded_file  – a Streamlit UploadedFile (from a file_uploader widget)
      • file_path      – path to an already-saved PDF on disk (selected resume)
    Saves results to analysis_history automatically.
    """
    from src.parser import parse_resume
    from src.skills_extractor import extract_skills, compare_skills
    from src.scorer import compute_ats_score

    st.markdown("---")
    st.markdown("""
    <div class="section-heading"> Analysis Results</div>
    <div class="section-sub">Powered by Hirelytics AI Engine.</div>
    """, unsafe_allow_html=True)

    with st.spinner("Parsing resume & computing ATS score… (first run may take ~30 s to load the embedding model)"):

        # ── 1. Get resume text ─────
        if file_path:
            # Selected saved resume — read directly from disk
            resume_text = parse_resume(file_path)
            resume_name = resume_name or Path(file_path).name
        else:
        
            os.makedirs(_RESUME_DIR, exist_ok=True)
            tmp_path = os.path.join(_RESUME_DIR, f"_tmp_{uploaded_file.name}")
            try:
                with open(tmp_path, "wb") as fh:
                    fh.write(uploaded_file.getbuffer())
                resume_text = parse_resume(tmp_path)
            finally:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
            resume_name = resume_name or uploaded_file.name

        # ── 2. Extract & compare skills ───
        resume_skills = extract_skills(resume_text)
        jd_skills     = extract_skills(jd_text)
        matched, missing = compare_skills(resume_skills, jd_skills)

        # ── 3. Compute ATS score ──
        result = compute_ats_score(resume_text, jd_text, matched, missing)

    # ── 4. Persist to history ────
    _save_to_history(resume_name, jd_text, result)

    # ── 5. Display ───
    _show_real_results(result)


def _show_real_results(result) -> None:
    """Render the ATSResult returned by compute_ats_score()."""

    score = result.ats_score

    # Score → colour and label
    if score >= 80:
        ring_color = "#22c55e"
        score_label = "Excellent match!"
    elif score >= 60:
        ring_color = "#FA4B4C"
        score_label = "Good — room to improve"
    elif score >= 40:
        ring_color = "#f59e0b"
        score_label = "Fair — needs significant work"
    else:
        ring_color = "#ef4444"
        score_label = "Poor match — review the JD"

    degrees = round((score / 100) * 360)

    r1, r2, r3 = st.columns(3)

    # ── ATS Score ring ─────
    with r1:
        st.markdown(f"""
        <div class="card" style="text-align:center;">
            <div class="card-title" style="text-align:center">ATS Score</div>
            <div class="score-ring" style="background:conic-gradient(
                {ring_color} 0deg,
                {ring_color} {degrees}deg,
                rgba(255,255,255,0.06) {degrees}deg 360deg
            );">
                <div class="score-inner">
                    <div class="score-num" style="color:{ring_color}">{score:.0f}</div>
                    <div class="score-label">/ 100</div>
                </div>
            </div>
            <div class="card-sub" style="text-align:center">{score_label}</div>
        </div>
        """, unsafe_allow_html=True)

    with r2:
        chips = "".join(
            f'<span class="chip chip-match">{s}</span>'
            for s in result.matched_skills[:12]   # cap at 12 to avoid overflow
        ) if result.matched_skills else '<span style="color:rgba(255,255,255,0.3);font-size:0.8rem">No matching skills found</span>'
        total_jd  = len(result.matched_skills) + len(result.missing_skills)
        matched_n = len(result.matched_skills)
        st.markdown(f"""
        <div class="card">
            <div class="card-title"> Keyword Matches</div>
            <div class="chip-row">{chips}</div>
            <div class="card-sub" style="margin-top:12px">
                {matched_n} of {total_jd} JD keywords matched
            </div>
        </div>
        """, unsafe_allow_html=True)
    with r3:
        miss_chips = "".join(
            f'<span class="chip">{s}</span>'
            for s in result.missing_skills[:12]
        ) if result.missing_skills else '<span style="color:#86efac;font-size:0.8rem">All JD skills found in your resume 🎉</span>'
        miss_n = len(result.missing_skills)
        st.markdown(f"""
        <div class="card">
            <div class="card-title"> Missing Skills</div>
            <div class="chip-row">{miss_chips}</div>
            <div class="card-sub" style="margin-top:12px">
                {miss_n} skill(s) to add for a better score
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Sub-score breakdown ────
    st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

    with st.expander(" Score Breakdown", expanded=False):
        b1, b2, b3 = st.columns(3)
        with b1:
            st.metric("Keyword Match", f"{result.keyword_score*100:.1f}%",
                      help="How many JD skills appear in your resume (weight: 50%)")
        with b2:
            st.metric("Semantic Similarity", f"{result.semantic_score*100:.1f}%",
                      help="How closely your resume language matches the JD (weight: 25%)")
        with b3:
            st.metric("Section Coverage", f"{result.section_score*100:.1f}%",
                      help="Presence of Skills, Experience, Projects sections (weight: 25%)")

    # ── Improvement suggestions ────
    with st.expander(" Improvement Suggestions", expanded=True):
        suggestions = []
        if result.missing_skills:
            top_missing = ", ".join(result.missing_skills[:5])
            suggestions.append(
                f"Add these missing skills to your resume if you have experience with them: **{top_missing}**"
            )
        if result.keyword_score < 0.5:
            suggestions.append(
                "Your keyword match is below 50%. Mirror the exact wording from the JD in your skills section."
            )
        if result.semantic_score < 0.4:
            suggestions.append(
                "Your overall language is not closely aligned with this role. "
                "Tailor your summary and bullet points to match the JD's tone and focus."
            )
        if not result.sections_found.get("projects", False):
            suggestions.append(
                "Add a **Projects** section — many ATS systems score it as a required section."
            )
        if not result.sections_found.get("skills", False):
            suggestions.append(
                "Add a dedicated **Skills** section for better ATS keyword detection."
            )
        if result.ats_score >= 80:
            suggestions.append(
                "Great match! Quantify achievements with numbers "
                "(e.g., 'Reduced inference latency by 40%') to stand out further."
            )
        if not suggestions:
            suggestions.append("Your resume is well-aligned with this job description. Keep it up!")

        for s in suggestions:
            st.markdown(f"- {s}")


# ── Entry point ─────
# Streamlit executes this file as a script, so show_home() must be called
# at module level for the page to actually render.
show_home()

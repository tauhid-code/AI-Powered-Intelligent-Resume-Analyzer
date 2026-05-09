import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

API_BASE = os.getenv("API_BASE_URL", "http://localhost:8000")


st.set_page_config(
    page_title="Hirelytics AI — Sign In",
    layout="centered",
    initial_sidebar_state="collapsed",
)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@400;500;600;700&display=swap');

/* ── Hide Streamlit chrome───── */
[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"],
#MainMenu, footer,
section[data-testid="stSidebar"] {
    display: none !important;
}

/* ── Page background─── */
.stApp, [data-testid="stAppViewContainer"] {
    background: #0e1117 !important;
}
[data-testid="stAppViewBlockContainer"],
.block-container {
    background: transparent !important;
    padding-top: 3.5rem !important;
    max-width: 480px !important;
}

/* ── Global font─── */
.stApp * {
    font-family: 'DM Sans', sans-serif !important;
    color: rgba(255,255,255,0.85) !important;
}

/* ── Divider────── */
hr {
    border-color: rgba(255,255,255,0.08) !important;
}

/* ── Text inputs — label─── */
[data-testid="stTextInput"] label,
[data-testid="stTextInput"] p {
    color: rgba(255,255,255,0.55) !important;
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.04em !important;
    text-transform: uppercase !important;
}
/* Text inputs — field */
[data-testid="stTextInput"] input {
    background:    #1F1F1F !important;
    border:        1px solid rgba(255,255,255,0.10) !important;
    border-radius: 10px !important;
    color:         #ffffff !important;
    font-size:     0.9rem !important;
    padding:       0.55rem 0.9rem !important;
    transition:    border-color 0.2s, box-shadow 0.2s !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: #FA4B4C !important;
    box-shadow:   0 0 0 3px rgba(250,75,76,0.20) !important;
    outline:      none !important;
}
[data-testid="stTextInput"] input::placeholder {
    color: rgba(255,255,255,0.25) !important;
}
/* Input wrapper divs — kill any white background */
[data-testid="stTextInput"] > div,
[data-testid="stTextInput"] > div > div {
    background: #1F1F1F !important;
    border-radius: 10px !important;
}
/* Eye icon button — match input background exactly */
[data-testid="stTextInput"] button,
[data-testid="stTextInput"] button > div,
[data-testid="stTextInput"] button svg {
    background:    #1F1F1F !important;
    border:        none !important;
    border-radius: 0 10px 10px 0 !important;
    color:         rgba(255,255,255,0.40) !important;
    fill:          rgba(255,255,255,0.40) !important;
}
[data-testid="stTextInput"] button:hover,
[data-testid="stTextInput"] button:hover svg {
    background: #1F1F1F !important;
    color:      rgba(255,255,255,0.80) !important;
    fill:       rgba(255,255,255,0.80) !important;
}

/* ── All buttons — base─ */
.stButton > button {
    border-radius:  10px !important;
    font-family:    'DM Sans', sans-serif !important;
    font-size:      0.875rem !important;
    font-weight:    600 !important;
    transition:     all 0.18s ease !important;
    padding:        0.6rem 1.2rem !important;
    letter-spacing: 0.01em !important;
}

/* Primary buttons */
.stButton > button[kind="primary"] {
    background: #FA4B4C !important;
    border:     none !important;
    color:      #ffffff !important;
    box-shadow: 0 4px 14px rgba(250,75,76,0.35) !important;
}
.stButton > button[kind="primary"]:hover {
    background: #e03e3f !important;
    box-shadow: 0 6px 20px rgba(250,75,76,0.50) !important;
    transform:  translateY(-1px) !important;
}
.stButton > button[kind="primary"]:active {
    transform: translateY(0) !important;
}

/* Secondary buttons */
.stButton > button[kind="secondary"] {
    background:  rgba(255,255,255,0.04) !important;
    border:      1px solid rgba(255,255,255,0.12) !important;
    color:       rgba(255,255,255,0.65) !important;
}
.stButton > button[kind="secondary"]:hover {
    background:   rgba(250,75,76,0.08) !important;
    border-color: rgba(250,75,76,0.45) !important;
    color:        #ffffff !important;
}

/* Form submit button */
[data-testid="stForm"] [data-testid="stFormSubmitButton"] > button {
    background:    #FA4B4C !important;
    border:        none !important;
    color:         #ffffff !important;
    font-size:     0.92rem !important;
    font-weight:   700 !important;
    border-radius: 10px !important;
    padding:       0.7rem 1.2rem !important;
    box-shadow:    0 4px 14px rgba(250,75,76,0.35) !important;
    transition:    all 0.18s ease !important;
    width:         100% !important;
}
[data-testid="stForm"] [data-testid="stFormSubmitButton"] > button:hover {
    background: #e03e3f !important;
    box-shadow: 0 6px 20px rgba(250,75,76,0.50) !important;
    transform:  translateY(-1px) !important;
}

/* ── Form container── */
[data-testid="stForm"] {
    background:    rgba(255,255,255,0.03) !important;
    border:        1px solid rgba(255,255,255,0.08) !important;
    border-radius: 14px !important;
    padding:       1.4rem 1.6rem !important;
}

/* ── Checkbox ─── */
[data-testid="stCheckbox"] label span {
    color: rgba(255,255,255,0.55) !important;
    font-size: 0.82rem !important;
}
[data-testid="stCheckbox"] input:checked + div {
    background:   #FA4B4C !important;
    border-color: #FA4B4C !important;
}

/* ── Caption / small text ──── */
.stApp [data-testid="stCaptionContainer"] p,
.stApp small,
.stApp .stCaption p {
    color:     rgba(255,255,255,0.30) !important;
    font-size: 0.78rem !important;
}

/* ── Alert boxes─── */
[data-testid="stAlert"] {
    background:    rgba(255,255,255,0.04) !important;
    border-radius: 10px !important;
}
</style>
""", unsafe_allow_html=True)


_defaults = {
    "auth_mode":  "login",
    "jwt_token":  None,
    "user_name":  None,
    "user_email": None,
}
for k, v in _defaults.items():
    st.session_state.setdefault(k, v)

if st.session_state.jwt_token:
    st.switch_page("pages/home.py")


# ── API helpers ──
def api_login(email: str, password: str) -> requests.Response:
    return requests.post(
        f"{API_BASE}/auth/login",
        json={"email": email, "password": password},
        timeout=10,
    )

def api_signup(name: str, email: str, password: str) -> requests.Response:
    return requests.post(
        f"{API_BASE}/auth/signup",
        json={"name": name, "email": email, "password": password},
        timeout=10,
    )

def password_strength(pw: str) -> tuple:
    score = 0
    if len(pw) >= 8:  score += 25
    if len(pw) >= 12: score += 15
    if any(c.isupper() for c in pw):  score += 20
    if any(c.isdigit() for c in pw):  score += 20
    if any(c in r"!@#$%^&*()_+-=[]{};':\"|,.<>/?" for c in pw): score += 20
    if score <= 30: return score, "Weak",   "#ef4444"
    if score <= 55: return score, "Fair",   "#f97316"
    if score <= 75: return score, "Good",   "#eab308"
    return score, "Strong", "#22c55e"


# ── Header and description ──
st.markdown("""
<div style="text-align:center; margin-bottom:1rem;">
    <div style="
        font-family:'Syne',sans-serif;
        font-size:2rem;
        font-weight:800;
        color:#ffffff;
        letter-spacing:-0.5px;
        line-height:1.1;
        margin-bottom:6px;
    ">Hirelytics AI</div>
    <div style="color:rgba(255,255,255,0.35);font-size:0.9rem;letter-spacing:0.02em;">
        Smarter hiring, powered by artificial intelligence
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("<hr style='border-color:rgba(255,255,255,0.07);margin-bottom:1.4rem'>",
            unsafe_allow_html=True)


# ── Google login button ───
google_clicked = st.button(
    "  Continue with Google",
    use_container_width=True,
    key="btn_google",
    type="secondary",
)
if google_clicked:
    st.info(" Google OAuth is not connected yet. Use email/password login below.")

st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

# ── OR divider ──
st.markdown("""
<div style="display:flex;align-items:center;gap:10px;margin:4px 0 12px">
    <div style="flex:1;height:1px;background:rgba(255,255,255,0.08)"></div>
    <span style="color:rgba(255,255,255,0.25);font-size:0.72rem;letter-spacing:0.12em;font-weight:600;">
        OR CONTINUE WITH EMAIL
    </span>
    <div style="flex:1;height:1px;background:rgba(255,255,255,0.08)"></div>
</div>
""", unsafe_allow_html=True)


# ── Sign In / Sign Up tab switcher ───
tab_a, tab_b = st.columns(2)
with tab_a:
    if st.button(
        "Sign In",
        key="tab_login",
        use_container_width=True,
        type="primary" if st.session_state.auth_mode == "login" else "secondary",
    ):
        st.session_state.auth_mode = "login"
        st.rerun()

with tab_b:
    if st.button(
        "Sign Up",
        key="tab_signup",
        use_container_width=True,
        type="primary" if st.session_state.auth_mode == "signup" else "secondary",
    ):
        st.session_state.auth_mode = "signup"
        st.rerun()

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)


# ── LOGIN FORM ────
if st.session_state.auth_mode == "login":

    with st.form("login_form", clear_on_submit=False):
        email    = st.text_input("Email Address", placeholder="you@company.com",     key="li_email")
        password = st.text_input("Password",      placeholder="Enter your password", key="li_pw", type="password")
        st.caption("Forgot password? Contact support to reset it.")
        submitted = st.form_submit_button("Sign In  →", use_container_width=True, type="primary")

    if submitted:
        if not email.strip() or not password:
            st.error(" Please enter both your email and password.")
        else:
            with st.spinner("Verifying credentials…"):
                try:
                    resp = api_login(email.strip().lower(), password)
                    if resp.status_code == 200:
                        data = resp.json()
                        # Clear any previous user's data before setting new session
                        for _k in ("stored_resumes", "analysis_history",
                                   "selected_resume", "interview_result", "active_page"):
                            st.session_state.pop(_k, None)
                        st.session_state.jwt_token  = data["access_token"]
                        st.session_state.user_name  = data["name"]
                        st.session_state.user_email = data["email"]
                        st.success(f"  Welcome back, **{data['name']}**! Loading your dashboard…")
                        st.switch_page("pages/home.py")
                    elif resp.status_code == 401:
                        st.error("  Incorrect email or password.")
                    else:
                        st.error(f"  {resp.json().get('detail', 'Login failed.')}")
                except requests.exceptions.ConnectionError:
                    st.error("  API server unreachable. Make sure FastAPI is running on port 8000.")
                except Exception as e:
                    st.error(f"Unexpected error: {e}")

    st.markdown(
        "<p style='text-align:center;color:rgba(255,255,255,0.28);font-size:0.8rem;margin-top:10px'>"
        "No account yet? Use the <b style='color:#FA4B4C'>Sign Up</b> tab above →</p>",
        unsafe_allow_html=True,
    )


# ── SIGNUP FORM ────
else:

    with st.form("signup_form", clear_on_submit=False):
        name    = st.text_input("Full Name",        placeholder="Jane Doe",           key="su_name")
        email   = st.text_input("Work Email",       placeholder="jane@company.com",   key="su_email")
        pw      = st.text_input("Password",         placeholder="Min. 8 characters",  key="su_pw",      type="password")
        pw_conf = st.text_input("Confirm Password", placeholder="Re-enter password",  key="su_confirm", type="password")

        if pw:
            pct, label, colour = password_strength(pw)
            st.markdown(f"""
            <div style="display:flex;align-items:center;gap:8px;margin:2px 0 8px">
                <div style="flex:1;height:4px;border-radius:3px;background:rgba(255,255,255,0.10);overflow:hidden">
                    <div style="width:{pct}%;height:100%;background:{colour};border-radius:3px;
                                transition:width .35s,background .35s"></div>
                </div>
                <span style="font-size:0.75rem;color:{colour};font-weight:600">{label}</span>
            </div>""", unsafe_allow_html=True)

        agreed    = st.checkbox("I agree to the Terms of Service and Privacy Policy", key="su_terms")
        submitted = st.form_submit_button("Create Account  →", use_container_width=True, type="primary")

    if submitted:
        errs = []
        if not name.strip():  errs.append("Full name is required.")
        if not email.strip(): errs.append("Email is required.")
        if len(pw) < 8:       errs.append("Password must be at least 8 characters.")
        if pw != pw_conf:     errs.append("Passwords do not match.")
        if not agreed:        errs.append("Please accept the Terms of Service.")

        if errs:
            for e in errs:
                st.error(f"  {e}")
        else:
            with st.spinner("Creating your account…"):
                try:
                    resp = api_signup(name.strip(), email.strip().lower(), pw)
                    if resp.status_code == 201:
                        st.success(" Account created! Tap **Sign In** to log in.")
                        st.session_state.auth_mode = "login"
                        st.rerun()
                    elif resp.status_code == 409:
                        st.error("  An account with that email already exists.")
                    else:
                        st.error(f"  {resp.json().get('detail', 'Signup failed.')}")
                except requests.exceptions.ConnectionError:
                    st.error("🔌  API server unreachable. Make sure FastAPI is running on port 8000.")
                except Exception as e:
                    st.error(f"Unexpected error: {e}")

    st.markdown(
        "<p style='text-align:center;color:rgba(255,255,255,0.28);font-size:0.8rem;margin-top:10px'>"
        "Already have an account? Use the <b style='color:#FA4B4C'>Sign In</b> tab above →</p>",
        unsafe_allow_html=True,
    )


# ── Footer ────
st.markdown("""
<div style="
    text-align:center;
    margin-top:2rem;
    padding-top:1.2rem;
    border-top:1px solid rgba(255,255,255,0.07);
    color:rgba(255,255,255,0.20);
    font-size:0.75rem;
    letter-spacing:0.03em;
">
    © 2025 Hirelytics AI &nbsp;·&nbsp; Secured with JWT &amp; bcrypt
</div>
""", unsafe_allow_html=True)

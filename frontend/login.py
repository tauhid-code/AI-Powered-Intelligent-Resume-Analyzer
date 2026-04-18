import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

API_BASE = os.getenv("API_BASE_URL", "http://localhost:8000")

# Page config
st.set_page_config(
    page_title="Hirelytics AI — Sign In",
    page_icon="🎯",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# CSS styles for the login/signup page

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Syne:wght@700;800&display=swap');

[data-testid="stAppViewContainer"] > .main {
    background: #071424;
    background-image:
        radial-gradient(ellipse 80% 60% at 20% 0%,  rgba(15,61,94,0.55)  0%, transparent 60%),
        radial-gradient(ellipse 60% 50% at 80% 100%, rgba(58,124,165,0.3) 0%, transparent 60%);
    min-height: 100vh;
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"],
#MainMenu, footer,
section[data-testid="stSidebar"] {
    display: none !important;
}

.block-container {
    padding-top: 4rem !important;
    padding-bottom: 4rem !important;
    max-width: 860px !important;
    min-width: 720px !important;
    width: 860px !important;
}

[data-testid="stVerticalBlockBorderWrapper"] {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
    margin: 0 !important;
}

.card-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.6rem;
    font-weight: 800;
    letter-spacing: -0.5px;
    background: linear-gradient(90deg, #d6eeff 0%, #81a4cd 55%, #3a7ca5 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-align: center;
    margin: 0 0 0.4rem;
    line-height: 1.2;
}
.card-sub {
    text-align: center;
    color: rgba(255,255,255,0.35);
    font-size: 1rem;
    letter-spacing: 0.2px;
    margin-bottom: 2.2rem;
}

.social-row {
    display: flex;
    gap: 10px;
    margin: 1rem 0 0;
}
.social-btn {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    background: rgba(255,255,255,0.055);
    border: 1px solid rgba(255,255,255,0.11);
    border-radius: 11px;
    padding: 0.9rem 0.5rem;
    color: rgba(255,255,255,0.65);
    font-size: 1rem;
    font-weight: 500;
    cursor: pointer;
}

.or-divider {
    display: flex;
    align-items: center;
    gap: 10px;
    margin: 1rem 0;
}
.or-line  { flex: 1; height: 1px; background: rgba(255,255,255,0.09); }
.or-label { color: rgba(255,255,255,0.25); font-size: 0.7rem; letter-spacing: 0.7px; white-space: nowrap; }

.stButton > button {
    background: transparent !important;
    border: 1px solid rgba(255,255,255,0.13) !important;
    color: rgba(255,255,255,0.5) !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    padding: 0.6rem !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: rgba(58,124,165,0.12) !important;
    border-color: rgba(58,124,165,0.4) !important;
    color: #fff !important;
}

.stTextInput label {
    color: rgba(255,255,255,0.55) !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.7px !important;
    text-transform: uppercase !important;
}

.stTextInput > div > div {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    border-radius: 11px !important;
    transition: all 0.2s !important;
}
.stTextInput > div > div:focus-within {
    border-color: #3a7ca5 !important;
    box-shadow: 0 0 0 3px rgba(58,124,165,0.2) !important;
    background: rgba(255,255,255,0.09) !important;
}
.stTextInput > div > div > input {
    color: #fff !important;
    font-size: 1.05rem !important;
    padding: 0.95rem 1.2rem !important;
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    caret-color: #81a4cd !important;
}
.stTextInput > div > div > input::placeholder {
    color: rgba(255,255,255,0.2) !important;
}

.stCheckbox label { color: rgba(255,255,255,0.5) !important; font-size: 0.82rem !important; }

div[data-testid="stFormSubmitButton"] > button {
    width: 100% !important;
    background: linear-gradient(135deg, #0f3d5e 0%, #3a7ca5 100%) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 1.05rem 1.5rem !important;
    font-size: 1.12rem !important;
    font-weight: 700 !important;
    margin-top: 0.7rem !important;
    box-shadow: 0 6px 22px rgba(15,61,94,0.5) !important;
    transition: all 0.2s ease !important;
}
div[data-testid="stFormSubmitButton"] > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 28px rgba(58,124,165,0.55) !important;
    background: linear-gradient(135deg, #1a5276 0%, #4a90c4 100%) !important;
}
div[data-testid="stFormSubmitButton"] > button:active {
    transform: translateY(0) !important;
}

.strength-wrap { display:flex; align-items:center; gap:8px; margin: 4px 0 8px; }
.strength-track { flex:1; height:3px; border-radius:3px; background:rgba(255,255,255,0.09); overflow:hidden; }
.strength-fill  { height:100%; border-radius:3px; transition: width .35s, background .35s; }
.strength-label { font-size:0.7rem; min-width:44px; text-align:right; }

.footer-note {
    text-align: center;
    color: rgba(255,255,255,0.3);
    font-size: 0.8rem;
    margin-top: 1.2rem;
}
.footer-note span { color: #81a4cd; font-weight: 600; cursor: pointer; }
.footer-note span:hover { color: #cde8ff; }

.stAlert { border-radius: 11px !important; font-size: 0.87rem !important; }

::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-thumb { background: rgba(58,124,165,0.35); border-radius: 4px; }
</style>
""", unsafe_allow_html=True)


# Session state defaults

_defaults = {
    "auth_mode":  "login",
    "jwt_token":  None,
    "user_name":  None,
    "user_email": None,
}
for k, v in _defaults.items():
    st.session_state.setdefault(k, v)

if st.session_state.jwt_token:
    st.switch_page("pages/app.py")



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


st.markdown("""
<div class="card-title">Hirelytics AI</div>
<div class="card-sub">Smarter hiring, powered by artificial intelligence</div>
""", unsafe_allow_html=True)

# Tab toggle
col_a, col_b = st.columns(2)
with col_a:
    if st.button("Sign In", key="tab_login", use_container_width=True):
        st.session_state.auth_mode = "login"
        st.rerun()
with col_b:
    if st.button("Sign Up", key="tab_signup", use_container_width=True):
        st.session_state.auth_mode = "signup"
        st.rerun()

# Active tab highlight
nth = 1 if st.session_state.auth_mode == "login" else 2
st.markdown(f"""
<style>
div[data-testid="column"]:nth-child({nth}) .stButton > button {{
    background: linear-gradient(135deg,#0f3d5e,#3a7ca5) !important;
    color: #fff !important;
    border-color: transparent !important;
    box-shadow: 0 4px 16px rgba(15,61,94,.4) !important;
}}
</style>""", unsafe_allow_html=True)

st.markdown("""
<div class="social-row">
    <div class="social-btn">
        <svg width="14" height="14" viewBox="0 0 48 48">
            <path fill="#4285F4" d="M44.5 20H24v8.5h11.8C34.5 33.9 30 37 24 37c-7.2 0-13-5.8-13-13s5.8-13 13-13c3.1 0 5.9 1.1 8.1 2.9l6-6C34.6 5.1 29.6 3 24 3 12.4 3 3 12.4 3 24s9.4 21 21 21c10.5 0 20-7.5 20-21 0-1.4-.1-2.7-.5-4z"/>
        </svg>
        Google
    </div>
    <div class="social-btn">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="white">
            <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/>
        </svg>
        GitHub
    </div>
</div>
<div class="or-divider">
    <div class="or-line"></div>
    <span class="or-label">OR CONTINUE WITH EMAIL</span>
    <div class="or-line"></div>
</div>
""", unsafe_allow_html=True)


# LOGIN FORM

if st.session_state.auth_mode == "login":

    with st.form("login_form", clear_on_submit=False):
        email    = st.text_input("Email Address", placeholder="you@company.com",     key="li_email")
        password = st.text_input("Password",      placeholder="Enter your password", key="li_pw", type="password")
        st.markdown(
            '<p style="font-size:0.76rem;color:rgba(255,255,255,0.28);margin:2px 0 6px;">'
            'Forgot password? <span style="color:#81a4cd;cursor:pointer;">Reset it</span></p>',
            unsafe_allow_html=True,
        )
        submitted = st.form_submit_button("Sign In  →", use_container_width=True)

    if submitted:
        if not email.strip() or not password:
            st.error("⚠️  Please enter both your email and password.")
        else:
            with st.spinner("Verifying credentials…"):
                try:
                    resp = api_login(email.strip().lower(), password)
                    if resp.status_code == 200:
                        data = resp.json()
                        st.session_state.jwt_token  = data["access_token"]
                        st.session_state.user_name  = data["name"]
                        st.session_state.user_email = data["email"]
                        st.success(f"✅  Welcome back, **{data['name']}**! Loading your dashboard…")
                        st.switch_page("pages/app.py")
                        st.rerun()
                    elif resp.status_code == 401:
                        st.error("❌  Incorrect email or password.")
                    else:
                        st.error(f"❌  {resp.json().get('detail', 'Login failed.')}")
                except requests.exceptions.ConnectionError:
                    st.error("🔌  API server unreachable. Ensure FastAPI is running on port 8000.")
                except Exception as e:
                    st.error(f"Unexpected error: {e}")

    st.markdown(
        '<div class="footer-note">No account yet? '
        '<span onclick="void(0)">Use the Sign Up tab above →</span></div>',
        unsafe_allow_html=True,
    )

# SIGNUP FORM

else:

    with st.form("signup_form", clear_on_submit=False):
        name    = st.text_input("Full Name",        placeholder="Jane Doe",           key="su_name")
        email   = st.text_input("Work Email",       placeholder="jane@company.com",   key="su_email")
        pw      = st.text_input("Password",         placeholder="Min. 8 characters",  key="su_pw",      type="password")
        pw_conf = st.text_input("Confirm Password", placeholder="Re-enter password",  key="su_confirm", type="password")

        if pw:
            pct, label, colour = password_strength(pw)
            st.markdown(f"""
            <div class="strength-wrap">
                <div class="strength-track">
                    <div class="strength-fill" style="width:{pct}%;background:{colour};"></div>
                </div>
                <span class="strength-label" style="color:{colour};">{label}</span>
            </div>""", unsafe_allow_html=True)

        agreed    = st.checkbox("I agree to the Terms of Service and Privacy Policy", key="su_terms")
        submitted = st.form_submit_button("Create Account  →", use_container_width=True)

    if submitted:
        errs = []
        if not name.strip():  errs.append("Full name is required.")
        if not email.strip(): errs.append("Email is required.")
        if len(pw) < 8:       errs.append("Password must be at least 8 characters.")
        if pw != pw_conf:     errs.append("Passwords do not match.")
        if not agreed:        errs.append("Please accept the Terms of Service.")

        if errs:
            for e in errs:
                st.error(f"⚠️  {e}")
        else:
            with st.spinner("Creating your account…"):
                try:
                    resp = api_signup(name.strip(), email.strip().lower(), pw)
                    if resp.status_code == 201:
                        st.success("🎉  Account created! Tap **Sign In** to log in.")
                        st.session_state.auth_mode = "login"
                        st.rerun()
                    elif resp.status_code == 409:
                        st.error("❌  An account with that email already exists.")
                    else:
                        st.error(f"❌  {resp.json().get('detail', 'Signup failed.')}")
                except requests.exceptions.ConnectionError:
                    st.error("🔌  API server unreachable. Ensure FastAPI is running on port 8000.")
                except Exception as e:
                    st.error(f"Unexpected error: {e}")

    st.markdown(
        '<div class="footer-note">Already have an account? '
        '<span onclick="void(0)">Use the Sign In tab above →</span></div>',
        unsafe_allow_html=True,
    )

##Copyright note

st.markdown("""
<p style="text-align:center;color:rgba(255,255,255,0.15);font-size:0.68rem;
   margin-top:1.5rem;letter-spacing:0.4px;">
   © 2025 Hirelytics AI &nbsp;·&nbsp; Secured with JWT &amp; bcrypt
</p>
""", unsafe_allow_html=True)
"""
Hirelytics AI — Sidebar Navigation Component

Renders the left-hand navigation rail and returns the currently
active page key so the caller can route to the correct page.

Active page keys:
    "dashboard"       → main dashboard with Quick Analyze
    "analysis"        → full ATS analysis page
    "interview_coach" → AI interview coach (coming soon)
"""

import streamlit as st


#  Navigation Item Definitions
_NAV_ITEMS = [
    ("dashboard",       "",  "Dashboard"),
    ("analysis",        "", "Analysis History"),
    ("interview_coach", "", "AI Powered Interview Coach"),
]


_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@700;800&family=DM+Sans:wght@400;500;600;700&display=swap');

/* ── Sidebar shell──── */
[data-testid="stSidebar"] {
    background: #0e1117 !important;
    border-right: 1px solid rgba(255,255,255,0.07) !important;
}
[data-testid="stSidebar"] > div:first-child {
    padding-top: 0 !important;
}
[data-testid="stSidebarContent"] {
    padding: 0 !important;
}

/* ── ALL sidebar buttons — shared base── */
[data-testid="stSidebar"] .stButton > button {
    border-radius:   0 10px 10px 0 !important;
    font-family:     'DM Sans', sans-serif !important;
    font-size:       0.875rem !important;
    font-weight:     500 !important;
    text-align:      left !important;
    justify-content: flex-start !important;
    padding:         0.62rem 1.1rem !important;
    width:           100% !important;
    transition:      all 0.18s ease !important;
    box-shadow:      none !important;
    border-top:      none !important;
    border-right:    none !important;
    border-bottom:   none !important;
}

/* ── INACTIVE nav buttons (kind="secondary")── */
[data-testid="stSidebar"] .stButton > button[kind="secondary"] {
    background:  transparent !important;
    border-left: 3px solid transparent !important;
    color:       rgba(255,255,255,0.45) !important;
}
[data-testid="stSidebar"] .stButton > button[kind="secondary"]:hover {
    background:  rgba(250,75,76,0.06) !important;
    border-left: 3px solid rgba(250,75,76,0.40) !important;
    color:       rgba(255,255,255,0.85) !important;
}

/* ── ACTIVE nav button (kind="primary")──── */
[data-testid="stSidebar"] .stButton > button[kind="primary"] {
    background:  rgba(250,75,76,0.14) !important;
    border-left: 3px solid #FA4B4C !important;
    color:       #FA4B4C !important;
    font-weight: 700 !important;
}
[data-testid="stSidebar"] .stButton > button[kind="primary"]:hover {
    background:  rgba(250,75,76,0.22) !important;
    color:       #ff6b6c !important;
}
[data-testid="stSidebar"] .stButton > button[kind="primary"]:focus:not(:active) {
    box-shadow: none !important;
}

/* ── LOGOUT button────── */
.logout-marker + div .stButton > button {
    background:  transparent !important;
    border-left: 3px solid transparent !important;
    color:       rgba(239,68,68,0.6) !important;
    font-size:   0.82rem !important;
}
.logout-marker + div .stButton > button:hover {
    background:  rgba(239,68,68,0.08) !important;
    border-left: 3px solid #ef4444 !important;
    color:       #ef4444 !important;
}

/* ── Settings / Support (secondary, non-nav) ── */
[data-testid="stSidebar"] .stButton > button:focus:not(:active) {
    box-shadow: none !important;
}

/* ── Sidebar horizontal rule──── */
[data-testid="stSidebar"] hr {
    border-color: rgba(255,255,255,0.07) !important;
    margin: 6px 14px !important;
}


/* Logo */
.hl-logo {
    display:       flex;
    align-items:   center;
    gap:           11px;
    padding:       20px 18px 16px;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    margin-bottom: 8px;
}
.hl-logo-icon {
    background:    #FA4B4C;
    border-radius: 10px;
    width:         34px;
    height:        34px;
    display:         flex;
    align-items:     center;
    justify-content: center;
    font-size:   1.05rem;
    flex-shrink: 0;
}
.hl-logo-name {
    font-family:  'Syne', sans-serif;
    font-size:    1.0rem;
    font-weight:  800;
    color:        #ffffff;
    letter-spacing: -0.2px;
    line-height:    1.1;
}
.hl-logo-sub {
    font-size:      0.58rem;
    color:          rgba(255,255,255,0.22);
    letter-spacing: 0.04em;
    margin-top:     2px;
}

/* Section labels */
.hl-section-label {
    display:         block;
    font-family:     'DM Sans', sans-serif;
    font-size:       0.63rem;
    font-weight:     700;
    letter-spacing:  0.13em;
    text-transform:  uppercase;
    color:           rgba(255,255,255,0.2);
    padding:         0 1.15rem;
    margin:          10px 0 4px;
}

/* Premium badge */
.hl-premium {
    margin:        6px 14px 2px;
    background:    linear-gradient(90deg, rgba(34,197,94,0.13), rgba(34,197,94,0.05));
    border:        1px solid rgba(34,197,94,0.22);
    border-radius: 9px;
    padding:       8px 12px;
    display:       flex;
    align-items:   center;
    gap:           9px;
}
.hl-premium-dot {
    width:         7px;
    height:        7px;
    border-radius: 50%;
    background:    #22c55e;
    box-shadow:    0 0 7px rgba(34,197,94,0.55);
    flex-shrink:   0;
}
.hl-premium-label {
    font-size:      0.7rem;
    font-weight:    700;
    color:          #86efac;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}
.hl-premium-sub {
    font-size:  0.62rem;
    color:      rgba(255,255,255,0.25);
    margin-top: 1px;
}

/* User card */
.hl-user-card {
    margin:        6px 14px 2px;
    background:    rgba(255,255,255,0.04);
    border:        1px solid rgba(255,255,255,0.08);
    border-radius: 10px;
    padding:       10px 12px;
    display:       flex;
    align-items:   center;
    gap:           10px;
}
.hl-avatar {
    background:    #FA4B4C;
    border-radius: 50%;
    width:    32px;
    height:   32px;
    display:         flex;
    align-items:     center;
    justify-content: center;
    font-family: 'Syne', sans-serif;
    font-size:   0.9rem;
    font-weight: 700;
    color:       #fff;
    flex-shrink: 0;
}
.hl-user-name {
    font-size:   0.82rem;
    font-weight: 600;
    color:       rgba(255,255,255,0.85);
    line-height: 1.2;
}
.hl-user-email {
    font-size:     0.67rem;
    color:         rgba(255,255,255,0.28);
    overflow:      hidden;
    text-overflow: ellipsis;
    white-space:   nowrap;
    max-width:     140px;
}
</style>
"""


# Public API 
def render_sidebar() -> str:
    """
    Render the sidebar and return the key of the currently active page.

    Usage (in a Streamlit page):
        from components.sidebar import render_sidebar
        active_page = render_sidebar()
    """
    st.session_state.setdefault("active_page", "dashboard")
    active = st.session_state["active_page"]

    valid_keys = {key for key, _, _ in _NAV_ITEMS}
    if active not in valid_keys:
        st.session_state["active_page"] = "dashboard"
        active = "dashboard"

    st.markdown(_CSS, unsafe_allow_html=True)

    with st.sidebar:

        st.markdown("""
        <div class="hl-logo">
            <div>
                <div class="hl-logo-name">Hirelytics AI</div>
                <div class="hl-logo-sub">Resume Intelligence Platform</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<span class="hl-section-label">Main Menu</span>',
                    unsafe_allow_html=True)

        for key, icon, label in _NAV_ITEMS:
            btn_type = "primary" if active == key else "secondary"
            if st.button(
                f"{icon}  {label}",
                key=f"nav_{key}",
                use_container_width=True,
                type=btn_type,
            ):
                st.session_state["active_page"] = key
                st.rerun()

        st.markdown("<hr>", unsafe_allow_html=True)

        st.markdown('<span class="hl-section-label">Account</span>',
                    unsafe_allow_html=True)

        st.button("  Settings",      key="nav_settings", use_container_width=True)
        st.button("  Support Center", key="nav_support",  use_container_width=True)

        st.markdown("""
        <div class="hl-premium">
            <div class="hl-premium-dot"></div>
            <div>
                <div class="hl-premium-label">Premium Active</div>
                <div class="hl-premium-sub">Full access enabled</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height:28px'></div>", unsafe_allow_html=True)

        name    = st.session_state.get("user_name",  "User")
        email   = st.session_state.get("user_email", "")
        initial = name[0].upper() if name else "U"

        st.markdown(f"""
        <div class="hl-user-card">
            <div class="hl-avatar">{initial}</div>
            <div>
                <div class="hl-user-name">{name}</div>
                <div class="hl-user-email">{email}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="logout-marker"></div>', unsafe_allow_html=True)
        if st.button("  Log Out", key="nav_logout", use_container_width=True):
            for _k in ("jwt_token", "user_name", "user_email"):
                st.session_state[_k] = None
            st.session_state["active_page"] = "dashboard"
            st.switch_page("app.py")

    return active

"""
Hirelytics AI — Main Entry Point
Auth router: unauthenticated users see the login screen,
authenticated users are redirected straight to the dashboard.

Run the app with:
    streamlit run frontend/app.py
"""
import os
import sys

import streamlit as st

# Ensure the frontend/ directory is on the Python path so sibling
# modules (login, components, pages) are importable.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

#  Session State Defaults
for _key, _default in {
    "auth_mode":   "login",
    "jwt_token":   None,
    "user_name":   None,
    "user_email":  None,
    "active_page": "dashboard",
}.items():
    st.session_state.setdefault(_key, _default)

#  Route
if st.session_state["jwt_token"]:
   
    st.switch_page("pages/home.py")
    st.stop()

_login_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "login.py")
exec(                                                        # noqa: S102
    compile(open(_login_path, encoding="utf-8").read(), _login_path, "exec"),
    {"__file__": _login_path, "__name__": "__main__"},
)

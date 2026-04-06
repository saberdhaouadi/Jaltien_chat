import streamlit as st
import hashlib
import json
import time
import os
from datetime import datetime
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration

# ─── PAGE CONFIG ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FriendChat",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── USERS CONFIG ───────────────────────────────────────────────────────────────
# Edit usernames and passwords here before deploying
USERS = {
    "Alex":    hashlib.sha256("alex123".encode()).hexdigest(),
    "Jordan":  hashlib.sha256("jordan456".encode()).hexdigest(),
    "Morgan":  hashlib.sha256("morgan789".encode()).hexdigest(),
    "Taylor":  hashlib.sha256("taylor321".encode()).hexdigest(),
    "Riley":   hashlib.sha256("riley654".encode()).hexdigest(),
}

AVATARS = {
    "Alex":   "🦁",
    "Jordan": "🐺",
    "Morgan": "🦊",
    "Taylor": "🐻",
    "Riley":  "🦅",
}

# ─── ICE / STUN CONFIG (free public STUN servers) ───────────────────────────────
RTC_CONFIG = RTCConfiguration({
    "iceServers": [
        {"urls": ["stun:stun.l.google.com:19302"]},
        {"urls": ["stun:stun1.l.google.com:19302"]},
        {"urls": ["stun:openrelay.metered.ca:80"]},
        {
            "urls": ["turn:openrelay.metered.ca:80"],
            "username": "openrelayproject",
            "credential": "openrelayproject",
        },
    ]
})

# ─── ONLINE TRACKING (file-based so it persists across reruns) ──────────────────
ONLINE_FILE = "/tmp/friendchat_online.json"

def get_online_users():
    """Return dict of {username: last_seen_timestamp}"""
    try:
        if os.path.exists(ONLINE_FILE):
            with open(ONLINE_FILE, "r") as f:
                data = json.load(f)
            # Remove users inactive for > 30 seconds
            now = time.time()
            data = {u: t for u, t in data.items() if now - t < 30}
            return data
    except Exception:
        pass
    return {}

def heartbeat(username):
    """Update this user's last-seen time."""
    data = get_online_users()
    data[username] = time.time()
    try:
        with open(ONLINE_FILE, "w") as f:
            json.dump(data, f)
    except Exception:
        pass

def remove_user(username):
    data = get_online_users()
    data.pop(username, None)
    try:
        with open(ONLINE_FILE, "w") as f:
            json.dump(data, f)
    except Exception:
        pass

# ─── AUTH HELPERS ────────────────────────────────────────────────────────────────
def hash_pw(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def verify(username: str, password: str) -> bool:
    return USERS.get(username) == hash_pw(password)

# ─── CUSTOM CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Syne:wght@400;600;700;800&display=swap');

:root {
    --bg:       #0d0f14;
    --surface:  #161922;
    --card:     #1d2130;
    --border:   #2a2f45;
    --accent:   #5b8dee;
    --accent2:  #e85b8d;
    --green:    #3ecf8e;
    --text:     #e8eaf6;
    --muted:    #6b7194;
    --radius:   16px;
}

html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Syne', sans-serif;
}

[data-testid="stHeader"] { display: none; }
[data-testid="stSidebar"] { display: none; }

/* ── Login card ── */
.login-wrap {
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 90vh;
}
.login-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 24px;
    padding: 48px 40px;
    width: 100%;
    max-width: 420px;
    box-shadow: 0 24px 64px rgba(0,0,0,.5);
}
.login-logo {
    font-size: 52px;
    text-align: center;
    margin-bottom: 8px;
}
.login-title {
    font-size: 28px;
    font-weight: 800;
    text-align: center;
    color: var(--text);
    margin-bottom: 4px;
    letter-spacing: -0.5px;
}
.login-sub {
    font-size: 13px;
    text-align: center;
    color: var(--muted);
    margin-bottom: 32px;
    font-family: 'DM Mono', monospace;
}

/* ── Top bar ── */
.topbar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 16px 24px;
    background: var(--surface);
    border-bottom: 1px solid var(--border);
    border-radius: 0 0 var(--radius) var(--radius);
    margin-bottom: 24px;
}
.topbar-brand {
    font-size: 20px;
    font-weight: 800;
    letter-spacing: -0.3px;
}
.topbar-brand span { color: var(--accent); }
.topbar-user {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 14px;
    color: var(--muted);
    font-family: 'DM Mono', monospace;
}
.topbar-avatar {
    font-size: 22px;
    width: 38px;
    height: 38px;
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
}

/* ── Friend pills ── */
.friends-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    margin-bottom: 24px;
}
.friend-pill {
    display: flex;
    align-items: center;
    gap: 8px;
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 50px;
    padding: 6px 14px 6px 8px;
    font-size: 13px;
    font-family: 'DM Mono', monospace;
}
.friend-pill .dot {
    width: 8px; height: 8px;
    border-radius: 50%;
    background: var(--muted);
}
.friend-pill .dot.online { background: var(--green); box-shadow: 0 0 6px var(--green); }
.friend-pill .emo { font-size: 18px; }

/* ── Section labels ── */
.section-label {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--muted);
    font-family: 'DM Mono', monospace;
    margin-bottom: 12px;
}

/* ── Video card ── */
.video-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 20px;
    margin-bottom: 20px;
}

/* ── Info banner ── */
.info-banner {
    background: linear-gradient(135deg, #1a2040, #1d2130);
    border: 1px solid var(--accent);
    border-radius: var(--radius);
    padding: 16px 20px;
    font-size: 13px;
    color: var(--muted);
    font-family: 'DM Mono', monospace;
    margin-bottom: 20px;
    line-height: 1.7;
}
.info-banner strong { color: var(--accent); }

/* ── Streamlit widget overrides ── */
.stSelectbox label, .stTextInput label, .stButton label {
    color: var(--muted) !important;
    font-size: 12px !important;
    font-family: 'DM Mono', monospace !important;
    text-transform: uppercase;
    letter-spacing: 1px;
}
.stTextInput > div > div > input {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-family: 'DM Mono', monospace !important;
}
.stTextInput > div > div > input:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(91,141,238,.2) !important;
}
.stSelectbox > div > div {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
}
div[data-testid="stButton"] > button {
    background: var(--accent) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 15px !important;
    padding: 10px 28px !important;
    width: 100%;
    transition: opacity .2s;
}
div[data-testid="stButton"] > button:hover { opacity: 0.85 !important; }

/* ── Error / success ── */
.stAlert { border-radius: 10px !important; font-family: 'DM Mono', monospace !important; }

/* ── Video stream container ── */
.stVideo, video { border-radius: 12px !important; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: var(--card) !important;
    border-radius: 12px !important;
    padding: 4px !important;
    gap: 4px !important;
    border: 1px solid var(--border) !important;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px !important;
    color: var(--muted) !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
}
.stTabs [aria-selected="true"] {
    background: var(--accent) !important;
    color: white !important;
}

/* ── Logout button special style ── */
.logout-btn div[data-testid="stButton"] > button {
    background: transparent !important;
    border: 1px solid var(--border) !important;
    color: var(--muted) !important;
    font-size: 12px !important;
    padding: 6px 14px !important;
    width: auto !important;
}
</style>
""", unsafe_allow_html=True)

# ─── SESSION STATE INIT ──────────────────────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "login_error" not in st.session_state:
    st.session_state.login_error = ""

# ─── LOGIN PAGE ──────────────────────────────────────────────────────────────────
if not st.session_state.logged_in:
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        st.markdown('<div class="login-logo">🎙️</div>', unsafe_allow_html=True)
        st.markdown('<div class="login-title">FriendChat</div>', unsafe_allow_html=True)
        st.markdown('<div class="login-sub">private video & voice for 5 friends</div>', unsafe_allow_html=True)

        username = st.selectbox(
            "Your name",
            options=[""] + list(USERS.keys()),
            format_func=lambda x: f"{AVATARS.get(x, '')} {x}" if x else "— pick your name —",
        )
        password = st.text_input("Password", type="password", placeholder="••••••••")

        if st.session_state.login_error:
            st.error(st.session_state.login_error)

        if st.button("Sign in →"):
            if not username:
                st.session_state.login_error = "Please select your name."
            elif not password:
                st.session_state.login_error = "Please enter your password."
            elif not verify(username, password):
                st.session_state.login_error = "Wrong password. Try again."
            else:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.login_error = ""
                heartbeat(username)
                st.rerun()

    st.stop()

# ─── MAIN APP (authenticated) ─────────────────────────────────────────────────────
username = st.session_state.username
avatar = AVATARS.get(username, "👤")
heartbeat(username)
online = get_online_users()

# Top bar
st.markdown(f"""
<div class="topbar">
  <div class="topbar-brand">Friend<span>Chat</span> 🎙️</div>
  <div class="topbar-user">
    <span>{username}</span>
    <div class="topbar-avatar">{avatar}</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Friends online status ────────────────────────────────────────────────────────
st.markdown('<div class="section-label">Who\'s online</div>', unsafe_allow_html=True)
pills_html = '<div class="friends-grid">'
for name, emo in AVATARS.items():
    is_online = name in online
    dot_class = "dot online" if is_online else "dot"
    status = "online" if is_online else "offline"
    pills_html += f'<div class="friend-pill"><span class="emo">{emo}</span><div class="{dot_class}"></div>{name}<span style="color:var(--muted);font-size:11px;margin-left:2px">{status}</span></div>'
pills_html += "</div>"
st.markdown(pills_html, unsafe_allow_html=True)

# ── Info banner ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="info-banner">
  <strong>How it works:</strong> Click <strong>START</strong> below to share your camera & mic.
  All 5 friends connect to the same room — everyone who clicks Start can see and hear each other.
  Make sure your browser grants camera/microphone permissions when asked.
</div>
""", unsafe_allow_html=True)

# ── Tabs ─────────────────────────────────────────────────────────────────────────
tab_video, tab_voice = st.tabs(["📹  Video + Voice", "🎙️  Voice Only"])

with tab_video:
    st.markdown('<div class="video-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Video & Voice room</div>', unsafe_allow_html=True)
    st.markdown(
        "Click **START** — your browser will ask for camera & microphone access. "
        "Once connected, friends who also click Start will appear in the room.",
        unsafe_allow_html=False,
    )

    webrtc_streamer(
        key="friendchat-video",
        mode=WebRtcMode.SENDRECV,
        rtc_configuration=RTC_CONFIG,
        media_stream_constraints={
            "video": {
                "width":  {"ideal": 640, "max": 1280},
                "height": {"ideal": 480, "max": 720},
                "frameRate": {"ideal": 24, "max": 30},
            },
            "audio": True,
        },
        video_html_attrs={
            "style": "width:100%; border-radius:12px; background:#0d0f14;",
            "controls": False,
            "autoPlay": True,
            "muted": True,   # mute local preview to avoid echo
        },
        async_processing=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

with tab_voice:
    st.markdown('<div class="video-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Voice-only room</div>', unsafe_allow_html=True)
    st.markdown(
        "Same room, but **no camera**. Perfect when you want to save bandwidth "
        "or just have a conversation.",
        unsafe_allow_html=False,
    )

    webrtc_streamer(
        key="friendchat-voice",
        mode=WebRtcMode.SENDRECV,
        rtc_configuration=RTC_CONFIG,
        media_stream_constraints={
            "video": False,
            "audio": True,
        },
        async_processing=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

# ── Logout ───────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown('<div class="logout-btn">', unsafe_allow_html=True)
col_a, col_b, col_c = st.columns([4, 1, 4])
with col_b:
    if st.button("Sign out"):
        remove_user(username)
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()
st.markdown("</div>", unsafe_allow_html=True)

# ── Auto-refresh for online status ──────────────────────────────────────────────
time.sleep(0.1)
st.markdown(
    """<script>
    setTimeout(function(){ window.location.reload(); }, 15000);
    </script>""",
    unsafe_allow_html=True,
)

import streamlit as st
import hashlib
import json
import streamlit.components.v1 as components

st.set_page_config(page_title="FriendChat", page_icon="🎙️", layout="wide", initial_sidebar_state="collapsed")

# ─── USERS CONFIG ───────────────────────────────────────────────────────────────
# Change names and passwords before deploying!
USERS = {
    "Alex":   hashlib.sha256("alex123".encode()).hexdigest(),
    "Jordan": hashlib.sha256("jordan456".encode()).hexdigest(),
    "Morgan": hashlib.sha256("morgan789".encode()).hexdigest(),
    "Taylor": hashlib.sha256("taylor321".encode()).hexdigest(),
    "Riley":  hashlib.sha256("riley654".encode()).hexdigest(),
}
AVATARS = {"Alex":"🦁","Jordan":"🐺","Morgan":"🦊","Taylor":"🐻","Riley":"🦅"}
COLORS  = {"Alex":"#5b8dee","Jordan":"#e85b8d","Morgan":"#3ecf8e","Taylor":"#f5a623","Riley":"#b45bee"}

# ─── DAILY.CO ROOM URL ──────────────────────────────────────────────────────────
# 1. Go to https://dashboard.daily.co  (free account)
# 2. Create a room (e.g. "friendchat-room"), set it to public
# 3. Paste the room URL below
DAILY_ROOM_URL = "https://your-domain.daily.co/friendchat-room"

def verify(username, password):
    return USERS.get(username) == hashlib.sha256(password.encode()).hexdigest()

for k, v in [("logged_in", False), ("username", ""), ("login_error", "")]:
    if k not in st.session_state:
        st.session_state[k] = v

# ─── CSS ─────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Syne:wght@700;800&display=swap');
:root{--bg:#0d0f14;--surface:#161922;--card:#1d2130;--border:#2a2f45;--accent:#5b8dee;--text:#e8eaf6;--muted:#6b7194;}
html,body,[data-testid="stAppViewContainer"]{background:var(--bg)!important;color:var(--text)!important;font-family:'Syne',sans-serif;}
[data-testid="stHeader"],[data-testid="stSidebar"],[data-testid="stBottom"]{display:none!important;}
.stTextInput>div>div>input{background:var(--card)!important;border:1px solid var(--border)!important;border-radius:10px!important;color:var(--text)!important;font-family:'DM Mono',monospace!important;}
.stTextInput>div>div>input:focus{border-color:var(--accent)!important;box-shadow:0 0 0 2px rgba(91,141,238,.2)!important;}
.stSelectbox label,.stTextInput label{color:var(--muted)!important;font-size:11px!important;font-family:'DM Mono',monospace!important;text-transform:uppercase;letter-spacing:1px;}
.stSelectbox>div>div{background:var(--card)!important;border:1px solid var(--border)!important;border-radius:10px!important;color:var(--text)!important;}
div[data-testid="stButton"]>button{background:var(--accent)!important;color:#fff!important;border:none!important;border-radius:10px!important;font-family:'Syne',sans-serif!important;font-weight:700!important;font-size:15px!important;padding:10px 28px!important;width:100%;transition:opacity .2s;}
div[data-testid="stButton"]>button:hover{opacity:.85!important;}
iframe{border:none!important;}
</style>
""", unsafe_allow_html=True)

# ════════════════ LOGIN ══════════════════════════════════════════════════════════
if not st.session_state.logged_in:
    c1, c2, c3 = st.columns([1,1.1,1])
    with c2:
        st.markdown("""
        <div style="text-align:center;padding:40px 0 8px">
          <div style="font-size:54px">🎙️</div>
          <div style="font-size:30px;font-weight:800;letter-spacing:-0.5px">FriendChat</div>
          <div style="font-size:13px;color:#6b7194;font-family:'DM Mono',monospace;margin-bottom:28px">
            private video &amp; voice · up to 5 friends
          </div>
        </div>""", unsafe_allow_html=True)
        username = st.selectbox("Your name", [""] + list(USERS.keys()),
                                format_func=lambda x: f"{AVATARS.get(x,'')} {x}" if x else "— pick your name —")
        password = st.text_input("Password", type="password", placeholder="••••••••")
        if st.session_state.login_error:
            st.error(st.session_state.login_error)
        if st.button("Sign in →"):
            if not username:   st.session_state.login_error = "Please select your name."
            elif not password: st.session_state.login_error = "Please enter your password."
            elif not verify(username, password): st.session_state.login_error = "Wrong password."
            else:
                st.session_state.logged_in = True
                st.session_state.username  = username
                st.session_state.login_error = ""
                st.rerun()
    st.stop()

# ════════════════ MAIN APP ═══════════════════════════════════════════════════════
ME     = st.session_state.username
avatar = AVATARS.get(ME, "👤")
color  = COLORS.get(ME, "#5b8dee")

# Top bar
st.markdown(f"""
<div style="display:flex;align-items:center;justify-content:space-between;padding:14px 24px;
  background:#161922;border-bottom:1px solid #2a2f45;border-radius:0 0 16px 16px;margin-bottom:20px">
  <div style="font-size:20px;font-weight:800">Friend<span style="color:#5b8dee">Chat</span> 🎙️</div>
  <div style="display:flex;align-items:center;gap:10px;font-size:13px;color:#6b7194;font-family:'DM Mono',monospace">
    <span>{ME}</span>
    <div style="font-size:22px;width:38px;height:38px;background:#1d2130;border:1px solid #2a2f45;
      border-radius:50%;display:flex;align-items:center;justify-content:center">{avatar}</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Daily.co embed — the only reliable cross-browser WebRTC in an iframe ─────────
# Daily handles camera, mic, audio routing, echo cancellation, TURN servers, all of it.
DAILY_HTML = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ background:#0d0f14; font-family:'Segoe UI',sans-serif; overflow:hidden; }}
  #frame {{ width:100vw; height:100vh; border:none; display:block; }}
  #splash {{
    position:fixed; inset:0; background:#0d0f14;
    display:flex; flex-direction:column; align-items:center; justify-content:center; gap:20px;
  }}
  #splash p {{
    color:#6b7194; font-size:13px; font-family:monospace; text-align:center; line-height:1.7;
    max-width:340px;
  }}
  #joinBtn {{
    background:#5b8dee; color:#fff; border:none; border-radius:12px;
    padding:13px 32px; font-size:15px; font-weight:700; cursor:pointer;
    font-family:inherit; transition:opacity .2s;
  }}
  #joinBtn:hover {{ opacity:.85; }}
  .name-badge {{
    background:#1d2130; border:1px solid #2a2f45; border-radius:50px;
    padding:6px 16px; font-size:13px; font-family:monospace; color:#e8eaf6;
    display:flex; align-items:center; gap:8px;
  }}
  .dot {{ width:8px; height:8px; background:#3ecf8e; border-radius:50%; box-shadow:0 0 6px #3ecf8e; }}
</style>
<script src="https://unpkg.com/@daily-co/daily-js"></script>
</head>
<body>

<div id="splash">
  <div style="font-size:48px">🎙️</div>
  <div class="name-badge">
    <div class="dot"></div>
    <span>{avatar} {ME}</span>
  </div>
  <p>
    Click <strong style="color:#e8eaf6">Join Call</strong> to enter the video room.<br>
    Your browser will ask for camera &amp; microphone — please allow both.
  </p>
  <button id="joinBtn">📹 Join Call</button>
  <p style="font-size:11px;color:#3a3f58">
    Friends using the same app will appear automatically once they also join.
  </p>
</div>

<iframe id="frame" style="display:none" allow="camera; microphone; autoplay; display-capture; speaker-selection; clipboard-write"></iframe>

<script>
  document.getElementById("joinBtn").onclick = function() {{
    const roomUrl = "{DAILY_ROOM_URL}";
    
    // Check if Daily.co room URL is configured
    if (roomUrl.includes("your-domain")) {{
      document.getElementById("splash").innerHTML = `
        <div style="color:#e85b8d;font-size:14px;font-family:monospace;text-align:center;padding:20px;max-width:400px;line-height:1.8">
          ⚠️ <strong style="color:#e8eaf6">Room not configured yet!</strong><br><br>
          1. Go to <a href="https://dashboard.daily.co" target="_blank" style="color:#5b8dee">dashboard.daily.co</a> (free)<br>
          2. Create a room named <code style="background:#1d2130;padding:2px 6px;border-radius:4px">friendchat-room</code><br>
          3. Copy the room URL and paste it into <code style="background:#1d2130;padding:2px 6px;border-radius:4px">DAILY_ROOM_URL</code> in app.py<br>
          4. Redeploy the app
        </div>`;
      return;
    }}

    // Use Daily.co's embedded call UI — handles everything (video, audio, echo cancellation)
    const callFrame = window.DailyIframe.createFrame(
      document.getElementById("frame"),
      {{
        iframeStyle: {{
          width: "100%",
          height: "100%",
          border: "none",
        }},
        showLeaveButton: true,
        showFullscreenButton: true,
      }}
    );

    callFrame
      .join({{
        url: roomUrl,
        userName: "{ME} {avatar}",
        startVideoOff: false,
        startAudioOff: false,
      }})
      .then(() => {{
        document.getElementById("splash").style.display = "none";
        document.getElementById("frame").style.display  = "block";
      }})
      .catch(err => {{
        document.getElementById("splash").innerHTML += 
          `<p style="color:#e85b8d">Error joining: ${{err.message}}</p>`;
      }});

    callFrame.on("left-meeting", () => {{
      document.getElementById("frame").style.display  = "none";
      document.getElementById("splash").style.display = "flex";
    }});
  }};
</script>
</body>
</html>
"""

components.html(DAILY_HTML, height=620, scrolling=False)

# Logout
st.markdown("---")
ca, cb, cc = st.columns([4,1,4])
with cb:
    st.markdown("""<style>
    div[data-testid='stButton']>button{
      background:#1d2130!important;border:1px solid #2a2f45!important;
      color:#6b7194!important;font-size:12px!important;
      width:auto!important;padding:6px 18px!important;
    }</style>""", unsafe_allow_html=True)
    if st.button("Sign out"):
        st.session_state.logged_in = False
        st.session_state.username  = ""
        st.rerun()

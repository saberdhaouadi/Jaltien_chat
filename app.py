import streamlit as st
import hashlib
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

# ─── ROOM NAME ──────────────────────────────────────────────────────────────────
# This is your private room. Change it to something unique so strangers can't guess it.
# Only people who know this name AND have your app password can join.
ROOM_NAME = "FriendChat-MyPrivateRoom-2026-XK9"

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
iframe{border:none!important;border-radius:16px!important;}
</style>
""", unsafe_allow_html=True)

# ════════════════ LOGIN ══════════════════════════════════════════════════════════
if not st.session_state.logged_in:
    c1, c2, c3 = st.columns([1, 1.1, 1])
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

# ── Jitsi Meet embed ─────────────────────────────────────────────────────────────
# Jitsi is 100% free, open-source, no account needed, handles all WebRTC properly.
# The External API gives full control: display name, avatar color, start muted, etc.

JITSI_HTML = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ background:#0d0f14; overflow:hidden; font-family:'Segoe UI',sans-serif; }}

  #splash {{
    position:fixed; inset:0; background:#0d0f14;
    display:flex; flex-direction:column; align-items:center; justify-content:center; gap:16px;
  }}
  .badge {{
    background:#1d2130; border:1px solid #2a2f45; border-radius:50px;
    padding:7px 18px; font-size:13px; font-family:monospace; color:#e8eaf6;
    display:flex; align-items:center; gap:8px;
  }}
  .live-dot {{ width:8px;height:8px;background:#3ecf8e;border-radius:50%;box-shadow:0 0 6px #3ecf8e; }}
  #joinBtn {{
    background:{color}; color:#fff; border:none; border-radius:12px;
    padding:13px 36px; font-size:15px; font-weight:700; cursor:pointer;
    font-family:inherit; letter-spacing:0.3px; transition:opacity .2s;
  }}
  #joinBtn:hover {{ opacity:.85; }}
  .hint {{ color:#3a3f58; font-size:12px; font-family:monospace; text-align:center; line-height:1.8; }}
  #meet {{ position:fixed; inset:0; display:none; }}
</style>
<script src="https://meet.jit.si/external_api.js"></script>
</head>
<body>

<div id="splash">
  <div style="font-size:46px">{avatar}</div>
  <div style="font-size:22px;font-weight:800;color:#e8eaf6">{ME}</div>
  <div class="badge"><div class="live-dot"></div><span>Room ready · {ROOM_NAME[:24]}…</span></div>
  <button id="joinBtn">📹 Join Call</button>
  <div class="hint">
    Your browser will ask for camera &amp; microphone access — allow both.<br>
    All 5 friends join the same private room automatically.
  </div>
</div>

<div id="meet"></div>

<script>
window.addEventListener("load", function() {{
  document.getElementById("joinBtn").addEventListener("click", function() {{
    document.getElementById("splash").style.display = "none";
    document.getElementById("meet").style.display   = "block";

    const api = new JitsiMeetExternalAPI("meet.jit.si", {{
      roomName: "{ROOM_NAME}",
      parentNode: document.getElementById("meet"),
      displayName: "{ME} {avatar}",
      userInfo: {{
        displayName: "{ME} {avatar}",
      }},
      configOverwrite: {{
        startWithAudioMuted:    false,
        startWithVideoMuted:    false,
        prejoinPageEnabled:     false,
        disableDeepLinking:     true,
        enableWelcomePage:      false,
        disableInviteFunctions: true,
        toolbarButtons: [
          "microphone", "camera", "desktop", "fullscreen",
          "fodeviceselection", "hangup", "chat",
          "tileview", "select-background", "toggle-camera",
        ],
      }},
      interfaceConfigOverwrite: {{
        SHOW_JITSI_WATERMARK:       false,
        SHOW_WATERMARK_FOR_GUESTS:  false,
        SHOW_BRAND_WATERMARK:       false,
        SHOW_POWERED_BY:            false,
        DISPLAY_WELCOME_PAGE_CONTENT: false,
        HIDE_INVITE_MORE_HEADER:    true,
        MOBILE_APP_PROMO:           false,
        APP_NAME:                   "FriendChat",
        NATIVE_APP_NAME:            "FriendChat",
        TOOLBAR_ALWAYS_VISIBLE:     false,
      }},
    }});

    api.addEventListener("readyToClose", function() {{
      api.dispose();
      document.getElementById("meet").style.display   = "none";
      document.getElementById("splash").style.display = "flex";
    }});
  }});
}});
</script>
</body>
</html>"""

components.html(JITSI_HTML, height=650, scrolling=False)

# Logout
st.markdown("---")
ca, cb, cc = st.columns([4, 1, 4])
with cb:
    st.markdown("""<style>
    div[data-testid='stButton']>button{{
      background:#1d2130!important;border:1px solid #2a2f45!important;
      color:#6b7194!important;font-size:12px!important;
      width:auto!important;padding:6px 18px!important;
    }}</style>""", unsafe_allow_html=True)
    if st.button("Sign out"):
        st.session_state.logged_in = False
        st.session_state.username  = ""
        st.rerun()

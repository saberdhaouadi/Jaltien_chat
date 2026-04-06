import streamlit as st
import hashlib
import json
import streamlit.components.v1 as components

# ─── PAGE CONFIG ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="FriendChat",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── USERS CONFIG ───────────────────────────────────────────────────────────────
USERS = {
    "Alex":   hashlib.sha256("alex123".encode()).hexdigest(),
    "Jordan": hashlib.sha256("jordan456".encode()).hexdigest(),
    "Morgan": hashlib.sha256("morgan789".encode()).hexdigest(),
    "Taylor": hashlib.sha256("taylor321".encode()).hexdigest(),
    "Riley":  hashlib.sha256("riley654".encode()).hexdigest(),
}
AVATARS = {"Alex":"🦁","Jordan":"🐺","Morgan":"🦊","Taylor":"🐻","Riley":"🦅"}
COLORS  = {"Alex":"#5b8dee","Jordan":"#e85b8d","Morgan":"#3ecf8e","Taylor":"#f5a623","Riley":"#b45bee"}

def verify(username, password):
    return USERS.get(username) == hashlib.sha256(password.encode()).hexdigest()

# ─── SESSION STATE ───────────────────────────────────────────────────────────────
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

# ════════════════════════════════════════════════════════════════════════════════
# LOGIN
# ════════════════════════════════════════════════════════════════════════════════
if not st.session_state.logged_in:
    c1, c2, c3 = st.columns([1,1.1,1])
    with c2:
        st.markdown("""
        <div style="text-align:center;padding:40px 0 8px">
          <div style="font-size:54px">🎙️</div>
          <div style="font-size:30px;font-weight:800;letter-spacing:-0.5px">FriendChat</div>
          <div style="font-size:13px;color:#6b7194;font-family:'DM Mono',monospace;margin-bottom:28px">private video &amp; voice · up to 5 friends</div>
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

# ════════════════════════════════════════════════════════════════════════════════
# MAIN APP
# ════════════════════════════════════════════════════════════════════════════════
ME     = st.session_state.username
avatar = AVATARS.get(ME, "👤")
color  = COLORS.get(ME, "#5b8dee")
users_json = json.dumps([{"name": n, "avatar": a, "color": COLORS.get(n,"#5b8dee")} for n, a in AVATARS.items()])

st.markdown(f"""
<div style="display:flex;align-items:center;justify-content:space-between;padding:14px 24px;
            background:#161922;border-bottom:1px solid #2a2f45;border-radius:0 0 16px 16px;margin-bottom:20px">
  <div style="font-size:20px;font-weight:800">Friend<span style="color:#5b8dee">Chat</span> 🎙️</div>
  <div style="display:flex;align-items:center;gap:10px;font-size:13px;color:#6b7194;font-family:'DM Mono',monospace">
    <span>{ME}</span>
    <div style="font-size:20px;width:36px;height:36px;background:#1d2130;border:1px solid #2a2f45;
                border-radius:50%;display:flex;align-items:center;justify-content:center">{avatar}</div>
  </div>
</div>""", unsafe_allow_html=True)

# Build friend pills HTML
pills = "".join(
    f'<div class="fpill" id="pill-{u["name"]}">'
    f'<span>{u["avatar"]}</span><div class="fdot"></div><span>{u["name"]}</span></div>'
    for u in json.loads(users_json)
)

HTML = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:#0d0f14;font-family:'Segoe UI',sans-serif;color:#e8eaf6;padding:16px;}}
#status{{font-size:12px;font-family:monospace;color:#6b7194;margin-bottom:14px;padding:10px 14px;
         background:#1d2130;border-radius:10px;border-left:3px solid #5b8dee;line-height:1.5}}
#controls{{display:flex;gap:10px;margin-bottom:16px;flex-wrap:wrap}}
button{{border:none;border-radius:10px;padding:9px 18px;font-size:13px;font-weight:700;cursor:pointer;transition:opacity .2s;font-family:inherit}}
button:hover{{opacity:.85}}
#btnJoin{{background:#5b8dee;color:#fff}}
#btnLeave,#btnMute,#btnCam{{background:#2a2f45;color:#e8eaf6;display:none}}
#videos{{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:12px}}
.vid-tile{{position:relative;background:#161922;border:1px solid #2a2f45;border-radius:14px;overflow:hidden;aspect-ratio:4/3}}
.vid-tile video{{width:100%;height:100%;object-fit:cover;display:block}}
.vid-label{{position:absolute;bottom:8px;left:8px;background:rgba(0,0,0,.6);border-radius:20px;
            padding:3px 10px 3px 6px;font-size:12px;display:flex;align-items:center;gap:5px;backdrop-filter:blur(4px)}}
.dot{{width:7px;height:7px;background:#3ecf8e;border-radius:50%;box-shadow:0 0 5px #3ecf8e}}
#friends-bar{{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:14px}}
.fpill{{display:flex;align-items:center;gap:6px;background:#1d2130;border:1px solid #2a2f45;
        border-radius:50px;padding:4px 12px 4px 8px;font-size:12px;font-family:monospace;transition:border-color .3s}}
.fpill.online{{border-color:#3ecf8e}}
.fdot{{width:7px;height:7px;border-radius:50%;background:#3a3f58;transition:background .3s,box-shadow .3s}}
.fpill.online .fdot{{background:#3ecf8e;box-shadow:0 0 5px #3ecf8e}}
</style>
<script src="https://unpkg.com/peerjs@1.5.4/dist/peerjs.min.js"></script>
</head><body>
<div id="friends-bar">{pills}</div>
<div id="status">Click <b>Join Call</b> to share your camera &amp; microphone with friends.</div>
<div id="controls">
  <button id="btnJoin">📹 Join Call</button>
  <button id="btnLeave">📴 Leave</button>
  <button id="btnMute">🎙️ Mute</button>
  <button id="btnCam">📷 Hide Cam</button>
</div>
<div id="videos"></div>
<script>
const ME={json.dumps(ME)};
const USERS={users_json};
const ROOM="friendchat-v1-2026";
const myId=ROOM+"-"+ME;
const OTHERS=USERS.map(u=>u.name).filter(n=>n!==ME);
let peer=null,myStream=null,calls={{}},muted=false,camOff=false;

function info(n){{return USERS.find(u=>u.name===n)||{{name:n,avatar:"👤",color:"#5b8dee"}}}}
function setStatus(m){{document.getElementById("status").innerHTML=m}}
function pillOnline(n,on){{const p=document.getElementById("pill-"+n);if(!p)return;on?p.classList.add("online"):p.classList.remove("online")}}

function addLocal(stream){{
  let t=document.getElementById("tile-local");
  if(!t){{
    t=document.createElement("div");t.className="vid-tile";t.id="tile-local";
    t.innerHTML=`<video id="vid-local" autoplay muted playsinline></video>
    <div class="vid-label"><div class="dot"></div><span>${{info(ME).avatar}} ${{ME}} (you)</span></div>`;
    document.getElementById("videos").prepend(t);
  }}
  document.getElementById("vid-local").srcObject=stream;
}}

function addRemote(name,stream){{
  // ── Video tile ──
  let t=document.getElementById("tile-"+name);
  if(!t){{
    t=document.createElement("div");t.className="vid-tile";t.id="tile-"+name;
    t.innerHTML=`<video id="vid-${{name}}" autoplay playsinline></video>
    <div class="vid-label"><div class="dot"></div><span>${{info(name).avatar}} ${{name}}</span></div>`;
    document.getElementById("videos").appendChild(t);
  }}
  const vid=document.getElementById("vid-"+name);
  vid.srcObject=stream;
  vid.muted=true; // mute video element to prevent echo/double audio

  // ── Dedicated <audio> element — this is what plays the voice ──
  let aud=document.getElementById("aud-"+name);
  if(!aud){{
    aud=document.createElement("audio");
    aud.id="aud-"+name;
    aud.autoplay=true;
    aud.muted=false;
    aud.volume=1.0;
    document.body.appendChild(aud);
  }}
  aud.srcObject=stream;
  // Force play — required in some browsers inside iframes
  aud.play().catch(()=>{{
    document.addEventListener("click",()=>aud.play(),{{once:true}});
  }});

  pillOnline(name,true);
}}

function removeTile(name){{
  const t=document.getElementById("tile-"+name);if(t)t.remove();
  const a=document.getElementById("aud-"+name);if(a)a.remove();
  pillOnline(name,false);delete calls[name];
}}

function handleCall(call){{
  const caller=call.peer.replace(ROOM+"-","");
  call.answer(myStream);
  call.on("stream",s=>addRemote(caller,s));
  call.on("close",()=>removeTile(caller));
  call.on("error",()=>removeTile(caller));
  calls[caller]=call;
}}

function callPeer(name){{
  if(calls[name])return;
  const c=peer.call(ROOM+"-"+name,myStream);if(!c)return;
  c.on("stream",s=>addRemote(name,s));
  c.on("close",()=>removeTile(name));
  c.on("error",()=>removeTile(name));
  calls[name]=c;
}}

document.getElementById("btnJoin").onclick=async()=>{{
  setStatus("🎤 Requesting camera &amp; microphone…");
  try{{myStream=await navigator.mediaDevices.getUserMedia({{video:true,audio:true}})}}
  catch(e){{setStatus("❌ Camera/mic blocked. Please allow access and reload the page.");return}}
  addLocal(myStream);pillOnline(ME,true);
  peer=new Peer(myId,{{
    host:"0.peerjs.com",port:443,path:"/",secure:true,
    config:{{iceServers:[
      {{urls:"stun:stun.l.google.com:19302"}},
      {{urls:"stun:stun1.l.google.com:19302"}},
      {{urls:"turn:openrelay.metered.ca:80",username:"openrelayproject",credential:"openrelayproject"}}
    ]}}
  }});
  peer.on("open",()=>{{
    setStatus("✅ Connected as <b>"+ME+"</b>. Calling friends… <span style='color:#f5a623'>🔊 If you can\'t hear audio, click anywhere on the page to unlock sound.</span>");
    ["btnJoin","btnLeave","btnMute","btnCam"].forEach((id,i)=>
      document.getElementById(id).style.display=i===0?"none":"");
    OTHERS.forEach(callPeer);
    setInterval(()=>OTHERS.forEach(callPeer),4000);
  }});
  peer.on("call",handleCall);
  peer.on("error",e=>{{if(e.type==="peer-unavailable")return;setStatus("⚠️ "+e.message)}});
}};

document.getElementById("btnLeave").onclick=()=>{{
  Object.values(calls).forEach(c=>c.close());
  if(peer)peer.destroy();
  if(myStream)myStream.getTracks().forEach(t=>t.stop());
  document.getElementById("videos").innerHTML="";
  // Remove all audio elements
  USERS.forEach(u=>{{const a=document.getElementById("aud-"+u.name);if(a)a.remove();}});
  calls={{}};peer=null;myStream=null;
  USERS.forEach(u=>pillOnline(u.name,false));
  ["btnJoin","btnLeave","btnMute","btnCam"].forEach((id,i)=>
    document.getElementById(id).style.display=i===0?"":"none");
  setStatus("You left. Click <b>Join Call</b> to reconnect.");
}};

document.getElementById("btnMute").onclick=()=>{{
  if(!myStream)return;muted=!muted;
  myStream.getAudioTracks().forEach(t=>t.enabled=!muted);
  document.getElementById("btnMute").textContent=muted?"🔇 Unmute":"🎙️ Mute";
}};
document.getElementById("btnCam").onclick=()=>{{
  if(!myStream)return;camOff=!camOff;
  myStream.getVideoTracks().forEach(t=>t.enabled=!camOff);
  document.getElementById("btnCam").textContent=camOff?"📷 Show Cam":"📷 Hide Cam";
}};
</script></body></html>"""

components.html(HTML, height=700, scrolling=True)

st.markdown("---")
ca, cb, cc = st.columns([4,1,4])
with cb:
    st.markdown("<style>div[data-testid='stButton']>button{background:#1d2130!important;border:1px solid #2a2f45!important;color:#6b7194!important;font-size:12px!important;width:auto!important;padding:6px 18px!important;}</style>", unsafe_allow_html=True)
    if st.button("Sign out"):
        st.session_state.logged_in = False
        st.session_state.username  = ""
        st.rerun()

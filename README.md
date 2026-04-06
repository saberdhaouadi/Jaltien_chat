# 🎙️ FriendChat — Private Video & Voice for 5 Friends

A **Streamlit** app for private video/voice chat between up to 5 friends.  
Each friend has their own username + password. All powered by **WebRTC** (peer-to-peer).

---

## 📁 Files

```
friendchat/
├── app.py            ← Main Streamlit application
├── requirements.txt  ← Python dependencies
└── README.md         ← This file
```

---

## 🔑 Customizing Usernames & Passwords

Open `app.py` and find the `USERS` dictionary near the top:

```python
import hashlib

USERS = {
    "Alex":    hashlib.sha256("alex123".encode()).hexdigest(),
    "Jordan":  hashlib.sha256("jordan456".encode()).hexdigest(),
    "Morgan":  hashlib.sha256("morgan789".encode()).hexdigest(),
    "Taylor":  hashlib.sha256("taylor321".encode()).hexdigest(),
    "Riley":   hashlib.sha256("riley654".encode()).hexdigest(),
}
```

**To change a password**, replace the string inside `sha256("YOUR_PASSWORD".encode())`.  
**To change a name**, edit the key (e.g., `"Alex"` → `"Sara"`).

Also update the `AVATARS` dict to match:

```python
AVATARS = {
    "Alex":   "🦁",
    "Jordan": "🐺",
    "Morgan": "🦊",
    "Taylor": "🐻",
    "Riley":  "🦅",
}
```

---

## 🚀 Running Locally

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the app
streamlit run app.py
```

The app opens at **http://localhost:8501**

---

## ☁️ Deploying to Streamlit Cloud (Free)

1. Push this folder to a **GitHub repository**
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**
3. Select your repo → set **Main file path** to `app.py`
4. Click **Deploy** — done! ✅

Your friends access it at the URL Streamlit gives you (e.g. `https://yourapp.streamlit.app`).

> **Note:** Streamlit Cloud is free for public repos. For a private repo you need a paid plan.  
> Alternatively, deploy to **Railway**, **Render**, or any VPS with Docker.

---

## 🎥 How Video/Voice Works

- Uses **WebRTC** (the same tech as Google Meet, Discord) via `streamlit-webrtc`
- **Peer-to-peer** — video goes directly between browsers (low latency)
- **STUN/TURN** servers help friends behind firewalls connect (free public servers used)
- Click **START** in the app → browser asks for camera/mic permission → you're live

---

## 🔒 Security Notes

- Passwords are stored as **SHA-256 hashes** (not plaintext)
- For production, consider moving passwords to **Streamlit Secrets** (`st.secrets`)
- The app has **no database** — all state is in-memory / temp files

### Using Streamlit Secrets (recommended for deployment)

In `app.py` replace the `USERS` dict with:

```python
import streamlit as st
USERS = st.secrets["users"]  # dict of name → hashed_password
```

Then create `.streamlit/secrets.toml`:

```toml
[users]
Alex   = "sha256_hash_here"
Jordan = "sha256_hash_here"
```

---

## 🛠️ Troubleshooting

| Problem | Fix |
|---|---|
| Camera/mic not working | Allow browser permissions; use HTTPS (required for WebRTC) |
| Can't see friends | Everyone must click START; check firewall/corporate network |
| Connection fails | Try a different network; the free TURN server may be throttled |
| App won't start | Run `pip install -r requirements.txt` again |

---

Built with ❤️ using Streamlit + streamlit-webrtc# Jaltien_chat

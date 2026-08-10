import os, re, urllib.parse, urllib.request
from flask import (
    Flask,
    abort,
    jsonify,
    render_template,
    request
)

app = Flask(__name__)

def get_vid(q):
    try:
        enc = urllib.parse.quote(q)
        url = f"https://www.youtube.com/results?search_query={enc}"
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        data = urllib.request.urlopen(req, timeout=5).read().decode()
        ids = re.findall(r"\"videoId\":\"([^\"]+)\"", data)
        return ids[0] if ids else None
    except Exception:
        return None

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/agent", methods=["POST"])
def ai_agent_router():
    d = request.get_json(silent=True)
    if not d or "command" not in d:
        # Fallback if frontend sends text_command instead
        cmd_text = d.get("text_command") if d else None
        if not cmd_text:
            abort(400)
        cmd = cmd_text.strip().lower()
    else:
        cmd = d["command"].strip().lower()

    if "youtube" in cmd:
        q = cmd
        patterns = [
            "open youtube and search",
            "open youtube and play",
            "open youtube",
            "search for",
            "search",
            "and play",
            "play",
            "on youtube"
        ]
        for p in patterns:
            q = q.replace(p, "")
        q = q.strip()
        vid = get_vid(q)
        if vid:
            target = f"https://www.youtube.com/watch?v={vid}&autoplay=1"
            msg = f"Playing {q}"
        else:
            enc = urllib.parse.quote_plus(q)
            target = f"https://www.youtube.com/results?search_query={enc}"
            msg = f"Searching YouTube for {q}"

    elif any(k in cmd for k in ["gmail", "email", "mail"]):
        to, body = "", ""
        tm = re.search(r"to\s+([a-zA-Z0-9._%+\s]+)", cmd)
        if tm:
            c = tm.group(1).replace(" at ", "@").replace(" ", "")
            to = c if "@" in c else f"{c}@gmail.com"
        else:
            to = "sharanbalaji2025@gmail.com"
            
        bm = re.search(r"(?:type|write|message)\s+(.*)", cmd)
        if bm:
            body = bm.group(1).strip()
        else:
            body = "how was your day"
            
        base = "https://mail.google.com/mail/u/0/?view=cm&fs=1"
        params = urllib.parse.urlencode({"to": to, "body": body})
        target = f"{base}&{params}"
        msg = f"Drafting email to {to}"
    
    else:
        enc = urllib.parse.quote_plus(cmd)
        target = f"https://www.google.com/search?q={enc}"
        msg = f"Searching Google for {cmd}"

    return jsonify({
        "success": True,
        "message": msg,
        "url": target
    })

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8000))
    )

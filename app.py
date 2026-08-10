from flask import (
    Flask,
    render_template,
    request,
    jsonify
)
import urllib.parse

app = Flask(__name__)

SITES = {
    "google": "https://www.google.com",
    "gmail": "https://mail.google.com/mail/u/0",
    "youtube": "https://www.youtube.com"
}

def open_site(site):
    if site in SITES:
        return {
            "success": True,
            "message": f"Opening {site}",
            "url": SITES[site]
        }
    return {
        "success": False,
        "message": "Unknown website",
        "url": None
    }

def play_youtube(cmd):
    query = cmd.replace(
        "play", "", 1
    ).strip()
    encoded = urllib.parse.quote(
        query
    )
    url = f"https://www.youtube.com/results?search_query={encoded}"
    return {
        "success": True,
        "message": f"Playing {query}",
        "url": url
    }

def draft_email(cmd):
    parts = cmd.split(" ", 2)
    raw_recipient = (
        parts[1]
        if len(parts) > 1
        else "sharanbalaji2025@gmail.com"
    )
    if "@" not in raw_recipient:
        recipient = (
            f"{raw_recipient}@gmail.com"
        )
    else:
        recipient = raw_recipient

    body = (
        parts[2]
        if len(parts) > 2
        else "how was your day"
    )
    base = "https://mail.google.com/mail/?view=cm&fs=1"
    params = urllib.parse.urlencode({
        "to": recipient,
        "body": body
    })
    url = f"{base}&{params}"
    return {
        "success": True,
        "message": f"Email to {recipient}",
        "url": url
    }

def brain(command):
    cmd = command.lower().strip()
    if cmd.startswith("open"):
        site = cmd.replace(
            "open", "", 1
        ).strip()
        return open_site(site)
    if cmd.startswith("play"):
        return play_youtube(cmd)
    if cmd.startswith("email"):
        return draft_email(cmd)
    return {
        "success": False,
        "message": "Command unknown",
        "url": None
    }

@app.route("/")
def home():
    return render_template(
        "index.html"
    )

@app.route(
    "/agent",
    methods=["POST"]
)
def agent():
    data = request.get_json()
    command = data.get(
        "command", ""
    )
    print("User said:", command)
    response = brain(command)
    return jsonify(response)

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )

from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# ------------------------- 
# WEBSITES
# -------------------------

SITES = {
    "google": "https://www.google.com",
    "openai": "https://www.openai.com",
    "gmail": "https://mail.google.com/mail/u/0",
    "youtube": "https://www.youtube.com"
}


# -------------------------
# AGENT BRAIN
# -------------------------

def brain(command):

    command = command.lower().strip()

    if command.startswith("open"):

        site = command.replace("open", "", 1).strip()

        if site in SITES:

            return {
                "success": True,
                "message": f"Opening {site}",
                "url": SITES[site]
            }

        return {
            "success": False,
            "message": "I don't know that website",
            "url": None
        }

    return {
        "success": False,
        "message": "I don't understand your command",
        "url": None
    }


# -------------------------
# HOME PAGE
# -------------------------

@app.route("/")
def home():
    return render_template("index.html")


# -------------------------
# AGENT API
# -------------------------

@app.route("/agent", methods=["POST"])
def agent():

    data = request.get_json()

    command = data.get("command", "")

    print("User said:", command)

    response = brain(command)

    return jsonify(response)


# -------------------------
# RUN
# -------------------------

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )

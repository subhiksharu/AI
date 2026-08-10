import webbrowser
import speech_recognition as sr

# memory
memory = {}

# tools
SITES = {
    "google": "https://www.google.com",
    "openai": "https://www.openai.com",
    "gmail": "https://mail.google.com/mail/u/0",
    "youtube": "https://www.youtube.com"
}

# brain
def open_site(site):
    key = site.lower().strip()
    if key in SITES:
        webbrowser.open(SITES[key])
        return f"Opening {key}"
    return "I don't know that website"


def brain(command):
    command = command.lower().strip()
    if command.startswith("open"):
        site = command.replace("open", "").strip()
        return open_site(site)
    return "I don't understand your command"


# voice input
def listen(recognizer, mic):
    with mic as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
        except sr.WaitTimeoutError:
            return ""

    try:
        text = recognizer.recognize_google(audio)
        print("You said:", text)
        return text
    except sr.UnknownValueError:
        print("agent: Sorry, I didn't catch that.")
        return ""
    except sr.RequestError as e:
        print(f"agent: Speech service error: {e}")
        return ""


# input + response
def main():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()

    print("Agent can open websites")
    print("Try saying:")
    print("  open gmail")
    print("  open openai")
    print("  open youtube")
    print("Say 'exit' to quit.")

    while True:
        user_input = listen(recognizer, mic)
        if not user_input:
            continue

        if user_input.lower() == "exit":
            print("Agent: goodbye buddy")
            break

        response = brain(user_input)
        print("agent:", response)


if _name_ == "_main_":
    main()

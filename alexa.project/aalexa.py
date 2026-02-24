import speech_recognition as sr
import pyttsx3
import pywhatkit
import wikipedia
import pyjokes
import datetime
import sys

# Initialize recognizer and text-to-speech engine
listener = sr.Recognizer()
engine = pyttsx3.init()

# Set female voice (optional)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Use [0] for male voice


def talk(text):
    print("Alexa:", text)
    engine.say(text)
    engine.runAndWait()


def take_command():
    command = ""
    try:
        with sr.Microphone() as source:
            print("Listening...")
            listener.adjust_for_ambient_noise(source, duration=1)
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()

            if 'alexa' in command:
                command = command.replace('alexa', '').strip()

            print("You said:", command)

    except sr.UnknownValueError:
        print("Sorry, I didn't understand that.")

    except sr.RequestError:
        print("Network error. Check your internet connection.")

    return command


def run_alexa():
    command = take_command()

    # 🔴 STOP / EXIT COMMAND
    if 'stop' in command or 'exit' in command or 'shutdown' in command:
        talk("Goodbye Prasanna. Shutting down now.")
        sys.exit()

    # 🎵 Play music
    elif 'play' in command:
        song = command.replace('play', '').strip()
        talk("Playing " + song)
        pywhatkit.playonyt(song)

    # ⏰ Tell time
    elif 'time' in command:
        current_time = datetime.datetime.now().strftime('%I:%M %p')
        talk("The current time is " + current_time)

    # 📖 Wikipedia search
    elif 'who is' in command or 'who the heck is' in command:
        person = command.replace('who the heck is', '').replace('who is', '').strip()
        try:
            info = wikipedia.summary(person, 1)
            print(info)
            talk(info)
        except:
            talk("Sorry, I couldn't find information about that.")

    # 📅 Date joke
    elif 'date' in command:
        talk("Sorry, I have a headache today.")

    # 💘 Relationship joke
    elif 'are you single' in command:
        talk("I am in a relationship with Wi-Fi.")

    # 😂 Tell joke
    elif 'joke' in command:
        talk(pyjokes.get_joke())

    # 🤔 Unknown command
    elif command != "":
        talk("Please say the command again.")

    else:
        pass


# 🔁 Run continuously
while True:
    run_alexa()
import speech_recognition as sr
import pyttsx3
import openai
from decouple import config

OPENAI_KEY = config("YOUR_OPENAI_API_KEY")
ENGINE = pyttsx3.init()
RECOGNIZER = sr.Recognizer()


def get_voice_input():
    while True:
        try:
            with sr.Microphone() as source:
                RECOGNIZER.adjust_for_ambient_noise(source, duration=0.5)
                print("Listening...")
                audio = RECOGNIZER.listen(source)
                print("Recognizing...")
                message = RECOGNIZER.recognize_whisper(audio, language="english")
                print(f"You said: {message}")
                return message
        except sr.RequestError as e:
            print(f"Could not request results from PocketSphinx service; {e}")
            return None
        except sr.UnknownValueError:
            print("Sorry, I did not hear your request.")
            return None


def get_chatgpt_response(messages, model='gpt-3.5-turbo'):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0.5,
        max_tokens=100,
        stop=None,
        n=1
    )
    message = response.choices[0].message.content
    messages.append(response.choices[0].message)
    return message


def speak(response):
    print(f"Jarvis: {response}")
    ENGINE.say(response)
    ENGINE.runAndWait()


if __name__ == "__main__":
    openai.api_key = OPENAI_KEY
    current_messages = []
    print("Jarvis: Hello! How can I assist you today?")
    while True:
        user_input = get_voice_input()
        if user_input:
            if "terminate" in user_input.lower():
                speak("Goodbye!")
                break
            current_messages.append({"role": "user", "content": user_input})
            chatgpt_response = get_chatgpt_response(current_messages)
            speak(chatgpt_response)

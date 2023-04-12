import speech_recognition as sr
import openai
from playsound import playsound
from dotenv import load_dotenv 
import requests
import os
import io
from pydub import AudioSegment
from pydub.playback import play

load_dotenv()

openai.api_key = os.getenv('OPEN_AI_API_KEY')
elevenlabs_api_key = os.getenv('ELEVEN_LABS_API_KEY')

def text_to_speech(text):
    req_body = {
        "text": text,
        "voice_settings": {
            "stability": 0,
            "similarity_boost": 0
        }
     }

    url = "https://api.elevenlabs.io/v1/text-to-speech/ntc4LoN5mYFjO8ppbtq2"
    headers = {"xi-api-key": elevenlabs_api_key}

    response = requests.post(url, headers=headers, json=req_body)

    audio_data = io.BytesIO(response.content)
    audio_segment = AudioSegment.from_file(audio_data, format="mp3")
    play(audio_segment)    

r = sr.Recognizer()

def get_voice_command():
    with sr.Microphone() as source:
        print("Speak now...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        print("Capturing input...")
        try:
            text = r.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, I didn't understand that.")
            return None

def get_response(prompt):
    response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
                ],
            stream=True
            )

    output_string = ''

    for idx, chunk in enumerate(response):
        if idx != 0:
            output_string += chunk.choices[0].delta.content

            if output_string[-1] == '.':
                text_to_speech(output_string)
                output_string = ''

while True:
    command = get_voice_command()
    if command:
        response = get_response(command)
        print(response)

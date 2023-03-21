import speech_recognition as sr
import openai
from google.cloud import texttospeech
from playsound import playsound

openai.api_key = "OPENAI_KEY"

client = texttospeech.TextToSpeechClient.from_service_account_json('google.json')

def text_to_speech(text):
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(language_code="en-AU", ssml_gender=texttospeech.SsmlVoiceGender.MALE)
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)
    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
    with open("output.mp3", "wb") as out:
        out.write(response.audio_content)
    playsound("output.mp3")

r = sr.Recognizer()

def get_voice_command():
    with sr.Microphone() as source:
        print("Speak now...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
        print("Listening...")
        try:
            text = r.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, I didn't understand that.")
            return None

def get_gpt3_response(prompt):
    response = openai.Completion.create(
        engine="curie",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response.choices[0].text.strip()

while True:
    command = get_voice_command()
    if command:
        response = get_gpt3_response(command)
        print(response)
        text_to_speech(response)

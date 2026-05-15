import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv("../.env")

client = genai.Client()

with open('../res/mamba.mp3', 'rb') as f:
    audio_data = f.read()

prompt = '''
Process the audio file, transcribe and generate a SRT file.
Rules:
Match each word exactly.
Seperate sentenses properly, make each sentence less than 10 words.
Do not summarize or paraphrase.
Do not correct grammar or 'clean up' the speech.
Maintain the original language of the speaker.
Use exactly SRT file format.
'''

response = client.models.generate_content(
    model='gemini-3.1-pro-preview',
    contents=[
        types.Part.from_bytes(
            data=audio_data,
            mime_type='audio/mpeg'
        ),
        prompt
    ]
)

print(response.text)

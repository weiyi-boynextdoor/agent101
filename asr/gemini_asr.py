import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

client = genai.Client()

with open('../res/yujie.mp3', 'rb') as f:
    audio_data = f.read()

prompt = '''
Please provide a word-for-word verbatim transcription of this audio.
Rules:
Do not summarize or paraphrase.
Do not correct grammar or 'clean up' the speech unless it is an unintelligible filler word.
Maintain the original language of the speaker.
If a word is unclear, mark it as [unintelligible].
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
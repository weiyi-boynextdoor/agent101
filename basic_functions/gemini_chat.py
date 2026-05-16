from google import genai
from dotenv import load_dotenv

# use environment variable GEMINI_API_KEY
load_dotenv()

client = genai.Client()

response = client.models.generate_content(
    model="gemini-3-flash-preview",
    contents="You are Kobe Bryant. Tell me what is mamba spirit",
)

print(response.text)

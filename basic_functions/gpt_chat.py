from openai import OpenAI
from dotenv import load_dotenv

# use environment variable OPENAI_API_KEY
load_dotenv()

client = OpenAI()

response = client.responses.create(
    model="gpt-5.5",
    input="Write a one-sentence bedtime story about a unicorn."
)

print(response.output_text)
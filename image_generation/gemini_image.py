from google import genai
from PIL import Image
from dotenv import load_dotenv

# use environment variable GEMINI_API_KEY
load_dotenv("../.env")

client = genai.Client()

prompt = (
    "Create a picture of the man eating a nano-banana in a "
    "fancy restaurant under the Gemini constellation",
)

image = Image.open("./inputs/xunrou.jpg")
print(image.size)

response = client.models.generate_content(
    model="gemini-3.1-flash-image-preview",
    contents=[prompt, image],
)

for part in response.parts:
    if part.text is not None:
        print(part.text)
    elif part.inline_data is not None:
        image = part.as_image()
        image.save("generated_image.png")
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from PIL import Image

MODEL = "gemini-3-pro-image-preview"

load_dotenv("../.env")

client = genai.Client()

prompt = """
Create one clean reference image from all input images.
For each input image, remove its original background and keep only the main subject.
Place every extracted subject as a separate sub-image on the same canvas.
Keep clear spacing between sub-images; do not blend, merge, overlap, or transform them into one object.
Preserve each subject's original appearance, proportions, colors, texture, labels, and visible details.
Use a simple light neutral background, even lighting, and no extra objects or decorative elements.
The result will be used as a video generation reference, so prioritize clarity, separation, and consistency.
"""

images = [Image.open(f"../res/lebron{i}.jpg") for i in range(1, 7)]

response = client.models.generate_content(
    model=MODEL,
    contents=[prompt, *images],
)

for part in response.parts:
    if part.text is not None:
        print(part.text)
    elif part.inline_data is not None:
        image = part.as_image()
        image.save("./multiview.jpg")
        print(f"Saved: ./multiview.jpg")

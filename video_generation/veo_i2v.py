# https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/video/generate-videos-from-an-image?hl=zh-cn

import time
from pathlib import Path

from google import genai
from google.genai.types import (
    GenerateVideosConfig,
    GenerateVideosSource,
    Image,
    VideoGenerationReferenceImage,
    VideoGenerationReferenceType,
)
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parents[1]

load_dotenv(ROOT_DIR / ".env")

client = genai.Client()

xunrou_image = (ROOT_DIR / "res" / "xunrou.jpg").read_bytes()
shoe_image = (ROOT_DIR / "res" / "lebron1.jpg").read_bytes()

operation = client.models.generate_videos(
    model="veo-3.1-generate-001",
    source=GenerateVideosSource(
        prompt="The man in the first reference image smiles and dunks a basketball. He wears the shoes in the second reference image.",
    ),
    config=GenerateVideosConfig(
        aspect_ratio="16:9",
        reference_images=[
            VideoGenerationReferenceImage(
                image=Image(
                    image_bytes=xunrou_image,
                    mime_type="image/jpeg",
                ),
                reference_type=VideoGenerationReferenceType.ASSET,
            ),
            VideoGenerationReferenceImage(
                image=Image(
                    image_bytes=shoe_image,
                    mime_type="image/jpeg",
                ),
                reference_type=VideoGenerationReferenceType.ASSET,
            ),
        ]
    ),
)

while not operation.done:
    time.sleep(15)
    operation = client.operations.get(operation)
    print(operation)

if operation.response:
    video = operation.response.generated_videos[0].video
    with open("output.mp4", "wb") as f:
        f.write(video.video_bytes)

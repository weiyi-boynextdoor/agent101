# https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/video/generate-videos-from-text?hl=zh-cn

import time
from google import genai
from google.genai.types import GenerateVideosSource, GenerateVideosConfig
from dotenv import load_dotenv

load_dotenv("../.env")

client = genai.Client()

operation = client.models.generate_videos(
    model="veo-3.1-generate-001",
    source=GenerateVideosSource(
        prompt="a cat reading a book",
    ),
    config=GenerateVideosConfig(
        aspect_ratio="16:9",
    ),
)

while not operation.done:
    time.sleep(15)
    operation = client.operations.get(operation)
    print(operation)

if operation.response:
    # print(operation.result.generated_videos[0].video.uri)
    video = operation.response.generated_videos[0].video
    with open("output.mp4", "wb") as f:
        f.write(video.video_bytes)

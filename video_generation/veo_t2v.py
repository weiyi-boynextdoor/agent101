import time
from google import genai
from google.genai.types import GenerateVideosConfig
from dotenv import load_dotenv

load_dotenv("../.env")

client = genai.Client()

# TODO(developer): Update and un-comment below line
# output_gcs_uri = "gs://your-bucket/your-prefix"

operation = client.models.generate_videos(
    model="veo-3.1-generate-001",
    prompt="a cat reading a book",
    config=GenerateVideosConfig(
        aspect_ratio="16:9",
        # output_gcs_uri=output_gcs_uri,
    ),
)

while not operation.done:
    time.sleep(15)
    operation = client.operations.get(operation)
    print(operation)

if operation.response:
    # print(operation.result.generated_videos[0].video.uri)
    video = operation.response.generated_videos[0].video
    if video.mime_type == "video/mp4":
        with open("output.mp4", "wb") as f:
            f.write(video.video_bytes)

# Example response:
# gs://your-bucket/your-prefix

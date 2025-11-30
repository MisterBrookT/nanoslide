from typing import Any
from dataclasses import dataclass
from typing import Optional
from PIL import Image as PILImage
from google import genai
from google.genai import types
from pathlib import Path


@dataclass
class LMResponse:
    text: Optional[str] = None
    image: Optional[PILImage] = None
    video: Optional[bytes] = None


class GoogleCaller:
    @staticmethod
    def generate_text(model: str, prompt: str, **kwargs: Any) -> LMResponse:
        client = genai.Client()
        response = client.models.generate_content(model=model, contents=prompt)
        return LMResponse(text=response.text, image=None)

    @staticmethod
    def understand_file(
        model: str, prompt: str, file_path: Path, **kwargs: Any
    ) -> LMResponse:
        client = genai.Client()
        response = client.models.generate_content(
            model=model,
            contents=[
                types.Part.from_bytes(
                    data=file_path.read_bytes(), mime_type="application/pdf"
                ),
                prompt,
            ],
        )
        return LMResponse(text=response.text, image=None)

    @staticmethod
    def generate_image(
        model: str,
        prompt: str,
        reference_image_path: Path | None = None,
        **kwargs: Any,
    ) -> LMResponse:
        """Generate image with optional reference image for style consistency.

        Args:
            model: Model name to use.
            prompt: Text prompt for generation.
            reference_image_path: Optional path to reference image for style consistency.
        """
        client = genai.Client()

        if reference_image_path:
            image = PILImage.open(reference_image_path)
            contents = [prompt, image]
        else:
            contents = [prompt]

        response = client.models.generate_content(
            model=model,
            contents=contents,
        )

        text = None
        image = None
        for part in response.parts:
            if part.text is not None:
                text = part.text
            elif part.inline_data is not None:
                image = part.as_image()
        return LMResponse(text=text, image=image)

    @staticmethod
    def generate_video(model: str, prompt: str, **kwargs: Any) -> LMResponse:
        """Generate video using veo model."""
        import time

        client = genai.Client()

        # Start video generation operation
        operation = client.models.generate_videos(
            model=model,
            prompt=prompt,
        )

        # Poll for completion
        while not operation.done:
            time.sleep(10)
            operation = client.operations.get(operation)

        # Get the video result
        video_bytes = None
        if operation.response and operation.response.generated_videos:
            video = operation.response.generated_videos[0]
            video_bytes = client.files.download(file=video.video)

        return LMResponse(video=video_bytes)


if __name__ == "__main__":
    from nanoslide.utils.io import extract_from_markdown
    from nanoslide.prompts.plan import get_plan_prompt

    response = GoogleCaller.understand_file(
        model="gemini-3-pro-preview",
        prompt=get_plan_prompt(
            user_prompt="多蜡笔小新动漫手绘风格，信息密度高，动漫人物形象明显, 用中文"
        ),
        file_path=Path("examples/scorpio.pdf"),
    )

    print(extract_from_markdown(response.text))

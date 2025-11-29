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
    def generate_image(model: str, prompt: str, **kwargs: Any) -> LMResponse:
        client = genai.Client()
        response = client.models.generate_content(
            model=model,
            contents=[prompt],
        )
        text = None
        image = None
        for part in response.parts:
            if part.text is not None:
                text = part.text
            elif part.inline_data is not None:
                image = part.as_image()
        return LMResponse(text=text, image=image)


if __name__ == "__main__":
    response = GoogleCaller.understand_file(
        model="gemini-3-pro-preview",
        prompt="what this paper mainly contribute for, respond this in chinese",
        file_path=Path("examples/scorpio.pdf"),
    )

    print(response.text)

"""Prompts for generating slide images."""


def get_slide_prompt(
    slide_content: str,
    has_reference: bool = False,
) -> str:
    """Generate the prompt for creating a single slide image.

    Args:
        slide_content: The story-driven content for this slide (from plan).
        has_reference: Whether a reference image is provided for style consistency.

    Returns:
        The complete prompt for slide image generation.
    """
    reference_instruction = ""
    if has_reference:
        reference_instruction = """
STYLE REFERENCE:
A reference image is provided. Match its artistic style, character design, color palette, and overall visual language. Only the scene content may differ.
"""

    prompt = f"""Create an image based on the scene below.

{reference_instruction}
SCENE:
{slide_content}

REQUIREMENTS:
- Clear, vivid illustration of the scene.
- Aspect ratio 16:9.
- Characters and actions must be clearly visible.

"""

    return prompt

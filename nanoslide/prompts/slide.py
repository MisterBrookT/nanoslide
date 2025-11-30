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

    prompt = f"""Create a 16:9 illustration of the following scene in the **official Zootopia (Disney 2016) art style**.

STYLE REQUIREMENTS:
- Soft, warm, natural lighting (not neon, not sci-fi, not holograms)
- No futuristic UI, no cyberpunk elements, no glowing screens
- Characters must follow Zootopia proportions, textures, and expressions
- Environments must match Zootopia’s grounded, semi-realistic world

{reference_instruction}
SCENE DESCRIPTION:
{slide_content}

OUTPUT:
One high-quality Zootopia-style image."""
    return prompt

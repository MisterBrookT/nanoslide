"""Prompts for generating video from slides."""


def get_video_prompt(
    slide_description: str,
    duration: int = 10,
) -> str:
    """Generate the prompt for creating video content from a slide.

    Args:
        slide_description: The story-driven scene description from plan.
        duration: Target duration in seconds for this segment.

    Returns:
        The complete prompt for video generation.
    """
    return f"""Create a short animated video segment based on the following scene.

## SCENE DESCRIPTION
{slide_description}

## VIDEO REQUIREMENTS
1. Duration: approximately {duration} seconds
2. Bring the scene to life with subtle animations and movement
3. Characters should have natural, expressive movements
4. Maintain the artistic style described in the scene
5. Smooth camera work (gentle pans, zooms if appropriate)
6. Create atmosphere through motion and visual effects
7. No text overlays - purely visual storytelling

## OUTPUT
Generate ONE animated video segment that captures the essence of this scene.
"""

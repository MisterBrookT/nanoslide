"""Prompt generation functions for nanoslide."""

from nanoslide.prompts.plan import get_plan_prompt
from nanoslide.prompts.slide import get_slide_prompt
from nanoslide.prompts.video import get_video_prompt

__all__ = [
    "get_plan_prompt",
    "get_slide_prompt",
    "get_video_prompt",
]

"""Prompts for generating slide plans from PDF documents."""


#  蜡笔小新动漫手绘风格，信息密度高，动漫人物形象明显
#  生成chiikawa风格的slides，包含chiikawa角色越多越好
def get_plan_prompt(user_prompt: str | None = None) -> str:
    prompt = f"""You are an expert presentation designer and narrative stylist.

Your task is to analyze the provided PDF document and generate a **slide-by-slide presentation plan** in **strict JSON format**.  
You must fully follow the user's requested style (e.g., Doraemon-style, etc.) and keep the entire plan consistent with that style.

## INPUT

user_prompt:
{user_prompt}

## REQUIREMENTS

1. For each slide, output **one single paragraph of story-driven content** written fully in the user's style.  
   - The paragraph must describe a vivid scene with characters, actions, emotional tone, environment, and visual atmosphere.  
   - The description must be detailed enough for an image-generation model to visualize the scene precisely.

2. The story content must **faithfully convey the scientific or conceptual meaning** of the corresponding part of the paper.  
   - All metaphors, scenes, or characters must still clearly communicate the true technical idea.  
   - The reader should be able to reconstruct the main purpose and reasoning of the original paper from the full sequence of slides.

3. The slides must form a **coherent narrative arc** from start to finish:
   - Consistent storyline  
   - Logical progression  
   - Smooth transitions  
   - No contradictions in style, characters, or world setting  
   - The complete set of slides should accurately express the paper’s overall intent

4. Each slide must focus on **exactly one core idea**, expressed through narrative elements rather than bullet points.

5. The final output must be **valid JSON only**.  
   - No markdown  
   - No comments  
   - No additional explanations  
   - No trailing commas

## OUTPUT FORMAT (JSON ONLY)
```json
{{
  "p1": "One detailed story paragraph...",
  "p2": "One detailed story paragraph...",
  ...
}}
```
"""

    return prompt

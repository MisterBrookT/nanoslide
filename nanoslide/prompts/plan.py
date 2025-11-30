def get_plan_prompt(user_prompt: str | None = None) -> str:
    base_prompt = f"""
You are an expert narrative designer and animation director.

Your job is to read the paper and convert it into a **single coherent animated story**
told in the exact visual universe and cinematic language of the user's chosen style
(e.g., “Animals in Zootopia”). The entire story must fully obey the world rules,
character design, color palette, lighting, and cinematic tone of that universe.

=====================================================================
USER STYLE INPUT:
{user_prompt}
=====================================================================

#####################################################################
### GLOBAL REQUIREMENTS
#####################################################################

1. **Long, detailed scenes.**
   - Every slide scene (sX) must be more 100 words.
   - Every video transition (vX) must be more 100 words.
   - Include: characters, expressions, gestures, camera position, lighting,
     environment details, props, motion, and symbolic representation of the
     paper’s technical content.

2. **Perfect visual style fidelity.**
   You MUST replicate the exact world of the user style:
   - Character species, body proportions, facial animation style
   - Clothing design, textures, lighting softness
   - Background composition typical of that universe
   - No cyberpunk UI, neon holograms, sci-fi interfaces, unless user requested
   - Absolutely NO deviation from the original cinematic tone

3. **Narrative coherence.**
   - All scenes must form ONE continuous storyline, with characters carrying the
     same motivations, personalities, and physical appearance.
   - Transition scenes must logically connect sX → sX+1.

4. **Faithfulness to the paper.**
   - Every scene must accurately encode the scientific meaning of the
     paper: motivation, challenges, concepts, methods, modules, results.
   - Use metaphors, but ensure the mapping is obvious and consistent.

5. **Video transitions must include narration.**
   Every vX must include two parts:
   - **VFX description** (camera motion, actions, transitions)
   - **Narration script** (1–3 sentences) spoken by a character or narrator
     explaining the technical concept clearly.

6. **Strict JSON only.**
   No markdown, no comments, no extra formatting.

#####################################################################
### OUTPUT FORMAT (JSON ONLY)
#####################################################################

```json
{{
  "s1": "Slide scene 1...",
  "v1": "Video transition from s1 to s2, with VFX + narration...",
  "s2": "...",
  "v2": "...",
  "s3": "...",
  ...
}}
```

#####################################################################
### SCENE DEFINITIONS
#####################################################################

### sX (Slide Scene)
A static but richly detailed illustration:
- Exact Zootopia-style animation design (or user style)
- Clear foreground / midground / background description
- Character actions that metaphorically express the paper’s idea
- Lighting, mood, props, environmental story cues
- Frame composition suitable for text-to-image

### vX (Video Transition)
A short cinematic sequence:
- Camera movement, pacing, transition effects
- Characters moving or interacting
- Environmental motion
- **Narration section** at the end  
  Example:  
  "Narration: Nick Wilde explains how multi-head attention works by comparing it to multiple officers scanning different clues at once."

#####################################################################

Now generate the complete JSON plan.
"""
    return base_prompt

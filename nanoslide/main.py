#!/usr/bin/env python3
"""nanoslide CLI - Transform PDFs into engaging slide presentations and videos."""

import json
from pathlib import Path
from typing import Annotated

import typer

from nanoslide.prompts import get_plan_prompt, get_slide_prompt, get_video_prompt
from nanoslide.utils.google_caller import GoogleCaller
from nanoslide.utils.io import extract_from_markdown

app = typer.Typer(
    name="nanoslide",
    help="Transform PDFs into engaging slide presentations and videos.",
    add_completion=False,
)


def get_output_dir(pdf_path: Path, output_dir: Path) -> Path:
    """Get the output directory for a given PDF file.

    Creates directory structure: output_dir/<pdf_stem>/
    """
    stem = pdf_path.stem
    result_dir = output_dir / stem
    result_dir.mkdir(parents=True, exist_ok=True)
    return result_dir


def _create_pptx(slides_dir: Path, pptx_path: Path) -> None:
    """Create PowerPoint presentation from slide images."""
    from pptx import Presentation
    from pptx.util import Inches

    # Find all slide images
    slide_files = sorted(
        slides_dir.glob("slide_*.png"),
        key=lambda x: int(x.stem.split("_p")[-1]) if "_p" in x.stem else 0,
    )

    if not slide_files:
        typer.echo(f"  ⚠️  No slide images found in {slides_dir}")
        return

    typer.echo(f"📑 Creating PowerPoint from {len(slide_files)} slides...")

    # Create presentation with 16:9 aspect ratio
    prs = Presentation()
    prs.slide_width = Inches(13.333)  # 16:9 width
    prs.slide_height = Inches(7.5)  # 16:9 height

    # Add each slide image
    blank_layout = prs.slide_layouts[6]  # Blank layout

    for slide_file in slide_files:
        typer.echo(f"  Adding: {slide_file.name}")
        slide = prs.slides.add_slide(blank_layout)

        # Add image to fill the entire slide
        slide.shapes.add_picture(
            str(slide_file),
            Inches(0),
            Inches(0),
            width=prs.slide_width,
            height=prs.slide_height,
        )

    # Save presentation
    prs.save(str(pptx_path))
    typer.echo(f"✅ PowerPoint saved to: {pptx_path}")


@app.command()
def plan(
    pdf: Annotated[Path, typer.Argument(help="Path to the source PDF file")],
    output_dir: Annotated[
        Path, typer.Option("--output", "-o", help="Output directory")
    ] = Path("outputs"),
    prompt: Annotated[
        str | None, typer.Option("--prompt", "-p", help="Style prompt for slides")
    ] = None,
    exist: Annotated[
        bool, typer.Option("--exist", "-e", help="Skip if output already exists")
    ] = False,
) -> Path:
    """Generate a slide plan from a PDF document.

    Analyzes the PDF and creates a detailed JSON plan for each slide.
    Output: outputs/<pdf_name>/plan.json
    """
    if not pdf.exists():
        typer.echo(f"Error: PDF file not found: {pdf}", err=True)
        raise typer.Exit(1)

    # Setup output directory
    result_dir = get_output_dir(pdf, output_dir)
    plan_file = result_dir / "plan.json"

    # Check if already exists
    if exist and plan_file.exists():
        typer.echo(f"⏭️  Skipping plan (already exists): {plan_file}")
        return plan_file

    typer.echo(f"📄 Reading PDF: {pdf}")

    # Default style prompt
    user_prompt = prompt or "蜡笔小新动漫手绘风格，信息密度高，动漫人物形象明显，用中文"

    typer.echo("🧠 Generating slide plan...")
    typer.echo(f"   Style: {user_prompt}")

    # Generate plan using Gemini
    plan_prompt = get_plan_prompt(user_prompt=user_prompt)
    response = GoogleCaller.understand_file(
        model="gemini-3-pro-preview",
        prompt=plan_prompt,
        file_path=pdf,
    )

    json.dump(
        extract_from_markdown(response.text),
        plan_file.open("w"),
        indent=2,
        ensure_ascii=False,
    )
    typer.echo(f"✅ Plan saved to: {plan_file}")
    return plan_file


@app.command()
def gen_slide(
    pdf: Annotated[Path, typer.Argument(help="Path to the source PDF file")],
    output_dir: Annotated[
        Path, typer.Option("--output", "-o", help="Output directory")
    ] = Path("outputs"),
    plan_file: Annotated[
        Path | None,
        typer.Option(
            "--plan", help="Path to existing plan.json (auto-detected if not provided)"
        ),
    ] = None,
    exist: Annotated[
        bool, typer.Option("--exist", "-e", help="Skip slides that already exist")
    ] = False,
) -> Path:
    """Generate slide images from a plan and create PowerPoint.

    Reads the plan.json and generates slide images, then fuses them into a PPT.
    Output: outputs/<pdf_name>/slide_pieces/*.png, outputs/<pdf_name>/presentation.pptx
    """
    result_dir = get_output_dir(pdf, output_dir)

    # Find plan file
    if plan_file is None:
        plan_file = result_dir / "plan.json"

    typer.echo(f"📋 Reading plan: {plan_file}")
    plan_content = json.loads(plan_file.read_text())

    # Create slides directory
    slides_dir = result_dir / "slide_pieces"
    slides_dir.mkdir(parents=True, exist_ok=True)

    typer.echo("🎨 Generating slides...")

    # Parse plan and generate slides
    sorted_keys = sorted(
        plan_content.keys(),
        key=lambda x: int(x[1:]) if x[1:].isdigit() else 0,
    )

    previous_slide_path = None
    for slide_num in sorted_keys:
        slide_path = slides_dir / f"slide_{slide_num}.png"

        # Check if already exists
        if exist and slide_path.exists():
            typer.echo(f"  ⏭️  Skipping slide {slide_num} (already exists)")
            previous_slide_path = slide_path
            continue

        slide_content = plan_content[slide_num]
        typer.echo(f"  Generating slide {slide_num}...")

        # Check if previous slide exists for style reference
        has_reference = previous_slide_path is not None and previous_slide_path.exists()
        if has_reference:
            typer.echo(
                f"    Using previous slide as style reference: {previous_slide_path.name}"
            )

        slide_prompt = get_slide_prompt(
            slide_content=slide_content,
            has_reference=has_reference,
        )

        response = GoogleCaller.generate_image(
            model="gemini-3-pro-image-preview",
            prompt=slide_prompt,
            reference_image_path=previous_slide_path if has_reference else None,
        )

        response.image.save(slide_path)
        typer.echo(f"    ✅ Saved: {slide_path}")

        # Update previous slide path for next iteration
        previous_slide_path = slide_path

    typer.echo(f"✅ Slides saved to: {slides_dir}")

    # Create PowerPoint presentation
    pptx_path = result_dir / "presentation.pptx"
    _create_pptx(slides_dir, pptx_path)

    return slides_dir


@app.command()
def gen_video(
    pdf: Annotated[Path, typer.Argument(help="Path to the source PDF file")],
    output_dir: Annotated[
        Path, typer.Option("--output", "-o", help="Output directory")
    ] = Path("outputs"),
    plan_file: Annotated[
        Path | None,
        typer.Option(
            "--plan", help="Path to existing plan.json (auto-detected if not provided)"
        ),
    ] = None,
    exist: Annotated[
        bool,
        typer.Option("--exist", "-e", help="Skip video segments that already exist"),
    ] = False,
) -> Path:
    """Generate video from slides using veo3.

    Reads the plan.json and generates video segments.
    Output: outputs/<pdf_name>/video/*.mp4
    """
    result_dir = get_output_dir(pdf, output_dir)

    # Find plan file
    if plan_file is None:
        plan_file = result_dir / "plan.json"

    if not plan_file.exists():
        typer.echo(f"Error: Plan file not found: {plan_file}", err=True)
        typer.echo("Run 'nanoslide plan' first to generate a plan.")
        raise typer.Exit(1)

    typer.echo(f"📋 Reading plan: {plan_file}")
    plan_content = json.loads(plan_file.read_text())

    # Create video directory
    video_dir = result_dir / "video"
    video_dir.mkdir(parents=True, exist_ok=True)

    typer.echo("🎬 Generating video...")

    # Parse plan and generate video segments
    sorted_keys = sorted(
        plan_content.keys(),
        key=lambda x: int(x[1:]) if x[1:].isdigit() else 0,
    )
    total_slides = len(sorted_keys)

    for key in sorted_keys:
        slide_num = int(key[1:]) if key[1:].isdigit() else 1
        video_path = video_dir / f"segment_{slide_num}.mp4"

        # Check if already exists
        if exist and video_path.exists():
            typer.echo(f"  ⏭️  Skipping video segment {slide_num} (already exists)")
            continue

        slide_content = plan_content[key]
        typer.echo(f"  Generating video segment {slide_num}/{total_slides}...")

        video_prompt = get_video_prompt(slide_description=slide_content)

        response = GoogleCaller.generate_video(
            model="veo-2.0-generate-001",
            prompt=video_prompt,
        )

        if response.video:
            video_path.write_bytes(response.video)
            typer.echo(f"    ✅ Saved: {video_path}")
        else:
            typer.echo(f"    ⚠️  Warning: No video generated for segment {slide_num}")

    typer.echo(f"✅ Video segments saved to: {video_dir}")
    return video_dir


@app.command()
def pipe(
    pdf: Annotated[Path, typer.Argument(help="Path to the source PDF file")],
    output_dir: Annotated[
        Path, typer.Option("--output", "-o", help="Output directory")
    ] = Path("outputs"),
    prompt: Annotated[
        str | None, typer.Option("--prompt", "-p", help="Style prompt for slides")
    ] = None,
    video: Annotated[
        bool, typer.Option("--video", "-v", help="Also generate video from slides")
    ] = False,
    exist: Annotated[
        bool, typer.Option("--exist", "-e", help="Skip steps if output already exists")
    ] = False,
) -> None:
    """Run the complete pipeline: plan → gen_slide (with PPT) → (gen_video).

    This is a convenience command that runs all steps in sequence.
    Output: outputs/<pdf_name>/
      - plan.json
      - slide_pieces/*.png
      - presentation.pptx
      - video/*.mp4 (if --video is set)
    """
    typer.echo("🚀 Starting nanoslide pipeline...")
    typer.echo("=" * 50)

    # Step 1: Generate plan
    typer.echo("\n📝 STEP 1: Generating plan...")
    plan_file = plan(pdf=pdf, output_dir=output_dir, prompt=prompt, exist=exist)

    # Step 2: Generate slides (includes PPT creation)
    typer.echo("\n🎨 STEP 2: Generating slides & PowerPoint...")
    gen_slide(pdf=pdf, output_dir=output_dir, plan_file=plan_file, exist=exist)

    # Step 3: Generate video (optional)
    if video:
        typer.echo("\n🎬 STEP 3: Generating video...")
        gen_video(pdf=pdf, output_dir=output_dir, plan_file=plan_file, exist=exist)

    typer.echo("\n" + "=" * 50)
    typer.echo("✨ Pipeline complete!")
    result_dir = get_output_dir(pdf, output_dir)
    typer.echo(f"📁 Output directory: {result_dir}")


@app.command()
def version() -> None:
    """Show version information."""
    typer.echo("nanoslide v0.1.0")


if __name__ == "__main__":
    app()

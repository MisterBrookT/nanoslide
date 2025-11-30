<p align="center">
  <img src="assets/project.png" alt="nanoslide" width="800">
</p>

<p align="center">
  <b>Transform Boring PDFs To Magic.</b><br>
</p>

<p align="center">
  <a href="README-CN.md">🇨🇳 中文文档</a>
</p>



## Features

- 📑 **Slide Generation**: Generates stylistic PowerPoint presentations.
- 🎬 **Video Generation**: Creates smooth transition animations between slides.

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd nanoslide

# Install dependencies
uv install
```

## Configuration

Set up your Google API key before use:

```bash
export GOOGLE_API_KEY="your-api-key-here"
```

## Usage

### Quick Start

Run the complete pipeline (PDF to presentation and video) in one command:

```bash
nanoslide pipe examples/transformer.pdf --prompt "Crayon Shin-chan anime hand-drawn style, high information density"
```

### Step-by-Step

#### 1. Generate Slide Plan

```bash
nanoslide plan examples/transformer.pdf --prompt "your style description"
```

Generates `outputs/transformer/plan.json`.

#### 2. Generate Slides

```bash
nanoslide gen-slide examples/transformer.pdf
```

Generates slide images and PowerPoint file:
- `outputs/transformer/slide_pieces/*.png`
- `outputs/transformer/presentation.pptx`

#### 3. Generate Video (Optional)

```bash
nanoslide gen-video examples/transformer.pdf
```

Generates video segments:
- `outputs/transformer/video/segment_*.mp4`

#### 4. Fuse Outputs

```bash
nanoslide fuse examples/transformer.pdf
```

Merges all video segments into a complete video:
- `outputs/transformer/video/fused.mp4`


## License

[MIT LICENSE](LICENSE).

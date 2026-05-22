# rendering_tools

Converts a device log containing periodic `micropython.mem_info(1)` output into
a sequence of PNG images showing heap memory usage over time.

## Installation

```bash
uv sync
```

Requires `pycairo`. Requires `ffmpeg` only if generating video.

## Usage

From the `rendering_tools` directory:

```bash
uv run mem_usage_render.py <log_file>
```

Generates `image_NNNN.png` files in the current directory. To assemble a video:

```bash
ffmpeg -r 10 -f image2 -s 2100x1252 -i image_%04d.png -vcodec libx264 -crf 25 -pix_fmt yuv420p mem_usage.mp4
```

## Tests

```bash
uv run pytest
```

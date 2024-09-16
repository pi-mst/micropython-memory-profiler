# Examples

## Generate a dump log

In `examples`:

```bash
docker run -ti --rm -v $(pwd):/code -w /code micropython/unix micropython -X heapsize=500000 -c "import mip; mip.install('logging'); import example1" | tee dump.log
```

**TODO** Remember to also install `mem_dump.py` when it's available on github.

- Currently, all lines preceeding the first '@@@' need to be deleted.

## Generate images

In `rendering_tools`:

```bash
uv run mem_usage_render.py ../examples/dump.log
ffmpeg -r 10 -f image2 -s 2100x1252 -i image_%04d.png -vcodec libx264 -crf 25 -pix_fmt yuv420p mem_usage.mp4
```
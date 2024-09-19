# Examples

## Generate a memory dump

In the `examples` folder:

For MicroPython on the unix port (run in a container):

```bash
docker run -ti --rm -v $(pwd):/code -w /code micropython/unix micropython -X heapsize=500000 -c "import mip; mip.install('logging'); mip.install('mem_dump'); import example1" | tee dump_unix.log
```

On a device:

```bash
mpremote mip install logging  # Only needed once
mpremote mip install mem_dump
mpremote mount . exec "import example1" | tee dump_device.log
```

**TODO:** The *install mem_dump* lines above will need to be updated when this
library is published. In the meantime, `mem_dump.py` should be copied to the
filesystem.

## Generate images

In `rendering_tools`:

```bash
uv run mem_usage_render.py ../examples/dump.log
ffmpeg -r 10 -f image2 -s 2100x1252 -i image_%04d.png -vcodec libx264 -crf 25 -pix_fmt yuv420p mem_usage.mp4
```

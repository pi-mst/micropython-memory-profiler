# Examples

## Generate a dump log

In `examples`:

```bash
mpunix micropython -X heapsize=500000 -c "import mip; mip.install('logging'); import app1" >dump.log
```

**TODO** Remember to also install `mem_dump.py` when it's available on github.

- Currently, all lines preceeding the first '@@@' need to be deleted.

## Generate images

In `rendering_tools`:

```bash
uv run mem_usage_render.py ../examples/dump.log
```
# micropython-memory-profiler

A memory profiler for use on MicroPython.

This tool provides a visual representation of heap memory usage over time. It
is helpful for understanding the behaviour of the MicroPython Garbage Collector
(GC) and, in particular, to help ensure that memory fragmentation is minimised
or eliminated.

There are two parts: an *on-device* component (`mem_dump.py`) that periodically
dumps a summarised view of heap memory, and a *PC-side* rendering tool
(`rendering_tools/`) that converts those dumps into images or video.

## On-device

### Installation

```bash
mpremote mip install github:PlanetInnovation/micropython-memory-profiler
```

### Usage

Call one of the following at startup depending on your application's concurrency
model. The default period of 350ms suits most applications; reduce it for
higher resolution at the cost of more output.

#### asyncio

```python
import mem_dump
await mem_dump.start_async()
```

Creates a background asyncio task. Suited to applications already using asyncio.
Since asyncio is co-operative, avoid over-subscribing the event loop or period
accuracy will suffer.

#### Timer

```python
import mem_dump
mem_dump.start_timer()
```

Configures a `machine.Timer` to trigger dumps. Timer behaviour varies by port
(hardware interrupt on most ports, software timer on ESP32).

#### Manual

Neither method is required - call `mem_dump.mem_dump(None)` directly at whatever
cadence suits your application.

### Tips

- Capture output alongside application logs so the renderer can display them
  side by side.
- Each dump is timestamped; some timing jitter is acceptable.

## Visualisation

See [`rendering_tools/`](rendering_tools/README.md) for the PC-side tool that
converts a captured log into PNG images and video. See
[`examples/`](examples/README.md) for end-to-end capture instructions.

# micropython-memory-profiler

A memory profiler for use on MicroPython.

This memory profiling tool is designed to provide a visual representation of
heap memory usage over time.  It is helpful for understanding the behavior of
the MicroPython Garbage Collector (GC) and, in particular, to help ensure that
memory fragmentation is minimised or eliminated.

## Details

There are two parts to this tool; The *on-device* component, encapsulated in
`mem_dump.py`, that periodically *dumps* a summarised view of the contents of the
device's memory. The other component, intended to run on a PC, can render
*visualisations* of the memory dump.

### Memory dumps

Installation:

```bash
mpremote mip install github:pi-mst/micropython-memory-profiler
```

Once installed, there are a couple of different ways - discussed below - to
trigger the memory dumps depending on what best suits your application.

The memory dumps needs to occur frequently enough to observe changes in memory
allocations to help detect any issues. That level of detail will be different
between applications.

The default period of 350ms is reasonable for many applications but there is a
trade-off between the fine-grained visibility in observing memory allocations
versus the overhead of recording each memory dump. If the application is failing
to complete tasks in a timely manner it may be necessary to increase the period.

Each memory dump is timestamped so, while an accurate period is *desirable*,
some jitter is likely to be *acceptable*.

It's also helpful to print the memory dump interleaved with log output; in this
way, rendering tools can display logs alongside a render of the memory.

#### asyncio

If the application to be analysed already employs asyncio, than calling
`start_async` is a convenient option to ensure the memory dump is triggered. It
creates an async task that uses an `asyncio.sleep` to control the period.

Since asyncio is a *co-operative* concurrency feature, care must be taken to
ensure that the asyncio event loop is not over-subscribed elsewhere in the
application otherwise the accuracy of the period will suffer.

#### Timer

If there is no async code in your application then `start_timer` can be called;
it will configure a `machine.Timer` to periodically dump memory. Be aware that
the way that Timers are implemented can differ between ports and this can have
an effect on the accuracy of the period. For example, most ports implement
`Timer` as an interrupt-serviced hardware timer but the ESP32 port uses software
timers.

#### Other

It's not necessary to use either of these methods, the user just needs to ensure
that `mem_dump` is called frequently.

## Todo

- Remember to update `package.json` and the installation links, above, if the
  repo moves

# MIT license; Copyright (c) 2024, Planet Innovation
# SPDX-License-Identifier: MIT
# 436 Elgar Road, Box Hill, 3128, VIC, Australia
# Phone: +61 3 9945 7510
#

import re


class Capture:
    def __init__(self):
        self.title = ""
        self.frames = []

    def add_frame(self, frame, rtc_offset):
        if self.frames:
            # Ensure this next frame is older than the previous frame, but allow
            # an error of 2 milliseconds to account for minor synchronisation issues,
            # and because RTC and CPU counter can run at slightly different speeds.
            assert frame.timestamp_ms > self.frames[-1].timestamp_ms - 2, (
                self.frames[-1].timestamp_ms,
                frame.timestamp_ms,
                frame.timestamp_ms - rtc_offset,
            )
        self.frames.append(frame)


class Frame:
    def __str__(self):
        return str(type(self).__qualname__) + "@ {} ms".format(self.timestamp_ms)


class DummyFrame(Frame):
    def __init__(self, timestamp_ms):
        self.timestamp_ms = timestamp_ms


class LogFrame(Frame):
    def __init__(self, timestamp_ms, line):
        self.timestamp_ms = timestamp_ms
        self.line = line


class HeapFrame(Frame):
    def __init__(self, timestamp_ms, heap):
        self.timestamp_ms = timestamp_ms

        # convert body to something prettier

        def gen(heap: list[str]):
            for entry in heap:
                if entry.find("lines all free") != -1:
                    m = re.search(r"\((\d+) lines all free", entry)
                    for _ in range(int(m.group(1))):
                        yield "." * 64
                else:
                    yield entry[10:]  # The contents of the memory representation

            while True:
                yield ""

        # There is an optional 'mem' line
        # eg  "mem: total=74627, current=42583, peak=42639"
        # If present, ensure it's included to find the top of the heap output.
        start_of_mem = 4  # The start of the memory dump starts on this line
        if heap[0].startswith("mem:"):
            start_of_mem += 1

        header = heap[0:start_of_mem]
        body = []
        g = gen(heap[start_of_mem:])
        MULT = 2
        while True:
            entry = ""
            for _ in range(MULT):
                entry += next(g)
            if not entry:
                break
            addr = len(body) * 0x400 * MULT
            body.append("{:08x}: ".format(addr) + entry)
        self.heap = header + body

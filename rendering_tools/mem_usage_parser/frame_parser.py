

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
            addr = 0

            for entry in heap:
                if entry.find("lines all free") != -1:
                    m = re.search(r"\((\d+) lines all free", entry)
                    for _ in range(int(m.group(1))):
                        yield "." * 64
                        #addr += 1024
                        addr += 0x800
                else:
                    #print(f"entry {entry[:5]}, {addr=}")
                    #assert int(entry[:5], 16) == addr
                    assert int(entry[:8], 16) == addr
                    #print(f"entry2: {entry[10:]}")
                    #yield entry[7:]
                    yield entry[10:] # The contents of the memory representation

                    #addr += 1024
                    addr += 0x800
            while True:
                yield ""

        # There is an optional 'mem' line
        # eg  "mem: total=74627, current=42583, peak=42639"
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
            addr = len(body) * 1024 * MULT
            #body.append("{:05x}: ".format(addr) + entry)
            body.append("{:08x}: ".format(addr) + entry)
        self.heap = header + body

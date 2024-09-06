"""
Convert a device log containing periodic micropython.mem_info(1) into a set of
images suitable to make a video.

A capture should be made first by running mem_usage_main.py on the device.  For
example:

    $ pyboard.py mem_usage_main.py | tee > mem_usage.log

Then run this script to convert the log to a sequence of PNG images:

    $ python mem_usage_render.py mem_usage.log

Video can then be made with (replace -s size with actual size of images):

    ffmpeg -r 10 -f image2 -s 2100x1252 -i image_%04d.png -vcodec libx264 -crf 25 -pix_fmt yuv420p mem_usage.mp4
"""

import re
import sys

import cairo

from mem_usage_parser.frame_parser import Capture, LogFrame, DummyFrame, HeapFrame

COLOUR_BACKGROUND = (1, 1, 1)
COLOUR_TEXT_PLAIN = (0, 0, 0)
COLOUR_TEXT_CHANGED = (1, 0, 0)

def parse_capture(filename):
    capture = Capture()
    rtc_offset = None
    with open(filename) as f:
        while True:
            line = f.readline().rstrip()
            if not line:
                # Skip blank lines
                break
            frame = None
            if line.startswith("@@@ v"):
                # Title line
                capture.title = line[4:]
                print("title:", capture.title)
            elif line.startswith("@@@ ") and line.find(" (") != -1:
                # Timestamp *and* datetime line
                _, timestamp_ms, datetime = line.split(None, 2)
                timestamp_ms = int(timestamp_ms)
                _, _, _, _, hr, mn, sc, us = tuple(
                    int(x) for x in datetime[1:-1].split(", ")
                )
                rtc_offset = (
                    ((hr * 60 + mn) * 60 + sc) * 1000 + us // 1000 - timestamp_ms
                )
                print("timestamp_ms:", timestamp_ms, "rtc_offset:", rtc_offset)
            elif line.startswith("@@@ "):
                # Line with (only) a timestamp. The *frame*, which includes
                # the memory and heap information, follows this line and
                # terminates when a '@@@' line is detected
                _, timestamp_ms = line.split()
                timestamp_ms = int(timestamp_ms)
                heap = []
                while True:
                    # Store all the lines between '@@@' token in heap
                    line = f.readline().rstrip()
                    if line.startswith("@@@"):
                        break
                    heap.append(line)
                if rtc_offset is None:
                    rtc_offset = capture.frames[-1].timestamp_ms - timestamp_ms + 200
                print(heap[:5])
                print(heap[6:])
                frame = HeapFrame(rtc_offset + timestamp_ms, heap)
            else:
                # LogFrame, use the timestamp if it's available
                print("match timestamp")
                print(line)
                m = re.match(r"20\d\d-\d\d-\d\d (\d\d):(\d\d):(\d\d),(\d\d\d) ", line)
                if m:
                    hr = int(m.group(1))
                    mn = int(m.group(2))
                    sc = int(m.group(3))
                    ms = int(m.group(4))
                    timestamp_ms = ((hr * 60 + mn) * 60 + sc) * 1000 + ms
                else:
                    timestamp_ms = capture.frames[-1].timestamp_ms + 10
                frame = LogFrame(timestamp_ms, line)
            if frame:
                capture.add_frame(frame, rtc_offset)
    return capture


def expand_frames(frames, frame_dt_ms):
    timestamp_ms = frames[0].timestamp_ms // frame_dt_ms * frame_dt_ms
    frame_num = 0
    while frame_num < len(frames):
        if timestamp_ms < frames[frame_num].timestamp_ms:
            timestamp_ms += frame_dt_ms
        while timestamp_ms < frames[frame_num].timestamp_ms:
            frames.insert(frame_num, DummyFrame(timestamp_ms))
            frame_num += 1
            timestamp_ms += frame_dt_ms
        frame_num += 1


def render_text_pane(cr, x, y, w, h, fontw, fonth, lines, prev_lines=None):
    if prev_lines:
        assert len(lines) == len(prev_lines)
    cr.rectangle(x, y, w, h)
    cr.clip_preserve()
    cr.set_source_rgb(*COLOUR_BACKGROUND)
    cr.fill()
    cr.set_source_rgb(*COLOUR_TEXT_PLAIN)
    for row, line in enumerate(lines):
        if prev_lines and prev_lines[row] != line:
            prev_line = prev_lines[row]
            for column, char in enumerate(line):
                if column < len(prev_line) and char == prev_line[column]:
                    cr.set_source_rgb(*COLOUR_TEXT_PLAIN)
                else:
                    cr.set_source_rgb(*COLOUR_TEXT_CHANGED)
                cr.move_to(x + 2 + (column) * fontw, y + 2 + (row + 1) * fonth)
                cr.show_text(char)
        else:
            cr.set_source_rgb(0, 0, 0)
            cr.move_to(x + 2, y + 2 + (row + 1) * fonth)
            cr.show_text(line)


def render(rows, columns, capture):
    fonth = 15
    fontw = 8
    width = (20 + columns * fontw) + 3 & ~3
    height = (65 + rows * fonth) + 3 & ~3

    status_x = 0
    status_y = 0
    status_w = width
    status_h = 50

    left_pane_x = 0
    left_pane_y = status_h
    left_pane_w = width // 2
    left_pane_h = height - left_pane_y

    right_pane_x = left_pane_w
    right_pane_y = left_pane_y
    right_pane_w = width - right_pane_x
    right_pane_h = left_pane_h

    ims = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    cr = cairo.Context(ims)

    cr.select_font_face("Mono", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
    cr.set_font_size(14)
    log_lines = []

    prev_heap = None
    for frame_num, frame in enumerate(capture.frames):
        cr.save()
        cr.rectangle(status_x, status_y, status_w, status_h)
        cr.set_source_rgb(*COLOUR_BACKGROUND)
        cr.fill()
        cr.set_source_rgb(*COLOUR_TEXT_PLAIN)
        cr.move_to(status_x + 10, status_y + status_h - 10)
        cr.set_font_size(30)
        cr.show_text(
            "{: 8} ms    {}".format(
                frame.timestamp_ms - capture.frames[0].timestamp_ms, capture.title
            )
        )
        cr.restore()

        cr.save()
        if isinstance(frame, DummyFrame):
            pass
        elif isinstance(frame, LogFrame):
            log_lines.append(frame.line)
            if len(log_lines) > rows:
                log_lines.pop(0)
            render_text_pane(
                cr,
                left_pane_x,
                left_pane_y,
                left_pane_w,
                left_pane_h,
                fontw,
                fonth,
                log_lines,
            )
        elif isinstance(frame, HeapFrame):
            render_text_pane(
                cr,
                right_pane_x,
                right_pane_y,
                right_pane_w,
                right_pane_h,
                fontw,
                fonth,
                frame.heap,
                prev_heap,
            )
            prev_heap = frame.heap
        else:
            assert 0
        cr.restore()

        # write new frame
        print(
            "frame {} at {} ms {}".format(
                frame_num, frame.timestamp_ms, type(frame).__qualname__
            )
        )
        ims.write_to_png("image_{:04}.png".format(frame_num))


def main():
    capture = parse_capture(sys.argv[1])
    max_rows = 0
    for frame in capture.frames:
        if isinstance(frame, HeapFrame):
            max_rows = max(max_rows, len(frame.heap))

    print(
        "{} frames, {} max rows, {} ms".format(
            len(capture.frames),
            max_rows,
            capture.frames[-1].timestamp_ms - capture.frames[0].timestamp_ms,
        )
    )
    expand_frames(capture.frames, 100)
    print("{} frames".format(len(capture.frames)))
    render(max_rows, 260, capture)


main()

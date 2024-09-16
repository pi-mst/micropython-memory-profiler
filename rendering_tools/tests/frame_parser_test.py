
from mem_usage_parser.frame_parser import HeapFrame

class TestHeapFrame:
    def test_unix(self):
        heap = [
            "mem: total=74627, current=42583, peak=42639"
            "stack: 7312 out of 80000"
            "GC: total: 2072832, used: 48160, free: 2024672"
            " No. of 1-blocks: 680, 2-blocks: 80, max blk sz: 91, max free sz: 63271"
            "GC memory layout; from 7f3795121f00:"
        ]
        frame = HeapFrame(1234, heap)
        print("test unix")
        print("\n".join(frame.heap))

    def test_device(self):
        heap = [
            "stack: 668 out of 15360"
            "GC: total: 152512, used: 1264, free: 151248",
            " No. of 1-blocks: 24, 2-blocks: 3, max blk sz: 18, max free sz: 9440",
            "GC memory layout; from 20006c30:"
        ]
        frame = HeapFrame(4321, heap)
        print("test device")
        print("\n".join(frame.heap))


# Other tests

# - Ensure blank lines are stripped
# - Ensure LogFrames are generated for inital lines (preceeding @@@ lines)
# - Check each of the frame types
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
            "stack: 668 out of 15360" "GC: total: 152512, used: 1264, free: 151248",
            " No. of 1-blocks: 24, 2-blocks: 3, max blk sz: 18, max free sz: 9440",
            "GC memory layout; from 20006c30:",
        ]
        frame = HeapFrame(4321, heap)
        print("test device")
        print("\n".join(frame.heap))


# Other tests

# - Ensure blank lines are stripped
# - Ensure LogFrames are generated for initial lines (preceding @@@ lines)
# - Check each of the frame types


two_frames = """
Installing logging (latest) from https://micropython.org/pi/v2 to /root/.micropython/lib
Copying: /root/.micropython/lib/logging.mpy
Done
INFO:MemTest:Begin Example 1
INFO:MemTest:Periodically, allocate bytearray blocks and store them in a list. At a slower interval, delete half of the list recover the memory.
@@@ 45828774 (2024, 9, 10, 12, 5, 42, 1, 254)
@@@ 45828774
mem: total=77932, current=44073, peak=44073
stack: 7328 out of 80000
GC: total: 296448, used: 49920, free: 246528
 No. of 1-blocks: 695, 2-blocks: 83, max blk sz: 91, max free sz: 7704
GC memory layout; from 7f2951dbdde0:
00000000: MDhh=hhLhhSh===h========hhhBMDhBShThSBBMDh==BShBDBDBBBhBhBBBBh==
00000800: =h===T==B==BBBTB=BBBT=B=h=h========MDShhSh========hhShMhShh==hhS
00001000: SDSh=BMDBShhhh==ShDhShLhh=LLhShSh=LhT=AhDhh=====================
00001800: ================================================================
00002000: =====h=============TSSSh=hhLhShShShShhSSLhShShSh=SSLhShSh=Shh=SS
00002800: LhShShShhShSLhShShShh=SSLhShSh=ShhSSSLhShShhSSLhShShShhSSLLhShSh
00003000: Shh=SSLhShShh====hShShhShhShSh==hSh=ShShhhSSSh=hhThh=hSSTDBMDhDS
00003800: h=hhALhShShShLhShShLhT=AhDhh====================================
00004000: ======================================================h=========
00004800: ====TSSSh=hhLhShShShShhSSLhShShSh=SSLhShSh=Shh=SSLhShShShhShSLhS
00005000: hShShh=SSLhShSh=Shh=SSLhShShhSSLhShShShhShSSLhShShhSSLhShShh====
00005800: hh=h==SShT==hShSShhThShhShSShhThShhSh===hhhBTT=Dh=BDBDhTh===BDhT
00006000: h===hhhTB=BBBBBhh=hh==h===DSShhh===h===BBBBBBBBhhh===BTh=B=BhBDB
00006800: BBBBhhh=h====TB=BBhhh=hDDBBBBh===h====hhh===============Bh===Sh=
00007000: h=====h==============hSShDTh======hh====h===========h===h===h===
00007800: ===h===h==hh===h============================h=Sh====hhh=========
00008000: ==============h=========h==hhh=h=hhhhhhhhhhhh=hh=hhhh=hhh=hh=hhh
00008800: hh=hh=hhhh=hh==hhh==h===h=hhhhhhhh===hhhhhhhhhhhh===hhhhhhh=hhhh
00009000: hhhhhhhhhhhh=hhhh====hhh==DBDBBh=DBTB=BBBBDh===BBBBBBBBBT==hBTh=
00009800: ==h===B=hTBBh==h===DhBTB=hh=hTh===BDBTB=BBBh==h===DBTB=BBBBBBBBD
0000a000: hB=BBh===TB=h========B==hhhh===hBBTTh==================hhhB=BDBB
0000a800: Lh=h====hLhLhhhh=LhhhTh=hh=Th=hTh=h=hhh===Th===h===h=h========h=
0000b000: ==hh=Thhh=h==h=hh=hh=h======h==h=hMFhDBFFFDShh===h==hSFFFDh=====
0000b800: =========h==Sh====h====ShTBBTh=DhTDhBhh=h===h===h=h=============
0000c000: =====hhBh=BLhh=h=T==hT==........................................
       (119 lines all free)
00048000: ................................................
@@@
INFO:MemTest:Allocating 5000 bytes
INFO:MemTest:Freeing half of the allocated bytearrays
INFO:MemTest:Allocating 5000 bytes
INFO:MemTest:Allocating 5000 bytes
INFO:MemTest:Allocating 5000 bytes
@@@ 45829127
mem: total=102737, current=66214, peak=66358
stack: 7328 out of 80000
GC: total: 296448, used: 46112, free: 250336
 No. of 1-blocks: 324, 2-blocks: 56, max blk sz: 157, max free sz: 7209
GC memory layout; from 7f2951dbdde0:
00000000: MDhh=hhLhhSh===h========hhhBMDhFShShhBBMDShAFShFDBDBBBhBhBBBBh==
00000800: =h===FDSB==BBBSB=BBBh=B=h=h========MDh=hFh========hhSSMhShAFh==F
00001000: ShSAFBMDFShhhDh==SDSShLhh=Lh====================================
00001800: ================================================================
00002000: ========================================================h=h=h...
00002800: ..FFFDh==Sh=h=S.................................................
00003000: .........................hShS...h.......................TDBMDh..
00003800: ..h......................D......................................
00004000: ................................................................
00004800: ....................Sh.......Sh.......Sh...Sh......Sh..Sh......S
00005000: h..Sh......Sh...Sh......Sh.......Sh..Sh..h....Sh.......Sh..h====
00005800: ...h==.........................................Dh=.D.Dh.h===.Dh.
00006000: h===hhh.B=BBB.Bh..hh==h===DSShh....h===BBBBBBBBhhh===B.h=B=Bh.DB
00006800: BBBBhhh=h====.B=BBhhh=hDDBBBBh===h====..h===============.h===Sh=
00007000: h=====h==============.SShD.h======hh====h===========h===h===h===
00007800: ===h===h==hh===h============================h=S.................
00008000: ........................h==......h.h.h.h.h.....h=.h.h=.....h=.h.
00008800: ....h=.h.h=.h==.........h=.h.h.h.h===.h.h.h.h.h.h===.h.h..h=.h.h
00009000: .h.h.h.h.h.h=.h.h====..h==D.D.Bh=DB.B=BBB.Dh===BBBBBBBBB...hB.h=
00009800: ==h===B=h..Bh==h===DhB.B=hh=h.h===.DB.B=B.Bh==h===DB.B=BBBBBBBBD
0000a000: hB=BBh===.B=h========B==hhhh===..B..h==================...B=.DBB
0000a800: .h=h====hLhLhh.h=Lhhh.h=hh=.h=hTh=h=h.h===Th===h===h=h========..
0000b000: ..h..Thh..h==h=hh=hh=h======h==h=hM.hD.......h===...............
0000b800: ........................h.B..h=DhTDhBhh=h===h===h=h=============
0000c000: =====hhBh=.Lhh=h=............A.hF...............h===============
0000c800: ================================================================
0000d000: ================================================================
0000d800: =============h==================================================
0000e000: ================================================================
0000e800: ==========================================h=====================
0000f000: ================================================================
0000f800: ================================================================
00010000: =======.........................................................
       (111 lines all free)
00048000: ................................................
@@@
"""

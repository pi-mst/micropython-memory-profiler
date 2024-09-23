# MIT license; Copyright (c) 2024, Planet Innovation
# SPDX-License-Identifier: MIT
# 436 Elgar Road, Box Hill, 3128, VIC, Australia
# Phone: +61 3 9945 7510

import time
import micropython

_MEM_DUMP_PERIOD_MS = 350
_FIRST = True


def mem_dump(_):
    global _FIRST
    if _FIRST:
        # Print ticks_ms/RTC synchronisation values, and do initial memory dump.
        # Unix supplies an extra - ninth - item (for dst). Restrict to 8
        # elements.
        print("@@@", time.ticks_ms(), time.localtime()[:8])
        _FIRST = False
    print("@@@", time.ticks_ms())
    micropython.mem_info(1)
    print("@@@")


def start_timer(period_ms=_MEM_DUMP_PERIOD_MS):
    from machine import Timer

    # Start a timer to periodically dump the heap.
    Timer(period=period_ms, callback=mem_dump)


async def start_async(period_ms=_MEM_DUMP_PERIOD_MS):
    import asyncio

    # Start a background asyncio task to periodically dump the heap.
    async def _mem_dump_task():
        while True:
            mem_dump(True)
            await asyncio.sleep_ms(period_ms)

    asyncio.create_task(_mem_dump_task())

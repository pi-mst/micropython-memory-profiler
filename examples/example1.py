# MIT license; Copyright (c) 2024, Planet Innovation
# SPDX-License-Identifier: MIT
# 436 Elgar Road, Box Hill, 3128, VIC, Australia
# Phone: +61 3 9945 7510

# Create an async program with a number of tasks:
#
#   1) allocate large blocks
#   2) de-allocate blocks, call gc.collect
#   3) profile

import asyncio
import time
import logging
import gc

import mem_dump

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("MemTest")

_MEMORY = []


class SimpleTimer:
    """A simple class that, when called, will return True if the time since
    it's creation has expired."""

    def __init__(self, seconds):
        self.start = int(time.time())
        self.seconds = seconds

    def __call__(self) -> bool:
        return (int(time.time()) - self.start) > self.seconds


async def allocate_task(finished, size_alloc=5_000, interval_ms=100):
    while not finished():
        log.info(f"Allocating {size_alloc} bytes")
        _MEMORY.append(bytearray(size_alloc))
        await asyncio.sleep_ms(interval_ms)


async def release_task(finished, interval_ms=2_000):
    while not finished():
        log.info("Freeing half of the allocated bytearrays")

        del _MEMORY[: len(_MEMORY) // 2]
        gc.collect()

        await asyncio.sleep_ms(interval_ms)


async def main():
    # Start the mem_dump async task
    await mem_dump.start_async()

    log.info("Begin Example 1")
    log.info(
        "Periodically, allocate bytearray blocks and store them in a list. "
        "At a slower interval, delete half of the list recover the memory."
    )

    # Run the example for ten seconds
    timer = SimpleTimer(10)

    # Start allocating and deleting memory
    await asyncio.gather(allocate_task(timer), release_task(timer))

    log.info("End Example 1")


asyncio.run(main())

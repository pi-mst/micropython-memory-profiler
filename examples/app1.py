# Create an async program with a number of tasks:
# 
#   1) allocate large blocks
#   2) de-allocate blocks, call gc.collect
#   3) profile

import asyncio
import time
import logging

import mem_dump

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("MemTest")

_MEMORY = []


class SimpleTimer:
    def __init__(self, seconds):
        self.start = int(time.time())
        self.seconds = seconds

    def __call__(self) -> bool:
        return (int(time.time()) - self.start) > self.seconds

async def allocate_task(finished):
    while not finished():
        log.info("Allocating")
        _MEMORY.append(bytearray(5000))
        await asyncio.sleep(1)

async def release_task(finished):
    while not finished():
        print("release")
        await asyncio.sleep(2)

log.info("starting")

async def main():
    await mem_dump.start_async()
    timer = SimpleTimer(10)
    await asyncio.gather(allocate_task(timer), release_task(timer))
    print("done")

asyncio.run(main())
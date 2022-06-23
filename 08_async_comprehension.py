import asyncio
from collections import AsyncIterable

from delay_request import delay_request

# The underlying misunderstanding is expecting async for to automatically parallelize the iteration.
# Async list comprehension allows for iteration over an async source. It does not automatically make whatever is
# going on in that source happen concurrently. If you really want to see what is happening here, remove the async
# keyword in the comprehension and watch it fail!

# https://realpython.com/async-io-python/#other-features-async-for-and-async-generators-comprehensions


async def delay_request_countdown(num: int) -> AsyncIterable:
    """
    Uses a while loop to make a request the number of times supplied to the coroutine.
    For each iteration, yield the result after it has been awaited.
    """
    i = 0
    while i < num:
        result = await delay_request(num + i)
        yield result
        i += 1


async def main() -> None:
    """
    Use async list comprehension. This will execute syncronously, but wouldnt be possible if it wasnt for
    the async keyword.
    """
    comprehended = [i async for i in delay_request_countdown(3)]
    for item in comprehended:
        print(item)


if __name__ == "__main__":
    asyncio.run(main())

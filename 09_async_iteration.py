import asyncio
from collections import AsyncIterable

from delay_request import delay_request

# Same example as 08_async_comprehension, but without using async list comphension.
# If you want to see qhy the 'async for' is important, remove the async in the main function and try and run without


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
    """This will run syncronously"""
    async for item in delay_request_countdown(3):
        print(item)


if __name__ == "__main__":
    asyncio.run(main())

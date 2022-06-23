import asyncio
from delay_request import delay_request

# Like gather, runs an iterable of awaitables concurrently, but also returns an iterable
# Each coroutine returned can be awaited to get the earliest next result
# Can have a timeout!
# https://docs.python.org/3/library/asyncio-task.html#asyncio.as_completed


async def main():
    """
    Prints the values of the requests 'as they come in'
    """
    for resp in asyncio.as_completed(
        [delay_request(7), delay_request(4), delay_request(2)]
    ):
        value = await resp
        print(value)


if __name__ == "__main__":
    asyncio.run(main())

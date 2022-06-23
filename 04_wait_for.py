import asyncio

from delay_request import delay_request

# https://docs.python.org/3/library/asyncio-task.html#timeouts
# https://docs.python.org/3/library/asyncio-task.html#asyncio.wait_for

# When you have an awaitable, but also a limit to how long you want to wait. Use this with a timeout...
# Gotcha = wait for itself HAS to be awaited


async def main() -> None:
    """
    Delay request will run for 4 seconds, timeout is 3. This will raise a TimeoutError
    """
    try:
        await asyncio.wait_for(delay_request(4), timeout=3.0)
    except asyncio.TimeoutError:
        print("This is a timeout")


asyncio.run(main())

if __name__ == "__main__":
    asyncio.run(main())

import asyncio
import aiohttp

import time

# Re-writing our delay_request function to use the AIOHttp Library, which demonstrates aync context manangers
# https://docs.aiohttp.org/en/stable/


async def delay_request(number: int) -> str:
    """
    Make a request where we will await the response for the number of seconds passed into the coroutine.
    Returns the url, as recorded by the service's response.
    """
    async with aiohttp.ClientSession() as session:
        print(f"firing off request for {number} seconds")
        async with session.get(f"https://httpbin.org/delay/{number}") as resp:
            result = await resp.json(content_type=None)
            print(f"recieved result for {number} seconds")
            return result["url"]


async def main() -> None:
    """
    Use gather to run three different calls to delay_request concurrently. Notice that despite 9 seconds of 'wait'
    time on the network calls, the whole programs finishes in  < 5 seconds, due the the different tasks being run
    in an interleaved manner.
    """
    start = time.time()
    res_1, res_2, res_3 = await asyncio.gather(
        delay_request(2),
        delay_request(3),
        delay_request(4),
    )
    end = time.time()
    print(end - start)
    print(res_1)
    print(res_2)
    print(res_3)


if __name__ == "__main__":
    asyncio.run(main())

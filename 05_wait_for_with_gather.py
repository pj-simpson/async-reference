import asyncio

from delay_request import delay_request

# According to the below (excellent) article. It's common to wrap gather in wait_for, as a workaround for the fact
# gather doesnt have a timeout
# https://hynek.me/articles/waiting-in-asyncio/


async def main() -> None:
    """
    We are going to timeout after four seconds, so that the execution of the longest running delay
    will raise a timeout error, meaning all the tasks are cancelled
    """
    try:
        result_1, result_2, result_3 = await asyncio.wait_for(
            asyncio.gather(delay_request(5), delay_request(2), delay_request(3)),
            timeout=4.0,
        )
        # This will never get printed, despite 'theoretically' having the results for 2/3 requests.
        print(result_1)
        print(result_2)
    except asyncio.TimeoutError:
        print("This is a timeout")


if __name__ == "__main__":
    asyncio.run(main())

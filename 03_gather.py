import asyncio
import time

from delay_request import delay_request

# Gather is king for running tasks concurrently. We dont even have to manually use the create the tasks, as gather will
# take care of this for us!
# https://docs.python.org/3/library/asyncio-task.html#running-tasks-concurrently


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

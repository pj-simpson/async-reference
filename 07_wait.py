import asyncio
from delay_request import delay_request
import time

# Like gather, takes an iterable of awaitables, however will return two sets. The coroutines which are 'done'
# along with those that are still pending.
# A timeout here represents the number of seconds to wait before returning NOT to raise a timeout error. If the
# timeout threashold is reached, any awaitables not yet compelte will be returned as the 'pending' set
# return_when indicates when this function should return :
# FIRST_COMPLETED = The function will return when any future finishes or is cancelled.
# FIRST_EXCEPTION = The function will return when any future finishes by raising an exception.
#   - If no future raises an exception then it is equivalent to ALL_COMPLETED.
# ALL_COMPLETED = The function will return when all futures finish or are cancelled.


async def main() -> None:
    """
    Wait three requests, but return on first exception with a timeout of 5 seconds, so that the 7 second long request
    is put into the 'pending' bucket.
    Inspect the sets returned and iterate over the pending set, to await the remaining task to finish it and
    get its return value.

    """
    start = time.time()
    done, pending = await asyncio.wait(
        [delay_request(7), delay_request(4), delay_request(2)],
        timeout=5,
        return_when="FIRST_EXCEPTION",
    )
    end_of_wait = time.time()
    print(end_of_wait - start)
    # inspect the two sets returned by wait
    print(done)
    print(pending)
    # iterate over any tasks (1) which will be in pending
    for item in pending:
        # Approx 2 second wait?
        result = await (item)
        print(result)
    # iterate over and await the done awaitables (this should appear instance as they are complete)!:
    for item in done:
        result = await (item)
        print(result)
    end = time.time()
    print(end - start)


if __name__ == "__main__":
    asyncio.run(main())

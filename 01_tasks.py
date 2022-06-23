import time
import asyncio
from delay_request import delay_request

# https://stackoverflow.com/questions/62528272/what-does-asyncio-create-task-do
# https://docs.python.org/3/library/asyncio-task.html#task-object

# create_task schedules a coroutine for execution. It needs to be awaited in order to have its result obtained


async def main() -> None:
    """
    Create two tasks, await the response of one, cancel the other, more long running task. Note the total time,
    and also that we only see the 'recieved response..' print statement for the non-cancelled task.

    """
    start = time.time()
    print("creating tasks")
    task_1 = asyncio.create_task(delay_request(4))
    task_2 = asyncio.create_task(delay_request(5))
    print("awaiting the response of 1 task, cancelling the other")
    result_1 = await task_1
    task_2.cancel()
    end = time.time()
    print(end - start)
    print(result_1)


if __name__ == "__main__":
    asyncio.run(main())

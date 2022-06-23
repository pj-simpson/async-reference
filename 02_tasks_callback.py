import asyncio

# If you dont require a return value from tasks, you dont have to await them
# Synchronous callback functions can be added to tasks
# This can be handy as any uncaught exceptions are passed to the callback
# https://docs.python.org/3/library/asyncio-task.html#creating-tasks

from delay_request import delay_request


def my_callback(task) -> None:
    """
    this function prints out the name of the Task passed to it, aswell as a console message.
    """
    print(task.get_name())
    print("This is the callback after the task is done")


async def main() -> None:
    """
    create a 'background task', whose result we never await
    attach a callback for when the task is 'done'
    """
    print("creating task with callback")
    task_1 = asyncio.create_task(delay_request(4))
    task_1.add_done_callback(my_callback)
    # ensure the program runs for long enough for the task to complete
    await asyncio.sleep(5)
    print("The task and its callback have now executed")


if __name__ == "__main__":
    asyncio.run(main())

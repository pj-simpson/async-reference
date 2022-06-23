import asyncio
import aiofiles

# using the AIOFiles Library to demonstrate aync context manangers
# https://pypi.org/project/aiofiles/


async def write(number: int) -> None:
    print(f"opening file {number}")
    async with aiofiles.open(f"testing_{number}.txt", mode="w") as f:
        print(f"writing to file {number}")
        await f.write(
            """\
        Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.\
         Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat\
         Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.\
         Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.\
        """
        )
    print(f"finished with file {number}")


async def main() -> None:
    """
    Using gather to run two instances of the 'write' coroutine concurrently.
    from the print statements, you'll notice that the operations happen in an interleaved manner.
    """
    await asyncio.gather(write(1), write(2))


if __name__ == "__main__":
    asyncio.run(main())

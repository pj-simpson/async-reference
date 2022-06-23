import asyncio
from collections import AsyncIterable

from delay_request import delay_request


# This example uses gather in the generator function, this probably better demonstrates why you might use async
# iteration, than examples 08 or 09. 'async for' ensures that we are asyncronous all the wait down, as is genrally
# considered best practise


async def further_generator_example() -> AsyncIterable:
    """
    Gather three requests and run them concurrently. Create a list of their results and yield each result
    """
    res_1, res_2, res_3 = await asyncio.gather(
        delay_request(2),
        delay_request(3),
        delay_request(4),
    )
    the_list = [res_1, res_2, res_3]
    for item in the_list:
        yield item


async def main():
    """
    Prior to any yield from the generator, the gather in the generator will run, we will then async iterate over the
    results, once they are avaliable.

    """
    async for item in further_generator_example():
        print(item)


if __name__ == "__main__":
    asyncio.run(main())

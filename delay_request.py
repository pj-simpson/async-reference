from typing import Dict

import requests_async as requests

# Using the 'requests async' library to make the well known requests lib api compatible with async/await syntax
# Using Httpbin delay endpoint to have a response returned after any umber of seconds.


async def delay_request(number: int) -> str:
    """
    Make a request where we will await the response for the number of seconds passed into the coroutine.
    Returns the url, as recorded by the service's response.
    """
    print(f"firing off request for {number} sec")
    resp = await requests.get(f"https://httpbin.org/delay/{number}")
    print(f"recieved response for {number} sec")
    return resp.json()["url"]

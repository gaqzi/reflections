# from __future__ import annotations

# import asyncio
# import logging
# from collections.abc import AsyncIterator, Awaitable

# import httpx

# logging.basicConfig(level=logging.INFO)

# TIMEOUT: float = 10_000  # ms

# # We don't want to overwhelm the server.
# CONCURRENCY_LIMIT: int = 10


# async def collect_test_uuid(order_code: str) -> AsyncIterator[str]:
#     url = f"http://southernlabpartners.local.dendi-dev.com:8000/api/v2/orders/test_results/?order_code={order_code}"

#     headers = {
#         "Authorization": "Token ec2631da8b3c76300b0c0c8840a7c608a6ee8172",
#         "Content-Type": "application/json",
#     }

#     async with httpx.AsyncClient(headers=headers) as client:
#         r = await client.get(url)
#         tests = r.json()["results"].pop()["tests"]

#         for i, test in enumerate(tests):
#             if i ==0 or i == 1:
#                 continue
#             yield test["uuid"]


# async def make_request(uuid: str) -> Awaitable[None]:
#     url = f"http://southernlabpartners.local.dendi-dev.com:8000/api/v2/test_results/{uuid}/"

#     payload = {
#         "result": {
#             "submitted_datetime": "2021-11-04T12:48:52.235490",
#             "result_quantitative": 22,
#             "result_qualitative": "",
#             "result_is_expected": False,
#             "result_text": "",
#             "result_flag": "example result flag",
#             "days_incubated": None,
#             "reflex_triggered": False,
#             "unit": "mg",
#             "reference_range_string": "example reference range string updated",
#         }
#     }
#     headers = {
#         "Authorization": "Token ec2631da8b3c76300b0c0c8840a7c608a6ee8172",
#         "Content-Type": "application/json",
#     }

#     async with httpx.AsyncClient(headers=headers) as client:
#         async with asyncio.Semaphore(CONCURRENCY_LIMIT):

#             logging.info("Posting results against test %s" % uuid)  # no fstring.

#             result = await client.put(url, json=payload, timeout=TIMEOUT)
#             print()
#             print("=" * 42)
#             logging.info(result.json())
#             print("=" * 42)
#             print()


# async def main(order_code: str) -> Awaitable[None]:
#     logging.info("Collecting the test uuids from 'GET v2/orders/test_results' API")

#     tasks = []
#     async for uuid in collect_test_uuid(order_code):
#         task = asyncio.create_task(make_request(uuid))
#         tasks.append(task)

#     await asyncio.gather(*tasks)


# if __name__ == "__main__":
#     asyncio.run(main(order_code="SO22-0002746"))
# src.py
from __future__ import annotations

# import asyncio
import inspect

# In <Python 3.9, import these from the 'typing' module.
from collections.abc import Awaitable, Callable
from functools import wraps
from typing import Any


def tag(*names: str) -> Callable:
    def decorator(func: Callable) -> Callable:
        # Tagging has to happen in function definition time.
        # Othewise calling func._tags will raise AttributeError.
        func._tags = names  # type: ignore

        if inspect.iscoroutinefunction(func):

            @wraps(func)
            async def async_wrapped(*args: Any, **kwargs: Any) -> Awaitable[Any]:
                return await func(*args, **kwargs)

            return async_wrapped
        else:

            @wraps(func)
            def sync_wrapped(*args: Any, **kwargs: Any) -> Any:
                return func(*args, **kwargs)

            return sync_wrapped

    return decorator

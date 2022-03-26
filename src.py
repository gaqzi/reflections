from __future__ import annotations

# In <Python3.9, import this from the 'typing' module.
from collections.abc import Sequence

# In <Python3.10, import this from the 'typing_extensions'
# module
from typing import TypeGuard


def check_sequence_str(
    container: Sequence[object],
) -> TypeGuard[Sequence[str]]:
    """Check all objects in the container is of type str."""

    return all(isinstance(o, str) for o in container)


def concat(
    container: Sequence[object],
    sep: str = "-",
) -> str | None:
    """Concat a sequence of string with the 'sep'."""

    if check_sequence_str(container):
        return f"{sep}".join(container)


if __name__ == "__main__":
    # Mypy complains here, as it can't figure out the
    # container type.
    concat(["hello", "world"])

# # from __future__ import annotations

# # import asyncio
# # import logging
# # from collections.abc import AsyncIterator, Awaitable

# # import httpx

# # logging.basicConfig(level=logging.INFO)

# # TIMEOUT: float = 10_000  # ms

# # # We don't want to overwhelm the server.
# # CONCURRENCY_LIMIT: int = 10


# # async def collect_test_uuid(order_code: str) -> AsyncIterator[str]:
# #     url = f"http://southernlabpartners.local.dendi-dev.com:8000/api/v2/orders/test_results/?order_code={order_code}"

# #     headers = {
# #         "Authorization": "Token ec2631da8b3c76300b0c0c8840a7c608a6ee8172",
# #         "Content-Type": "application/json",
# #     }

# #     async with httpx.AsyncClient(headers=headers) as client:
# #         r = await client.get(url)
# #         tests = r.json()["results"].pop()["tests"]

# #         for i, test in enumerate(tests):
# #             if i ==0 or i == 1:
# #                 continue
# #             yield test["uuid"]


# # async def make_request(uuid: str) -> Awaitable[None]:
# #     url = f"http://southernlabpartners.local.dendi-dev.com:8000/api/v2/test_results/{uuid}/"

# #     payload = {
# #         "result": {
# #             "submitted_datetime": "2021-11-04T12:48:52.235490",
# #             "result_quantitative": 22,
# #             "result_qualitative": "",
# #             "result_is_expected": False,
# #             "result_text": "",
# #             "result_flag": "example result flag",
# #             "days_incubated": None,
# #             "reflex_triggered": False,
# #             "unit": "mg",
# #             "reference_range_string": "example reference range string updated",
# #         }
# #     }
# #     headers = {
# #         "Authorization": "Token ec2631da8b3c76300b0c0c8840a7c608a6ee8172",
# #         "Content-Type": "application/json",
# #     }

# #     async with httpx.AsyncClient(headers=headers) as client:
# #         async with asyncio.Semaphore(CONCURRENCY_LIMIT):

# #             logging.info("Posting results against test %s" % uuid)  # no fstring.

# #             result = await client.put(url, json=payload, timeout=TIMEOUT)
# #             print()
# #             print("=" * 42)
# #             logging.info(result.json())
# #             print("=" * 42)
# #             print()


# # async def main(order_code: str) -> Awaitable[None]:
# #     logging.info("Collecting the test uuids from 'GET v2/orders/test_results' API")

# #     tasks = []
# #     async for uuid in collect_test_uuid(order_code):
# #         task = asyncio.create_task(make_request(uuid))
# #         tasks.append(task)

# #     await asyncio.gather(*tasks)


# # if __name__ == "__main__":
# #     asyncio.run(main(order_code="SO22-0002746"))


# # main()
# from __future__ import annotations

# # In < Python 3.9, import this from the 'typing' module.
# from collections.abc import Generator
# from pathlib import Path

# d = {k: v for k, v in zip("smart", ["a", {"x": "b"}, "c", "d", "e"])}


# def search(d: dict, key: str, default: str | None = None) -> str | None:
#     stack = [d.items()]

#     while stack:
#         for k, v in stack[-1]:
#             if isinstance(v, dict):
#                 stack.append(v.items())
#                 break
#             elif k == key:
#                 return v
#         else:
#             stack.pop()
#     return default


# def list_files(root: str = ".") -> Generator[str, None, None]:
#     """Recursively find files in a directory."""

#     root = Path(root)

#     stack = [root.iterdir()]
#     while stack:
#         for path in stack[-1]:
#             if path.is_dir():
#                 stack.append(path.iterdir())
#                 break

#             elif path.is_file():
#                 yield str(path).split("/")[-1]
#         else:
#             stack.pop()


# g = list_files("./theme")
# for f in g:
#     print(f)


# from __future__ import annotations

# from typing import TypeGuard, TypeVar

# T = TypeVar("T", str, int, float)

# def tuple_of_lists_of_t(o: tuple[list[T], ...]) -> TypeGuard[tuple[list[T], ...]]:

#     if not isinstance(o, tuple):
#         return False

#     return all(isinstance(elem, (str, int, float)) for lst in o for elem in lst)

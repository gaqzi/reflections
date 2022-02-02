from __future__ import annotations

from typing import Generic, TypeVar, Union

T = TypeVar("T")
E = TypeVar("E", bound=Exception)


class Ok(Generic[T]):
    def __init__(self, value: T) -> None:
        self._value = value

    def ok(self) -> T:
        return self._value


class Err(Generic[E]):
    def __init__(self, e: E) -> None:
        self._e = e

    def err(self) -> E:
        return self._e


Result = Union[Ok[T], Err[E]]


def div(dividend: int, divisor: int) -> Result[int, ZeroDivisionError]:
    if divisor == 0:
        return Err(ZeroDivisionError("Zero division error occured!"))

    return Ok(dividend // divisor)


Convertible = TypeVar("Convertible", int, float, str)
IntResult = Result[int, TypeError]


def to_int(num: Convertible) -> IntResult:
    if not isinstance(num, (int, float, str)):
        return Err(TypeError("Input type is not convertible to integer."))

    return Ok(int(num))


if __name__ == "__main__":
    result = to_int(1)

    if isinstance(result, Ok):
        print(result.ok())
    else:
        print(result.err())


# from __future__ import annotations

# # In < Python 3.9, import this from the 'typing' module.
# from collections.abc import Generator
# from pathlib import Path
# from typing import Any

# d = {
#     k: v
#     for k, v in zip(
#         "smart", ["a", {"x": "b"}, "c", {"y": ["hello", "world"]}, "d", "e"]
#     )
# }


# def find_first(d: dict, key: str, default: str | None = None) -> str | None:
#     """Find the first value against a key in an arbitrarily nested
#     dictionary.
#     """
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


# def list_files(root: str = ".") -> Generator[Any, None, None] | None:
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

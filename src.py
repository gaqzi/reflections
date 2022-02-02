# """An error-handling model influenced by that used by the Rust programming language
# See https://doc.rust-lang.org/book/ch09-00-error-handling.html.
# """
# from typing import Generic, TypeVar, Union

# T = TypeVar("T")
# E = TypeVar("E", bound=Exception)


# class Ok(Generic[T]):
#     def __init__(self, value: T) -> None:
#         self._value = value

#     def ok(self) -> T:
#         return self._value


# class Err(Generic[E]):
#     def __init__(self, e: E) -> None:
#         self._e = e

#     def err(self) -> E:
#         return self._e


# Result = Union[Ok[T], Err[E]]


# def div(dividend: int, divisor: int) -> Result[int, ZeroDivisionError]:
#     if divisor == 0:
#         return Err(ZeroDivisionError("Zero division error occured!"))

#     return Ok(dividend // divisor)


# def main() -> None:
#     r = div(10, 0)
#     if isinstance(r, Ok):

#         print(r.ok())
#     else:
#         print(r.err())


# main()
from __future__ import annotations

# In < Python 3.9, import this from the 'typing' module.
from collections.abc import Generator
from pathlib import Path

d = {k: v for k, v in zip("smart", ["a", {"x": "b"}, "c", "d", "e"])}


def search(d: dict, key: str, default: str | None = None) -> str | None:
    stack = [d.items()]

    while stack:
        for k, v in stack[-1]:
            if isinstance(v, dict):
                stack.append(v.items())
                break
            elif k == key:
                return v
        else:
            stack.pop()
    return default


def list_files(root: str = ".") -> Generator[str, None, None]:
    """Recursively find files in a directory."""

    root = Path(root)

    stack = [root.iterdir()]
    while stack:
        for path in stack[-1]:
            if path.is_dir():
                stack.append(path.iterdir())
                break

            elif path.is_file():
                yield str(path).split("/")[-1]
        else:
            stack.pop()


g = list_files("./theme")
for f in g:
    print(f)

---
title: Narrowing Types with TypeGuard in Python
date: 2022-02-23
tags: Python, Types
status: draft
---

Static type checkers like Mypy follow your code flow and statically try to figure out the types of the variables without you having to explicitly annotate inline codes. For example:

```python
# src.py
from __future__ import annotations


def check(x: int | float) -> str:
    if not isinstance(x, int):
        reveal_type(x)
        # Type is now 'float'.

    else:
        reveal_type(x)
        # Type is now 'int'.

    return str(x)
```

The `reveal_type` function is provided by Mypy and you don't need to import this. If you run Mypy against this snippet, it'll print the following lines:

```
src.py:6: note: Revealed type is "builtins.float"
src.py:10: note: Revealed type is "builtins.int"
```

Here, I didn't have to explicitly tell the type checker how the conditionals narrow the type. From PEP-647:

> Static type checkers commonly employ a technique called 'type narrowing' to determine a more precise type of an expression within a program's code flow. When type narrowing is applied within a block of code based on a conditional code flow statement (such as if and while statements), the conditional expression is sometimes referred to as a 'type guard'.

So in the above snippet, Mypy performed **type narrowing** to determine the more precise type of the variable `x` and the `if ... else` conditionals, in this case, is known as **type guards**.

However, in some complex cases, the type checker can't figure out the types statically. Mypy will complain when it encounters one of these issues:

```python
from __future__ import annotations

# In <Python3.9, import this from the 'typing' module.
from collections.abc import Sequence


def check_sequence_str(container: Sequence[object]) -> bool:
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
```

Here, the `check_sequence_str` checks whether the input argument is a sequence of strings in runtime. Then in the `concat` function, I used it to check whether the input conforms to the expected type requirement; if it does, the function performs string concatenation and returns the value. Otherwise, it returns `None`. If you run, Mypy against this, it'll complain:

```
src.py:22: error: Argument 1 to "join" of "str" has incompatible type "Sequence[object]";
expected "Iterable[str]"
            return f"{sep}".join(container)
                                 ^
Found 1 error in 1 file (checked 1 source file)
```

The type checker can't figure out that the container type is `list[str]`.

Functions like `check_sequence_str` that—checks the type of an input object and returns a boolean—are called type guard functions. PEP-647 proposed a `TypeGuard` class to help the type checkers to narrow down more complex types. Python 3.10 added `TypeGuard` class to the `typing` module. You can use it like this:

```python
# src.py
...

# In <Python3.10, import this from 'typing_extensions' module.
from typing import TypeGuard


def check_sequence_str(
    container: Sequence[object],
) -> TypeGuard[Sequence[str]]:
    """Check all objects in the container is of type str."""

    return all(isinstance(o, str) for o in container)


...
```

Notice that the return type now has the expected type defined inside the `TypeGuared` generic type. Now Mypy will be satisfied if you run it against the modified snippet.

## What Makes a Function a TypeGuard Function

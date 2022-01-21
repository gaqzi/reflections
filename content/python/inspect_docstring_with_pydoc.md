---
title: Inspect Docstrings with Pydoc
date: 2022-01-22
tags: Python
---

How come I didn't know about the `python -m pydoc` command before today.

> It lets you inspect the docstrings of any modules, classes, functions, or methods in Python.

I'm running the commands from a Python 3.10 virtual environment but it'll work on any Python version. Let's print out the docstrings of the `functools.lru_cache` function. Run:


```
python -m pydoc functools.lru_cache
```

Works for third party tools as well:

```
python -m pydoc typing_extensions.ParamSpec
```

Also, works for any custom Python structure that is accessible from the current Python path. Let's define a function with docstrings and put that in a module called `src.py`:

```python
# src.py
def greetings(name: str) -> None:
    """Prints Hello <name>! on the console.

    Parameters
    ----------
    name : str
        Name of the person you want to greet
    """

    print("Hello {name}!")
```

You can inspect the entire `src.py` module or the `greetings` function specifically as follows:

To inspect the module, run:

```
python -m pydoc src
```

To inspect the `greetings` function only, run:

```
python -m pydoc src.greetings
```

It'll return:

```
Help on function greetings in src:

src.greetings = greetings(name: str) -> None
    Prints Hello <name>! on the console.

    Parameters
    ----------
    name : str
        Name of the person you want to greet
```

Instead of inspecting the docstrings one by one, you can also pull up all the docstrings in the current Python path and serve them as HTML pages. To do so, run:

```
python -m pydoc -b
```

This will render the docstrings as HTML web pages and automatically open the index page with your default browser. You can use the built-in search to find and read your desired docstring.

## References

* [Tweet by Brandon Rhodes](https://twitter.com/brandon_rhodes/status/1354416534098214914)

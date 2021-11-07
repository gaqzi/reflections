# Use Daemon Threads to Test Infinite While Loops

Python's daemon threads are cool. A Python script will stop when the main thread is done and only daemon threads are running. To test a simple `hello` function that runs indefinitely, you can do the following:


```python
# test_hello.py

import asyncio
import threading
from functools import partial
from unittest.mock import patch

import pytest


async def hello():
    while True:
        await asyncio.sleep(1)
        print("hello")


@pytest.mark.asyncio
@patch("asyncio.sleep", autospec=True)
async def test_hello(mock_asyncio_sleep, capsys):

    run = partial(asyncio.run, hello())
    t = threading.Thread(target=run, daemon=True)
    t.start()
    t.join(timeout=0.1)

    out, err = capsys.readouterr()
    assert err == ""
    assert "hello" in out
    mock_asyncio_sleep.assert_awaited()
```

To execute the script, make sure you've your virtual env actiavated. Also you'll need to install `pytest` and `pytest-asyncio`. Then run:

```
pytest test_hello -v -s
```

## Reference

* The idea came from this quora [answer](https://qr.ae/pGDHVw).

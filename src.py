import time
from functools import lru_cache
from typing import TypeVar

Number = TypeVar("Number", int, float, complex)


class SlowAdder:
    def __init__(self, delay: int = 1):
        self.delay = delay
        self.calculate = lru_cache()(self._calculate)

    def _calculate(self, *args: Number) -> Number:
        time.sleep(self.delay)
        return sum(args)

    def __del__(self) -> None:
        print("Deleting instance ...")


slow_adder = SlowAdder()
print(slow_adder.__dict__)

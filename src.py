# Placeholder python file to test the snippets
from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class ProtoFoo(Protocol):
    def bar(self) -> str:
        ...

    @classmethod
    def baz(cls) -> str:
        ...

    @property
    def qux(self) -> str:
        ...


class Foo:
    def bar(self) -> str:
        return "from instance method"

    @classmethod
    def baz(cls) -> str:
        return "from class method"

    @property
    def qux(self) -> str:
        return "from property method"


def run(foo: ProtoFoo) -> None:
    if not isinstance(foo, ProtoFoo):
        raise Exception("Foo do not conform to Protofoo interface")

    print(foo.bar())
    print(foo.baz())
    print(foo.qux)


if __name__ == "__main__":
    foo = Foo()
    run(foo)

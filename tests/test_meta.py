"""Unit tests for the ranker.meta module."""
from ranker.meta import SingletonMeta


def test_singleton__equal_ids():
    """
    Given: A class that has `SingletonMeta` as a metaclass
    When: The class is created multiple times
    Then: All instances of that class should be the same instance
    """

    class Foo(metaclass=SingletonMeta):
        ...

    assert id(Foo()) == id(Foo()) == id(Foo())


def test_singleton__set_attr():
    """
    Given:
    When:
    Then:
    """

    class Foo(metaclass=SingletonMeta):
        bar: str

    first = Foo()
    first.bar = "Baz"

    second = Foo()
    assert second.bar == "Baz"

    second.bar = "Red"
    assert first.bar == "Red"
    assert second.bar == "Red"

"""Unit tests for the ranker.meta module."""
import pytest


@pytest.fixture
def singleton():
    """Override default fixture for `singleton`"""
    from ranker.meta import SingletonMeta

    SingletonMeta._SingletonMeta__instances = {}


def test_singleton__equal_ids():
    """
    Given: A class that has `SingletonMeta` as a metaclass
    When: The class is created multiple times
    Then: All instances of that class should be the same instance
    """
    from ranker.meta import SingletonMeta

    class Foo(metaclass=SingletonMeta):
        ...

    assert id(Foo()) == id(Foo()) == id(Foo())


def test_singleton__set_attr():
    """
    Given:
    When:
    Then:
    """
    from ranker.meta import SingletonMeta

    class Foo(metaclass=SingletonMeta):
        bar: str

    first = Foo()
    first.bar = "Baz"

    second = Foo()
    assert second.bar == "Baz"

    second.bar = "Red"
    assert first.bar == "Red"
    assert second.bar == "Red"

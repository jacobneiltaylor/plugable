import abc

import pytest

import plugable


class AbstractPlugable(plugable.Plugable):
    @abc.abstractmethod
    def example(self):
        pass


class PlugableImpl1(AbstractPlugable, register="one"):
    def example(self):
        return 1


class PlugableImpl2(AbstractPlugable, register="two"):
    def example(self):
        return 2


class PlugableImplCustomInit(AbstractPlugable, register="custom"):
    def __init__(self, x, y):
        self._x = x
        self._y = y

    def example(self):
        return self._x + self._y


class PlugablePartialImpl(AbstractPlugable):
    @abc.abstractmethod
    def inner(self):
        pass

    def example(self):
        return self.inner()


class PlugableImpl3(PlugablePartialImpl, register="three"):
    def inner(self):
        return 3


@pytest.mark.parametrize(
    ("impl", "retval"),
    (("one", 1), ("two", 2), ("three", 3)),
    ids=("one", "two", "three"),
)
def test_plugable_base(impl, retval):
    assert AbstractPlugable.get(impl).example() == retval
    assert AbstractPlugable.get(impl).registered_as == impl


def test_plugable_fail():
    with pytest.raises(KeyError) as excinfo:
        AbstractPlugable.get("nonexistent")

    assert str(excinfo.value) == "'nonexistent'"


def test_plugable_class_scope():
    assert PlugablePartialImpl.get("three").example() == 3
    with pytest.raises(RuntimeError) as excinfo:
        PlugablePartialImpl.get("two")

    assert (
        str(excinfo.value)
        == f"'PlugableImpl2' isn't a subclass of 'PlugablePartialImpl'"
    )


def test_plugable_register():
    class PlugableImpl4(AbstractPlugable):
        def example(self):
            return 4

    AbstractPlugable.registry.register("four", PlugableImpl4)

    impl = AbstractPlugable.get("four")

    assert type(impl) == PlugableImpl4
    assert impl.example() == 4


def test_plugable_register_implicit():
    class PlugableImpl5(AbstractPlugable, register="five"):
        def example(self):
            return 5

    impl = AbstractPlugable.get("five")

    assert type(impl) == PlugableImpl5
    assert impl.example() == 5


def test_plugable_entrypoint():
    class Dummy1(plugable.Plugable, entrypoint="dummy"):
        @abc.abstractmethod
        def example(self):
            pass

    assert Dummy1.registry.entrypoint == "dummy"


def test_plugable_exclusive():
    class Dummy2(plugable.Plugable):
        @abc.abstractmethod
        def example(self):
            pass

    class Dummy2Subclass(Dummy2, register="dummy"):
        def example(self):
            return 666

    impls = Dummy2.registry.enum()

    assert "one" not in impls
    assert "two" not in impls
    assert "three" not in impls
    assert impls[0] == "dummy"
    assert len(impls) == 1

    impl = Dummy2.get(impls[0])

    assert type(impl) == Dummy2Subclass
    assert impl.example() == 666


def test_plugable_custom_init():
    impl = AbstractPlugable.get("custom", 4, y=6)
    assert type(impl) == PlugableImplCustomInit
    assert impl.example() == 10

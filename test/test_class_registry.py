import pytest

import plugable.class_registry as module


class Superclass:
    data = 0


class Subclass1(Superclass):
    data = 1


class Subclass2(Superclass):
    data = 2


class Subclass3(Subclass1):
    data = 3


class InvalidClass:
    data = -1


class ExternalSubclass(Subclass2):
    data = 666


_NAMES = ("class1", "class2", "class3")


def _get_entrypoints_mock(name):
    class MockEntrypoint:
        def load(self):
            def func():
                return {"class4": ExternalSubclass}.items()
            return func

    return [MockEntrypoint()]


def _get_test_reg():
    reg = module.ClassRegistry()
    reg.root_class = Superclass

    for x in [Subclass1, Subclass2, Subclass3]:
        reg.register(f"class{x.data}", x)

    return reg


def _exec_test(test):
    reg = _get_test_reg()

    for name in _NAMES:
        assert test(reg, name)


def test_registry_get():
    _exec_test(lambda x, y: x.get(y).data == int(y[-1]))


def test_registry_enum():
    _exec_test(lambda x, y: y in x.enum())


def test_registry_reg_fail():
    reg = _get_test_reg()

    with pytest.raises(TypeError) as excinfo:
        reg.register("class4",  InvalidClass)

    assert str(excinfo.value) == f"{InvalidClass} is not a subclass of {Superclass}"  # noqa: E501


def test_registry_get_fail():
    reg = _get_test_reg()

    with pytest.raises(KeyError) as excinfo:
        reg.get("class4")

    assert str(excinfo.value) == "'class4'"


def test_registry_external():
    temp = module._get_entrypoints
    module._get_entrypoints = _get_entrypoints_mock

    reg = _get_test_reg()
    reg.entrypoint = "dummy"
    reg.register_externals()
    assert reg.get("class4").data == 666

    module._get_entrypoints = temp

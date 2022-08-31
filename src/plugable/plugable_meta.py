import abc

from .class_registry import ClassRegistry


class PlugableMeta(abc.ABCMeta):
    """
    Enables the creation of abstract classes that can automatically
    discover and load their concrete implementations at runtime
    """

    REGISTRY_ATTR_NAME = "registry"
    ANCHOR_ATTR_NAME = "plugable_anchor"
    REGNAME_ATTR_NAME = "registered_name"

    @classmethod
    def _is_anchor(cls, base):
        args = (base, cls.ANCHOR_ATTR_NAME)
        return hasattr(*args) and getattr(*args)

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        namespace = {}
        registered_name = None

        if "register" in kwargs:
            registered_name = kwargs["register"]

        for base in bases:
            if cls._is_anchor(base):
                namespace[cls.ANCHOR_ATTR_NAME] = False
                namespace[cls.REGISTRY_ATTR_NAME] = ClassRegistry()
                namespace[cls.REGNAME_ATTR_NAME] = registered_name
                break

        return namespace

    def __new__(self, name, bases, dct, register=None, entrypoint=None):
        new_class = super().__new__(self, name, bases, dct)

        for base in bases:
            if self._is_anchor(base):
                new_class.registry.root_class = new_class
                new_class.registry.entrypoint = entrypoint
                break

        if register:
            new_class.registry.register(register, new_class)

        return new_class

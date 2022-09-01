import abc

from plugable.class_registry import ClassRegistry


class PlugableMeta(abc.ABCMeta):
    """
    Enables the creation of abstract classes that can automatically
    discover and load their concrete implementations at runtime
    """

    REGISTRY_ATTR_NAME = "registry"
    ANCHOR_ATTR_NAME = "plugable_anchor"
    REGNAME_ATTR_NAME = "registered_as"

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
            namespace[cls.REGNAME_ATTR_NAME] = registered_name

        for base in bases:
            if cls._is_anchor(base):
                namespace[cls.ANCHOR_ATTR_NAME] = False
                namespace[cls.REGISTRY_ATTR_NAME] = ClassRegistry()
                break

        return namespace

    def __new__(self, name, bases, dct, register=None, entrypoint=None):
        new_class = super().__new__(self, name, bases, dct)
        reg: ClassRegistry = getattr(new_class, "registry")

        for base in bases:
            if self._is_anchor(base):
                reg.root_class = new_class
                reg.entrypoint = entrypoint
                break

        if register:
            reg.register(register, new_class)

        return new_class

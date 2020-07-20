from .class_registry import ClassRegistry
from .plugable_meta import PlugableMeta


class Plugable(metaclass=PlugableMeta):
    registry = ClassRegistry()
    plugable_anchor = True

    @classmethod
    def get(cls, name, *args, **kwargs):
        instance = cls.registry.get(name, *args, **kwargs)
        if isinstance(instance, cls):
            return instance
        inst_name = type(instance).__name__
        cls_name = cls.__name__
        raise RuntimeError(f"'{inst_name}' isn't a subclass of '{cls_name}'")


__all__ = [
    "Plugable"
]

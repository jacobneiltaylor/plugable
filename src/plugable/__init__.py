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


__all__ = [
    "Plugable"
]

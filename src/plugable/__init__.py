from .class_registry import ClassRegistry
from .plugable_meta import PlugableMeta


class Plugable(metaclass=PlugableMeta):
    registry = ClassRegistry()
    plugable_anchor = True

    @classmethod
    def get(cls, name, *args, **kwargs):
        return cls.registry.get(name, *args, **kwargs)


__all__ = [
    "Plugable"
]

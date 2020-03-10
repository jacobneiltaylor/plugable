import pkg_resources


def _get_entrypoints(name):
    return pkg_resources.iter_entry_points(name)


class ClassRegistry:
    """
        Represents a collection of classes that implement a
        given interface (specified by root_class)
    """
    def __init__(self):
        self.root_class = None
        self.entrypoint = None
        self._registry = {}

    def register(self, name: str, subcls):
        if issubclass(subcls, self.root_class):
            self._registry[name] = subcls
        else:
            raise TypeError(f"{subcls} is not a subclass of {self.root_class}")

    def enum(self) -> list:
        return list(self._registry.keys())

    def get(self, name, *args, **kwargs):
        return self._registry[name](*args, **kwargs)

    def register_externals(self):
        for entrypoint in _get_entrypoints(self.entrypoint):
            for name, subcls in entrypoint.load()():
                self.register(name, subcls)

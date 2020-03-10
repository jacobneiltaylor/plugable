# Plugable: A Python Plugin Framework

This package exposes a framework for writing extensible applications.

Specifically, it allows consumers to mark an abstract class as "Plugable", using standard inheritance semantics and ABC decorators:

```python3
from abc import abstractmethod
from plugable import Plugable

class AbstractInterface(Plugable):
    @abstractmethod
    def example(self):
        pass
```

Following this, you can create subclasses for differing implementations, and register them with the `AbstractInterface` registry, like so:

```python3
class ExampleOne(AbstractInterface, register="one"): # Integrated registration
    def example(self):
        print("You ran ExampleOne!")

class ExampleTwo(AbstractInterface):
    def example(self):
        print("You ran ExampleTwo!")

AbstractInterface.registry.register("two", ExampleTwo) # Explicit registration
```

Finally, you can access and consume the registered implementations, like so:

```python3
AbstractInterface.get("one").example()  # You ran ExampleOne!
AbstractInterface.get("two").example()  # You ran ExampleTwo!
```


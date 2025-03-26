from pyscript import Event
from pyscript.web import div, page, when


class App:
    def __init__(self, components=None):
        self._components = components or []

    def add_component(self, component):
        self._components.append(component)

    def run(self):
        page.append(
            div(children=[component._element for component in self._components])
        )
        for component in self._components:
            component._finish()


_registered_handlers = {}


def on(attr_name: str, event="event"):
    def decorator(method):
        _registered_handlers[method] = (attr_name, event)
        return method

    return decorator


class Component:
    @property
    def id(self):
        """A unique string identifier for the component."""
        return f"{self.__class__.__name__}-{hash(self)}"

    @property
    def selector(self):
        """A CSS query selector for the component by its ID."""
        return f"#{self.id}"

    def draw(self):
        return None

    def _finish(self):
        for method_name, method in self.__class__.__dict__.items():
            # Check whether any of the class's methods are in the registry.
            # Use the instance of the method instead of name since the function
            # object should be unique.
            try:
                (attr_name, event) = _registered_handlers[method]
            except (KeyError, TypeError):
                continue  # Wasn't registered, skip to next

            # Split the watched event name, making sure it starts with self
            attrs = attr_name.split(".")
            if attrs[0] != "self":
                continue

            # Traverse the nested attributes to get the attribute value and its parent
            obj = self
            parent = None
            for a in attrs[1:]:
                parent = obj
                obj = getattr(obj, a)

            # Get the bound method
            func = getattr(self, method.__name__)

            # Assign the event listener
            if event == "event":
                # The value is an Event object
                when(obj)(func)
            elif event == "changed":
                # The value will be derived from the State descriptor
                # We need the parent to access the actual descriptor object
                assert parent is not None
                descriptor_name = attrs[-1]
                descriptor = getattr(parent.__class__, descriptor_name, None)
                event_obj = descriptor.get_event(parent)
                when(event_obj)(func)
            elif event == "click":
                when("click", self.selector)(func)
            else:
                raise ValueError(f"Unimplemented event type {event}")

        self.draw()


class Input:
    def __init__(self, default=None):
        self._default = default
        self._instance_values = {}

    def __get__(self, instance, _):
        return self._instance_values.setdefault(instance, self._default)

    def __set__(self, instance, value):
        self._instance_values[instance] = value


class State(Input):
    def __init__(self, default=None):
        super().__init__(default=default)
        self._changed_events = {}

    def get_event(self, instance):
        return self._changed_events.setdefault(instance, Event())

    def __set__(self, instance, value):
        super().__set__(instance, value)

        event = self.get_event(instance)
        event.trigger(value)

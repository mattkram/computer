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


class Switch:
    def __init__(self):
        self.is_open = True
        self.state_changed = Event()

        self._id = f"{self.__class__.__name__}-{hash(self)}"
        self._element = div(
            div(
                div(className="circuit-line circuit-line-left"),
                div(className="circuit-line circuit-line-right"),
                div(className="switch-base"),
                div(className="switch-lever"),
                div(className="status", id=f"{self._id}-status"),
                id=f"{self._id}-switch",
                className="switch",
            ),
            className="switch-container",
            id=self._id,
        )

    def on_click(self, e=None):
        self.is_open = not self.is_open
        self.state_changed.trigger(None)

    def draw(self, e=None):
        switch_element = page[f"#{self._id}-switch"]
        status_element = page[f"#{self._id}-status"]

        if self.is_open:
            switch_element.classes.add("open")
            switch_element.classes.remove("closed")
            status_element.textContent = "OPEN"
        else:
            switch_element.classes.add("closed")
            switch_element.classes.remove("open")
            status_element.textContent = "CLOSED"

    def _finish(self):
        # Late bind the click event handler
        when("click", f"#{self._id}")(self.on_click)
        when(self.state_changed)(self.draw)
        self.draw()


class Light:
    def __init__(self, input):
        self.input = input

        self.is_on = False
        self.state_changed = Event()

        self._element = div(className="lightbulb", id="my-div")

    def on_input_state_changed(self, e=None):
        # Toggle the light state
        self.is_on = not self.is_on
        self.state_changed.trigger(None)

    def draw(self):
        if self.is_on:
            self._element.classes.add("on")
        else:
            self._element.classes.remove("on")

    def _finish(self):
        when(self.input.state_changed)(self.on_input_state_changed)
        when(self.state_changed)(self.draw)
        self.draw()


# Compose the UI
app = App()

# Make two independent switches
for i in range(2):
    switch = Switch()
    light = Light(input=switch)
    app.add_component(switch)
    app.add_component(light)

app.run()

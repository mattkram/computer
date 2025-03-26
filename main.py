from pyscript.web import div, page

from app import App, Component, State, on


class Switch(Component):
    is_open = State(default=True)

    def __init__(self):
        self._element = div(
            div(
                div(className="circuit-line circuit-line-left"),
                div(className="circuit-line circuit-line-right"),
                div(className="switch-base"),
                div(className="switch-lever"),
                div(className="status", id=f"{self.id}-status"),
                id=f"{self.id}-switch",
                className="switch",
            ),
            className="switch-container",
            id=self.id,
        )

    @on("self._element", event="click")
    def on_click(self, e=None):
        self.is_open = not self.is_open

    @on("self.is_open", event="changed")
    def draw(self, e=None):
        switch_element = page[f"{self.selector}-switch"]
        status_element = page[f"{self.selector}-status"]

        if self.is_open:
            switch_element.classes.add("open")
            switch_element.classes.remove("closed")
            status_element.textContent = "OPEN"
        else:
            switch_element.classes.add("closed")
            switch_element.classes.remove("open")
            status_element.textContent = "CLOSED"


class Light(Component):
    is_on = State(default=False)

    def __init__(self, input):
        super().__init__()
        self.input = input

        self._element = div(className="lightbulb", id=self.id)

    @on("self.input.is_open", event="changed")
    def on_input_state_changed(self, e=None):
        # Toggle the light state
        self.is_on = not self.is_on

    @on("self.is_on", event="changed")
    def draw(self):
        if self.is_on:
            self._element.classes.add("on")
        else:
            self._element.classes.remove("on")


# Compose the UI
app = App()

# Make two independent switches
for i in range(2):
    switch = Switch()
    light = Light(input=switch)
    app.add_component(switch)
    app.add_component(light)

app.run()

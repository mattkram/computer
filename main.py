from pyscript.web import div, page

from app import App, Component, Input, State, on


class Switch(Component):
    is_open = State(default=True)

    __css_class__ = "switch-container"

    @property
    def children(self):
        return div(
            div(className="circuit-line circuit-line-left"),
            div(className="circuit-line circuit-line-right"),
            div(className="switch-base"),
            div(className="switch-lever"),
            div(className="status", id=f"{self.id}-status"),
            id=f"{self.id}-switch",
            className="switch",
        )

    @on("self.element", event="click")
    def toggle_state(self):
        self.is_open = not self.is_open

    @on("self.is_open")
    def draw(self):
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
    input = Input()
    is_on = State(default=False)

    __css_class__ = "lightbulb"

    @on("self.input.is_open")
    def toggle_state(self):
        self.is_on = not self.is_on

    @on("self.is_on")
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

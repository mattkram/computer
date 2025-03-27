import asyncio
from random import random

from pyscript.web import div, page, p

from app import App, Component, Input, State, on


class Switch(Component):
    clock = Input()
    react_to_clock = Input(default=False)

    x = State(default_factory=random)
    y = State(default_factory=random)

    is_open = State(default=True)

    __css_class__ = "switch-container"
    __style__ = {"position": "absolute"}

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

    @on(event="click")
    def toggle_state(self):
        self.is_open = not self.is_open

    @on("self.clock.num_cycles")
    def on_clock_cycle(self):
        if self.react_to_clock and random() >= 0.5:
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

    @on("self.x")
    def update_x_position(self):
        print(f"Setting x position to {self.x=}")
        self.element.style["left"] = f"{self.x * 90}%"

    @on("self.y")
    def update_y_position(self):
        print(f"Setting y position to {self.y=}")
        self.element.style["top"] = f"{self.y * 90}%"


class Light(Component):
    input = Input()

    x = State(default_factory=random)
    y = State(default_factory=random)

    is_on = State(default=False)

    __style__ = {"position": "absolute"}
    __css_class__ = "lightbulb"

    @on("self.input.is_open")
    def toggle_state(self):
        # This is a bug. We toggle the light every time switch state is set.
        # Instead, we need to read self.input.is_open and derive self.is_on
        # from that.
        self.is_on = not self.is_on

    @on("self.is_on")
    def draw(self):
        if self.is_on:
            self._element.classes.add("on")
        else:
            self._element.classes.remove("on")

    @on("self.x")
    def update_x_position(self):
        print(f"Setting x position to {self.x=}")
        self.element.style["left"] = f"{self.x * 90}%"

    @on("self.y")
    def update_y_position(self):
        print(f"Setting y position to {self.y=}")
        self.element.style["top"] = f"{self.y * 90}%"


class Clock(Component):
    num_cycles = State(default=0)

    __css_class__ = "clock"

    @property
    def children(self):
        return p("", id="clock-text")

    def run(self):
        async def timer_loop():
            while True:
                await asyncio.sleep(1)
                self.num_cycles += 1

        asyncio.ensure_future(timer_loop())

    @on("self.num_cycles")
    def draw(self):
        text_element = page["#clock-text"]
        text_element.innerHTML = f"Cycle count: {self.num_cycles}"


# Compose the UI
app = App(className="canvas")

# Create the clock
clock = Clock()
app.add_component(clock)

# Make two independent switches
for i in range(5):
    y = 0.2 * i + 0.05
    switch = Switch(x=0.1, y=y, clock=clock)
    light = Light(input=switch, x=0.5, y=y, clock=clock)

    # Make the second switch randomly toggle
    switch.react_to_clock = True

    app.add_component(switch)
    app.add_component(light)

clock.run()
app.run()

# This is a hack for a bug. For some reason, the positions don't get set when the app runs.
for component in app._components:
    try:
        component.x = component.x
        component.y = component.y
    except AttributeError:
        pass

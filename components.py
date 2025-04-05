import asyncio
from random import random

from pyscript.web import div, page, p, span

from app import Component, Input, State, on


class Switch(Component):
    clock = Input()
    react_to_clock = Input(default=False)

    x = State(default_factory=random)
    y = State(default_factory=random)

    is_open = State(default=True)
    output = State(default=0)

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
        if self.react_to_clock and random() >= 0.8:
            self.is_open = not self.is_open

    @on("self.is_open")
    def draw(self):
        switch_element = page[f"{self.selector}-switch"]
        status_element = page[f"{self.selector}-status"]

        if self.is_open:
            self.output = 0
            switch_element.classes.add("open")
            switch_element.classes.remove("closed")
            status_element.textContent = "OPEN"
        else:
            self.output = 1
            switch_element.classes.add("closed")
            switch_element.classes.remove("open")
            status_element.textContent = "CLOSED"

    @on("self.x")
    def update_x_position(self):
        self.element.style["left"] = f"{self.x * 90}%"

    @on("self.y")
    def update_y_position(self):
        self.element.style["top"] = f"{self.y * 90}%"

    count = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.svg_id = f"switch-{self.count}"
        Switch.count += 1

    # @on("self.is_open")
    # def draw_on_svg(self):
    #     svg_object = page["#my-svg-object"]
    #
    #     # It's a list and not indexing freezes the thread
    #     svg_doc = svg_object.contentDocument[0]
    #
    #     switch_element = svg_doc.getElementById(self.svg_id)
    #     if switch_element is None:
    #         return
    #
    #     if self.is_open:
    #         switch_element.classList.add("open")
    #         switch_element.classList.remove("closed")
    #     else:
    #         switch_element.classList.add("closed")
    #         switch_element.classList.remove("open")


class Light(Component):
    input = Input()

    x = State(default_factory=random)
    y = State(default_factory=random)

    is_on = State(default=False)

    __style__ = {"position": "absolute"}
    __css_class__ = "lightbulb"

    @on("self.input.output")
    def toggle_state(self):
        self.is_on = bool(self.input.output)

    @on("self.is_on")
    def draw(self):
        if self.is_on:
            self._element.classes.add("on")
        else:
            self._element.classes.remove("on")

    count = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.svg_id = f"circuit-node-{self.count}"
        Light.count += 1

    # @on("self.is_on")
    # def draw_node_color(self):
    #     svg_object = page["#my-svg-object"]
    #
    #     # It's a list and not indexing freezes the thread
    #     svg_doc = svg_object.contentDocument[0]
    #
    #     circle = svg_doc.getElementById(self.svg_id)
    #     if circle is None:
    #         return
    #
    #     if self.is_on:
    #         circle.style.fill = "red"
    #     else:
    #         circle.style.fill = "black"
    #
    #     bulb = svg_doc.getElementById(self.svg_id.replace("circuit-node", "lightbulb"))
    #     if bulb:
    #         if self.is_on:
    #             bulb.classList.add("on")
    #         else:
    #             bulb.classList.remove("on")

    @on("self.x")
    def update_x_position(self):
        self.element.style["left"] = f"{self.x * 90}%"

    @on("self.y")
    def update_y_position(self):
        self.element.style["top"] = f"{self.y * 90}%"


class Clock(Component):
    clock_rate = State(default=1)
    num_cycles = State(default=0)

    __css_class__ = "clock"

    @property
    def children(self):
        return [
            p("Cycle count: ", span(id="cycle-count")),
            p("Clock rate (Hz): ", span(id="clock-rate")),
        ]

    def run(self):
        async def timer_loop():
            while True:
                await asyncio.sleep(1 / self.clock_rate)
                self.num_cycles += 1

        asyncio.ensure_future(timer_loop())

    @on("self.num_cycles")
    def draw(self):
        page["#cycle-count"].innerHTML = self.num_cycles
        page["#clock-rate"].innerHTML = self.clock_rate

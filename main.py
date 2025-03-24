from pyscript import Event
from pyscript.web import button, div, page, when


class Switch:
    def __init__(self):
        self.is_open = True

        self.state_changed = Event()
        self._id = f"switch-{hash(self)}"
        self._element = button(id=self._id)
        self.on_state_changed()

    def on_click(self, e=None):
        self.is_open = not self.is_open
        self.state_changed.trigger(None)

    def on_state_changed(self, e=None):
        state = "open" if self.is_open else "closed"
        self._element.innerHTML = f"The switch is {state}"

    def finish(self):
        # Late bind the click event handler
        when("click", f"#{self._id}")(self.on_click)
        when(self.state_changed)(self.on_state_changed)


class Light:
    def __init__(self):
        self.is_on = False
        self._element = div(className="lightbulb", id="my-div")

    def light(self, e=None):
        # Toggle the light state
        self.is_on = not self.is_on
        self._element.classList.toggle("on")

    def finish(self):
        when(switch.state_changed)(self.light)


# Compose the UI
light = Light()
switch = Switch()

page.append(
    switch._element,
    light._element,
)

switch.finish()
light.finish()

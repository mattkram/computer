from app import App

from components import Switch, Clock, Light

# Compose the UI
app = App(className="canvas")

# Create the clock
clock = Clock(clock_rate=2)
app.add_component(clock)

# Make two independent switches
for i in range(4):
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

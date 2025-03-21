from pyscript import Event
from pyscript.web import button, div, page, when

button_was_clicked = Event()
times_clicked = 0
light_is_on = False

page.append(
    button(f"Clicked {times_clicked} times", id="my-button"),
    div("The light is off!", id="my-div"),
)


@when("click", "#my-button")
def switch(e):
    global times_clicked

    times_clicked += 1
    e.target.innerHTML = f"Clicked {times_clicked} times"
    button_was_clicked.trigger(result="Hi")


@when(button_was_clicked)
def light(e):
    global light_is_on

    # Toggle the light state
    light_is_on = not light_is_on

    state = "on" if light_is_on else "off"
    text = f"The light is {state}!"
    page["#my-div"].innerHTML = text

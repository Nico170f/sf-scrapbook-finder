from pynput.mouse import Controller, Listener, Button

mousePositionCoords: list[tuple[int, int]] = []

# https://pythonhosted.org/pynput/mouse.html#controlling-the-mouse


def getMousePosition(self) -> list[tuple[int, int]]:
    mousePositionCoords.clear()
    # mouse = Controller()

    def on_click(x, y, button, pressed):
        # print('------------', x, y)

        if button == Button.middle:
            return False

        if not validateMouseButton(button):
            return

        if not pressed:
            return

        if not validateMousePosition(x, y):
            print("Invalid mouse position. The selection has been reset.")
            self.printMouseInstruction()
            mousePositionCoords.clear()
            return

        mousePositionCoords.append((x, y))
        print(f'First selection has been saved ({x}, {y})')

        if len(mousePositionCoords) == 2:
            return False

    with Listener(
            on_click=on_click) as listener:
        listener.join()

    return mousePositionCoords


def validateMouseButton(button: Button):
    if button != Button.left:
        print('Invalid mouse button. Use left mouse button.')
        return False
    return True


def validateMousePosition(x: int, y: int):
    if len(mousePositionCoords) == 0:
        return True

    xPosition, yPosition = mousePositionCoords[0]

    if (xPosition == x or xPosition > x):
        print('here')
        return False

    if (yPosition == y or yPosition > y):
        print('here2')
        return False

    return True

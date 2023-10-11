from sf.mouse.getMousePostion import getMousePosition

userActions: list[str] = ['help', 'h', 'start', 's']
helpMenu = """
> This is the help menu
> Newline 
> Another newline 
"""
mousePositionInstructions = """
> First click should be the top left corner of the area you want to capture.
> Second click should be the bottom right corner of the area you want to capture.

Click "mouse wheel" to exit.
"""


class Solver:
    def __init__(self):
        # print('Init')
        self.prompt()

    def prompt(self):
        userAction = input(
            'What would you like to do? (\'help\' for help) ').casefold()

        if userAction not in userActions:
            print('Invalid action, please try again.')
            return self.prompt()

        if (checkAction(self, userAction)):
            return self.prompt()

    def startSolving(self):
        if not self.getSolvingWindow():
            return self.prompt()

    def getSolvingWindow(self):
        self.printMouseInstruction()
        self.mousePosition = getMousePosition(self)
        if len(self.mousePosition) != 2:
            print('Invalid mouse position(s). Please try again.')
            return False
        return True

    def printMouseInstruction(self):
        print(mousePositionInstructions)


def checkAction(self: Solver, action: str) -> bool:
    match action:
        case 'start' | 's':
            self.startSolving()
            return False

        case 'help':
            print(helpMenu)

        case 'test':
            print('lmao')

        case _:
            print('Invalid action, please try again.')

    return True


from sf.getMousePostion import getMousePosition
from sf.itemFinder import ItemFinder


userActions: list[str] = [
    'help', 'h',
    'mousepos', 'mp',
    'start', 's'
]

helpMenu = """
> help | h
    - Displays this menu
    
> mousepos | mp
    - Gets the x,y positions for the solving "window"
    
> start | s
    - Start the item finder
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

        self.checkAction(userAction)

    def startSolving(self):
        # if not self.getSolvingWindow():
        #     return self.prompt()
        self.getSolvingWindow()
        self.prompt()

    def getSolvingWindow(self):
        self.printMouseInstruction()
        self.mousePosition = getMousePosition(self)
        if len(self.mousePosition) != 2:
            print('Invalid mouse position(s). Please try again.')
            return False
        return True

    def printMouseInstruction(self):
        print(mousePositionInstructions)

    def checkAction(self, action: str):
        match action:
            case 'help' | 'h':
                print("*" * 30)
                print(helpMenu)
                print("*" * 30)

            case 'mousepos' | 'mp':
                self.startSolving()
                return

            case 'start' | 's':
                ItemFinder(self)
                return

            case _:
                print('Invalid action, please try again.')

        self.prompt()

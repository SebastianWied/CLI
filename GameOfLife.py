import copy
import time
import curses

ALIVE = 1
DEAD = 0
xSize = 100
ySize = 40


def initializeBoard(board):
    """
    Initializes the game board with all cells set to DEAD.

    Args:
    board (list): The game board as a 2D list.
    """
    for y in range(ySize):
        newList = []
        for x in range(xSize):
            newList.append(DEAD)
        board.append(newList)


def checkNeighbors(x, y, board):
    """
    Counts the number of alive neighbors for a given cell (x, y).

    Args:
    x (int): The x-coordinate of the cell.
    y (int): The y-coordinate of the cell.
    board (list): The game board.

    Returns:
    int: The number of alive neighbors.
    """
    total = 0

    for checkX in range(x-1, x+2):
        if checkX >= 0 and checkX < xSize:
            for checkY in range(y-1, y+2):
                if x == checkX and y == checkY:
                    continue  # Skip current cell
                if checkY >= 0 and checkY < ySize and board[checkY][checkX]:
                    total += 1  # Only adds one if alive and in bounds

    return total


def setState(x, y, state, grid):
    """
    Sets the state of a cell in the grid.

    Args:
    x (int): The x-coordinate of the cell.
    y (int): The y-coordinate of the cell.
    state (int): The new state of the cell (ALIVE or DEAD).
    grid (list): The grid in which to set the state.
    """
    grid[y][x] = state


def updateBoard(board):
    """
    Updates the board based on Conway's Game of Life rules.

    Args:
    board (list): The current game board.

    Returns:
    list: The updated game board.
    """
    grid = copy.deepcopy(board)
    for y, yRow in enumerate(board):
        for x, xVal in enumerate(yRow):
            neighbors = checkNeighbors(x, y, board)
            if neighbors < 2:
                setState(x, y, DEAD, grid)
            elif neighbors == 2:
                if board[y][x] == ALIVE:
                    continue
            elif neighbors == 3:
                setState(x, y, ALIVE, grid)
            else:
                setState(x, y, DEAD, grid)
    return grid


def drawGrid(grid, screen, hOffset=1):
    """
    Draws the grid on the screen.

    Args:
    grid (list): The grid to draw.
    screen: The curses screen object.
    hOffset (int): Horizontal offset for drawing.
    """
    screen.clear()
    xLen = len(grid[0])
    yHeight = len(grid)

    # Draw border
    for x in range(xLen+2):
        screen.addstr(0+hOffset, x, '-')
        screen.addstr(yHeight+1+hOffset, x, '-')
    for y in range(yHeight+2):
        screen.addstr(y+hOffset, 0, '|')
        screen.addstr(y+hOffset, xLen+1, '|')

    # Draw grid
    for height, yRow in enumerate(grid):
        for xDist, x in enumerate(yRow):
            if x == 0:
                value = ' '  # Dead
            if x == 1:
                value = '1'  # Alive
            screen.addstr(1+height+hOffset, 1+xDist, value)
    screen.addstr(0, 0, 'Quit simulation using q')
    screen.refresh()


def createPattern(screen, grid):
    """
    Allows user to create a pattern on the grid before starting the simulation.

    Args:
    screen: The curses screen object.
    grid (list): The grid on which to create the pattern.

    Returns:
    list: The grid with the user-created pattern.
    """
    board = copy.deepcopy(grid)
    xPos = 0
    yPos = 0
    hOffset = 1
    drawGrid(board, screen, hOffset)
    # Highlight cursor:
    screen.addstr(yPos+1+hOffset, xPos+1, 'X', curses.A_STANDOUT)
    screen.addstr(0, 0, ("Control the cursor using the arrow keys. Press " +
                         "enter to place a tile. Begin simulation using r"))
    screen.refresh()
    while True:
        inp = inputHandler.getInput(screen)
        if inp == 'Run/reload':
            break
        elif inp == 'Up':
            yPos = max(0, yPos-1)
        elif inp == 'Down':
            yPos = yPos + 1
        elif inp == 'Left':
            xPos = max(0, xPos-1)
        elif inp == 'Right':
            xPos = xPos + 1
        elif inp == 'Select':
            state = board[yPos][xPos]
            if state == 0:
                setState(xPos, yPos, ALIVE, board)
            else:
                setState(xPos, yPos, DEAD, board)

        drawGrid(board, screen, hOffset)
        screen.addstr(0, 0, ('Control the cursor using the arrow keys.' +
                             " Press enter to place a tile." +
                             " Begin simulation using r"))
        screen.addstr(yPos+1+hOffset, xPos+1, 'X', curses.A_STANDOUT)
        screen.refresh()
    return board


def main(stdscr, InputHandler):
    """
    Main function to run the simulation.

    Args:
    stdscr: The standard screen object provided by curses.
    InputHandler: An object to handle user inputs.
    """
    board = []
    stdscr.clear()
    curses.curs_set(0)
    stdscr.refresh

    global inputHandler
    inputHandler = InputHandler

    initializeBoard(board)
    board = createPattern(stdscr, board)

    drawGrid(board, stdscr)

    time.sleep(1)

    while True:
        stdscr.nodelay(1)
        inp = inputHandler.getInput(stdscr)
        if inp == 'Quit':
            break
        board = updateBoard(board)
        drawGrid(board, stdscr)
        time.sleep(.05)  # Tick speed


if __name__ == '__main__':
    curses.wrapper(main)

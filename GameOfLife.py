import copy
import time
import curses

ALIVE = 1
DEAD = 0
xSize = 100
ySize = 40

def initializeBoard(board):
    for y in range(ySize):
        newList = []
        for x in range(xSize):
            newList.append(DEAD)
        board.append(newList)
        
def checkNeighbors(x,y,board):
    total = 0
    
    for checkX in range(x-1,x+2):
        if checkX >= 0 and checkX < xSize:
            for checkY in range(y-1,y+2):
                if x == checkX and y == checkY:
                    continue
                if checkY >= 0 and checkY < ySize and board[checkY][checkX]:
                    total += 1
        
    return total
    
def setState(x,y,state,grid):
    grid[y][x] = state

def updateBoard(board):
    grid = copy.deepcopy(board)
    for y,yRow in enumerate(board):
        for x,xVal in enumerate(yRow):
            neighbors = checkNeighbors(x, y,board)
            if neighbors < 2:
                setState(x, y, DEAD,grid)
            elif neighbors == 2:
                if board[y][x] == ALIVE:
                    continue
            elif neighbors == 3:
                setState(x, y, ALIVE,grid)
            else:
                setState(x, y, DEAD,grid)
    return grid

def drawGrid(grid,screen,hOffset = 1):
    screen.clear()
    xLen = len(grid[0])
    yHeight = len(grid)
    
    for x in range(xLen+2):
        screen.addstr(0+hOffset,x,'-')
        screen.addstr(yHeight+1+hOffset,x,'-')
    for y in range(yHeight+2):
        screen.addstr(y+hOffset,0,'|')
        screen.addstr(y+hOffset,xLen+1,'|')
        
    for height,yRow in enumerate(grid):
        for xDist,x in enumerate(yRow):
            if x == 0:
                value = ' '
            if x == 1:
                value = '1'
            screen.addstr(1+height+hOffset,1+xDist,value)
    screen.addstr(0,0,'Quit simulation using q')
    screen.refresh()
    

def createPattern(screen,grid):
    board = copy.deepcopy(grid)
    xPos = 0
    yPos = 0
    hOffset = 1
    drawGrid(board, screen, hOffset)
    screen.addstr(yPos+1+hOffset,xPos+1,'X',curses.A_STANDOUT)
    screen.addstr(0,0,'Control the cursor using the arrow keys. Press enter to place a tile. Begin simulation using r')
    screen.refresh()
    while True:
        inp = inputHandler.getInput(screen)
        if inp == 'Run/reload':
            break
        elif inp == 'Up':
            yPos = max(0,yPos-1)
        elif inp == 'Down':
            yPos = yPos + 1
        elif inp == 'Left':
            xPos = max(0,xPos-1)
        elif inp == 'Right':
            xPos = xPos + 1
        elif inp == 'Select':
            state = board[yPos][xPos]
            if state == 0:
                setState(xPos, yPos, ALIVE, board)
            else:
                setState(xPos, yPos, DEAD, board)
        
        drawGrid(board, screen, hOffset)
        screen.addstr(0,0,'Control the cursor using the arrow keys. Press enter to place a tile. Begin simulation using r')
        screen.addstr(yPos+1+hOffset,xPos+1,'X',curses.A_STANDOUT)
        screen.refresh()
    return board
    

def main(stdscr, InputHandler):
    board = []
    stdscr.clear()
    curses.curs_set(0)
    stdscr.refresh

    global inputHandler
    inputHandler = InputHandler

    initializeBoard(board)
    board = createPattern(stdscr,board)

    drawGrid(board,stdscr)

    time.sleep(1)
        
    while True:
        stdscr.nodelay(1)
        inp = inputHandler.getInput(stdscr)
        if inp == 'Quit':
            break
        board = updateBoard(board)
        drawGrid(board,stdscr)
        time.sleep(.05)
    
if __name__ == '__main__':
    curses.wrapper(main)
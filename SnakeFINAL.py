#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  3 08:17:25 2023

@author: sebastianwiedenhoeft
"""

'''
Plan:

Initialization:
    
    Create screen
    Create board
    Create initial variables:
        Score
        Position
    Place player in center of board
    Place initial apples
    
If q is pressed, quit program

Class snake - DONE
    Store previous moves
    Store score
    Store current direction
    
    Function: move
        Call board function to check off limits
    
Class board - DONE
    Store board
    Store off limits board
    Store board dimensions as easy access vars
    
    Check if a position is off limits function
    Function: Draw board
    Function: Initialize board
    Function: Create off limits board

Gameplay loop:
    General function:
        Process the game one tick at a time, loop this tick function
    Tick function:
        What it needs to do:
            Move
                
            Check for apple
            
            Update snake with output from move
            
    Move function:
        Input: current direction
        
        Create 4 element list, checking each direction around snake.
        Check for input
            If there is input, update direction
            If no input, keep at current direction
        Update new position based on direction
        return new position
'''
import numpy as np
import curses
import time
import random as rand

class snakeClass:
    score = 1
    prevPosX = []
    prevPosY = []
    bodyX = []
    bodyY = []
    currentPos = (0,0) #(y,x)
    currentDir = 3 #Start facing west
    
    def prevPos(self,oldX,oldY):
        self.prevPosX.append(oldX)
        self.prevPosY.append(oldY)
    
    def drawSnake(self,board,tile):
        self.bodyX = self.prevPosX[(-1*self.score):] #Get body x positions from prevposition list
        self.bodyY = self.prevPosY[(-1*self.score):] #Get body y positions from prevposition list
        for i in range(self.score):
            board.board[self.bodyY[i],self.bodyX[i]] = tile
            
    def getScore(self):
        return self.score
    
    def setScore(self,new):
        self.score = new
            
    def __init__(self,y,x):
        self.currentPos = (y,x)

class playMap:
    board = 0
    olboard = 0
    boardY = 0
    boardX = 0
    applePos = (15,20)
    
    def initializeBoard(self,sh,sw):
        board = np.full((sh,sw), ' ') #Create empty board with no border
        yToUse = 0#Draw border
        for i in range(2):
            for j in range(sw):
                board[yToUse,j] = '-'
            yToUse = sh-1
            
        xToUse = 0 #Draw border
        for i in range(2):
            for j in range(sh):
                board[j,xToUse] = '|'
            xToUse = sw-1
        return board
    
    def initializeOLBoard(self,y,x,boundary):
        '''
        Generate board to use to check if position is off limits. 0 is off limits, 1 is allowed

        Parameters
        ----------
        board : array
            Game board.
        boundary : int
            How much of the edge is off limits.

        Returns
        -------
        None.

        '''
        OLBoard = np.full((y,x),1) #OLBoard = off limits board
        switcher = 0 #Controls direction of boundary creation
        
        #Create top and bottom bounds
        for switch in range(0,y,y-1):#Switch for top and bottom, start at 0 and jump to y
            for dx in range(x): #Iterate over every x
                for bound in range(boundary): #Loop for boundary size. If boundary is 1, make one off limits row
                    OLBoard[switch+(bound * ((-1)**switcher)),dx-1] = 0 # -1 ** switcher means on left side, it prints
                    #first row then second row(increasing, -1^0 = 1), and on right side(switcher = 0), creates
                    #second boundary then first(-1^1 = -1). Makes it work towards the middle.
            switcher = 1 #Changes direction of boundary creation
        
        switcher = 0
        
        #Create left and right bounds. Process is same as above, look there for info on workings
        for switch in range(0,x,x-1):
            for dy in range(y):
                for bound in range(boundary):
                    OLBoard[dy,switch+(bound * ((-1)**switcher))] = 0
            switcher = 1
            
            
        return OLBoard
    
    def offLimitsMap(self,pos,olboard):
        offLimits = [0,0,0,0] #0 means disallowed, 1 means allowed. Each index corresponds to a direction
        currentX = pos[1]
        currentY = pos[0]
        
        for i in range(2): #Check up/down
            yToUse = currentY + (1*((-1)**i))
            offLimits[i] = olboard[yToUse, currentX]
            
        for i in range(2): #Check right/left
            xToUse = currentX + (1*((-1)**i))
            offLimits[i+2] = olboard[currentY, xToUse]
        
        #self.testOffLimitsMap(offLimits,pos)
        return offLimits
    
    def testOffLimitsMap(self,ol,pos): #Ooff limit board testing-for program functionality
        currentX = pos[1]
        currentY = pos[0]
        print('Current x:',currentX)
        print('Current y:',currentY)
        for x in range(-1,2):
            for y in range(-1,2):
                print(self.olboard[currentX+x,currentY+y], end = '')
            print('\n')
            
    def checkOffLimits(self,snake,board): #Run to check if the snake is in a legal position
        if (snake.currentPos[1] == 0) or (snake.currentPos[1] == board.boardY-1):
            return 0 #Return dead
        if (snake.currentPos[0] == 0) or (snake.currentPos[0] == board.boardX-1):
            return 0 #Return dead
        else:
            return 1 #Return not dead
            
    def drawBoard(self,stdscr): #T
        height, width = np.shape(self.board)
        
        stdscr.clear()
        for x in range(0,width):
            for y in range(0,height):
                tile = str(self.board[y,x])
                stdscr.addstr(y,x,tile)
                #stdscr.refresh()
                #time.sleep(.5)
        
        stdscr.addstr(height,0,'Use arrow keys to navigate. q to exit')
        stdscr.refresh()
        return stdscr
    
    def checkSelfColl(self,snake):
        snakeY, snakeX = snake.currentPos
        # Check if the current position is in the snake's body
        if (snakeY, snakeX) in zip(snake.bodyY, snake.bodyX):
            return False  # Snake collided with itself
        else:
            return True  # Snake did not collide with itself
    
    def __init__(self,sh,sw,bound):
        self.boardX = sw
        self.boardY = sh
        
        self.board = self.initializeBoard(self.boardX,self.boardY)
        self.olboard = self.initializeOLBoard(self.boardY, self.boardX, bound)
        pass

class Gameplay:
    def gameplayLoop(self, stdscr,tickLength,sh,sw):
        #This function controls all game functions
        board = playMap(sw, sh, 1)  #Create new board
        snake = snakeClass(10, 10) #Create new snake in top left corner
        direction = 1 #Set starting direction
        snake.prevPos(10, 10) #Add previous position for drawing purposes
        self.placeApple(board) #Generate apple
        
        while (board.checkOffLimits(snake, board) == 1): #While snake in a legal position, loop game tick
            if not board.checkSelfColl(snake):
                break  # Snake collided with itself, end the game
            #Game tick - run and feed direction into next game tick
            direction = self.gameplayTick(snake, board, stdscr, direction, tickLength)
            if direction == -1:
                return
        #This runs if the loop ends, which means the player lost
        stdscr.clear() #Clear the screen
        title = 'You lost. Please press y if you would like to play again. Press anything else to quit'
        score = 'Score: '+str(snake.getScore()-1)
        stdscr.addstr(sh//2-3,sw//2-(len(score))//2,score)
        stdscr.addstr(sh//2,sw//2-(len(title)//2),title) #Draw ending message
        stdscr.refresh()
        stdscr.nodelay(0) #Make screen pause when input is asked for
        cont = stdscr.getch() #Get input if the player wants to continue
        stdscr.nodelay(1)
        if cont == ord('y'): #If they do, clear screen and run this function again. This restarts the game
            stdscr.clear()
            self.gameplayLoop(stdscr,tickLength,sh,sw)
        else:
            return #If not, end the program
             
    
    def gameplayTick(self, snake,board,stdscr,dire,tickLength):
        '''
        Choose take direction input from updateDirection functio. This feeds back into this gameplay function on the next tick
        Get movement
        Place snake on board
        Draw board

        '''
        snake.setScore(snake.getScore() + self.eatApple(board, snake)) #Check if apple eaten
        result = snake.drawSnake(board, ' ') #Clear previous snake position
        
        direction = self.updateDirection(snake,stdscr,dire)
        if direction == -1:
            return -1
        #Update board with snake position
        
        snake.drawSnake(board,'X')
        #Draw Board
        board.drawBoard(stdscr)
        #Wait for tick length
        time.sleep(tickLength)
        return direction #Feed direction to next tick

    def updateDirection(self, snake,stdscr,dire):
        '''
        Assigns new values to snake.pos and snake.direction
        
        Checks for input
        
        If no input, set direction to snake.direction
        If input, set direction to input and snake.direction to input
        
        Call movement function

        Parameters
        ----------
        snake : TYPE
            DESCRIPTION.

        Returns
        -------
        direction
        '''
        direction = dire
        stdscr.nodelay(1)
        
        ch = inputHandler.getInput(stdscr)
        
        if ch == -1: #If no input, dont do anything. Direction stays the same, 
            pass #so snake moves in the same direction as before
        elif ch == 'Quit': #If q is pressed, end program
            return -1
        elif (ch == 'Up') and direction != 2: #If w, move north
            direction = 0
        elif (ch == 'Right') and direction != 3: #If d, move east
            direction = 1
        elif (ch == 'Down') and direction != 0: #If s, move south
            direction = 2
        elif (ch == 'Left') and direction != 1: #If a, move west
            direction = 3
        
        snake.currentPos = self.movement(direction,snake) #Run movement function.
        
        return direction 

    def movement(self, direction, snake):
        '''
        Update direction based on direction input
        North = direction 0
        East = direction 1
        South = direction 2
        West = direction 3
        
        Parameters
        ----------
        snake : object

        Returns
        -------
        new position
        '''
        newY = snake.currentPos[0] 
        newX = snake.currentPos[1] #set new position to current position
        snake.prevPos(newX, newY)#Add prev position to prevPos list
        if direction == 0: #Update position based on move direction
            newY -=  1
        elif direction == 1:
            newX += + 1
        elif direction == 2:
            newY +=  1
        elif direction == 3:
            newX -= 1
        
        position = (newY,newX) #create new position tuple
        return position #Return to snake object
    
    def placeApple(self,board): #Put an apple in a random position on the board
        height, width = np.shape(board.board) #Get board width and height
        randX = rand.randrange(0+2,width-2) #Choose random position within board
        randY = rand.randrange(0+2,height-2) #^
        
        board.board[randY,randX] = 'a' #Place apple icon on board
        
        board.applePos = (randY,randX) #Tell board where the apple is
        
    def eatApple(self,board,snake): #Run every move
        if (snake.currentPos == board.applePos): #If snake head in same position as apple
            board.board[board.applePos] = ' ' #Empty that tile
            self.placeApple(board) #Place another apple
            return 1 #Add one to score
        return 0 #If no apple eaten, add 0 to score
        
    
    def __init__(self,stdscr,tickLength,sh,sw):
        self.gameplayLoop(stdscr, tickLength,sh,sw)

def testing(): #Test map
    board = playMap(10,10,1)
    snake = snakeClass(5, 5)

    print('Snake current pos:', snake.currentPos)
    print('Snake current direction:', snake.currentDir)

    print('Board:\n', board.board)
    print('OLBoard:\n', board.olboard)
    print('Off limits map at snake pos:',board.offLimitsMap(snake.currentPos, board.olboard))
    print('Off limits map at 1,1:',board.offLimitsMap((1,1), board.olboard))
    pass

def chooseDifficulty(stdscr,sh,sw):
    speed = .1 #Seconds per loop
    
    gameplayHandler = Gameplay(stdscr,speed,sh,sw)
    
    return gameplayHandler
    
def main(stdscr,InputHandler):
    # Set up the screen
    curses.curs_set(0)
    stdscr.clear()
    stdscr.refresh()
    global inputHandler
    inputHandler = InputHandler

    # Get the screen dimensions
    sh, sw = stdscr.getmaxyx()

    # Display game title
    title = "Snake!"
    stdscr.addstr(sh // 2, (sw - len(title)) // 2, title)
    stdscr.refresh()
    stdscr.getch()
    
    sh-= 1
    sw -= 1
    
    gameplayHandler = chooseDifficulty(stdscr,sh,sw) #Start game
    
    
if __name__ == "__main__":
    curses.wrapper(main)
import curses


class Board:
    def __init__(self):
        self.board = [[0, 0, 0],
                      [0, 0, 0],
                      [0, 0, 0]]

    def assignNewTile(self, tile, player):
        self.board[tile[1]][tile[0]] = player

    def checkWin(self):
        # Check across win
        for y in self.board:
            if y[0] != 0:
                if y[0] == y[1] == y[2]:
                    return y[0]
        # Check up/down win
        for i in range(3):
            if self.board[0][i] != 0:
                if self.board[0][i] == self.board[1][i] == self.board[2][i]:
                    return self.board[0][i]
        # Check diagonal TL-BR
        if self.board[0][0] != 0:
            if self.board[0][0] == self.board[1][1] == self.board[2][2]:
                return self.board[0][0]
        # Check diagonal TL-BR
        if self.board[0][2] != 0:
            if self.board[0][2] == self.board[1][1] == self.board[2][0]:
                return self.board[0][2]
        return 0

    def drawBoard(self, screen, start):
        for x in range(3):  # Draw top markers
            screen.addstr(start[1], 3+start[0]+(2*x), str(x+1))
        for y in range(3):  # Draw Side markers
            screen.addstr(3+start[1]+(2*y), start[0], str(y+1))
        for height, y in enumerate(self.board):   # Draw board
            for x in range(3):
                tile = str(y[x])
                screen.addstr(3+start[1]+2*height, 3+start[0]+(2*x), tile)


def getInput(screen, player, sh, sw, board):
    while True:
        try:
            msg = f'Player {player} please input your x coordinate, \
followed by y coordinate of choice'
            screen.addstr((sh // 2) - 12, (sw // 2) - len(msg)//2, msg)
            screen.refresh()
            inp = screen.getch()
            if inp == ord('q'):
                return -1
            inpX = max(0, min(2, int(chr(inp))-1))
            inp = screen.getch()
            if inp == ord('q'):
                return -1
            inpY = max(0, min(2, int(chr(inp))-1))
            screen.addstr((sh//2) - 12, (sw // 2) - len(msg)//2, ' '*len(msg))
            if board.board[inpY][inpX] != 0:
                continue
            return inpX, inpY
        except ValueError:
            pass


def gameplay(screen, board, sw, sh):
    startX = (sw // 2) - 6
    startY = (sh // 2) - 9
    screen.clear()
    counter = 2
    while counter < 12:
        screen.clear()
        player = (counter % 2) + 1
        if board.checkWin() != 0:
            winner = board.checkWin()
            return winner
        board.drawBoard(screen, (startX, startY))
        val = getInput(screen, player, sh, sw, board)
        if val == -1:
            return -1
        inpX, inpY = val[0], val[1]
        screen.refresh()
        board.assignNewTile((inpX, inpY), player)
        counter += 1
    return 0


def main(stdscr):
    sh, sw = stdscr.getmaxyx()
    sw -= 1
    board = Board()
    curses.curs_set(0)
    winner = gameplay(stdscr, board, sw, sh)
    stdscr.clear()
    if winner == -1:
        return
    if winner != 0:
        msg = f'Player {winner} wins!'
        stdscr.addstr(sh//2, (sw//2) - len(msg)//2, msg)
    else:
        msg = 'Its a draw!'
        stdscr.addstr(sh//2, (sw//2) - len(msg)//2, msg)
    stdscr.refresh()
    stdscr.getch()


if __name__ == '__main__':
    curses.wrapper(main)

import SnakeFINAL as snake
import GameOfLife
import tictactoe

import curses
import cursesMenu as menu
import cursesInput


def main(stdscr):
    inputHandler = cursesInput.initializeKeyMapping({})
    options = {
        0: {'Name': '1', 'Description': 'Snake',
            'Function': snake.main, 'Params': [stdscr, inputHandler]},
        1: {'Name': '2', 'Description': "Conways's Game of Life",
            'Function': GameOfLife.main, 'Params': [stdscr, inputHandler]},
        2: {'Name': '3', 'Description': 'Tic Tac Toe',
            'Function': tictactoe.main, 'Params': [stdscr]},
        3: {'Name': '4', 'Description': 'Keymappings',
            'Function': inputHandler.showMappings, 'Params': [stdscr]}
        }
    header = '''To play a game, navigate with arrows and select using enter.
Exit the loader using q'''
    menu.main(screen=stdscr, options=options, header=header, menuPos=(1, 3),
              inputHandler=inputHandler)


if __name__ == '__main__':
    curses.wrapper(main)

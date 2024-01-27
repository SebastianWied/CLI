#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 11 22:11:30 2023

@author: sebastianwiedenhoeft
"""
import curses
import cursesInput
'''
Dynamic menu module - Currently only for full screen menus

Inputs:
    Menu size
    Header text
    Header position - defaults to top left
    Menu items
        Stored in a dictionary. Key is menu number, value is another dictionary
        The stored within dictionary contains all attributes of the menu entry
        If dictionary contains a function call, the value should be a list.
        first value is function call, other values are the parameters
'''


# =============================================================================
# Takes as input:
#    Screen to draw on
#    Dictionary of options
#      Dictionary formatted as:
#      {Menu number(starts at 0):
#                   {Name to print, description, function call, [parameters]},}
#    Header and header position
#    Menu position
# =============================================================================
def main(screen, options, header='', headerPos=(0, 0), menuPos=(0, 0),
         inputHandler=None,updateMethod=None):
    if not inputHandler:
        inputHandler = cursesInput.initializeKeyMapping({})
    screen.clear()
    curses.curs_set(0)

    sh, sw = screen.getmaxyx()
    sw -= 1

    selected = 0

    # Define everythings initial position for cleaner access
    headerx = headerPos[0]
    headery = headerPos[1]
    menux = menuPos[0]
    menuy = menuPos[1]

    # Loop to run menu
    while True:
        screen.clear()
        screen.nodelay(0)
        screen.addstr(headery, headerx, header)  # Draw header
        yCount = menuy

        for entry in options.items():
            name = str(entry[1]['Name'])
            if entry[0] == selected:  # Check if current entry is the selection
                screen.addstr(yCount, menux, name, curses.A_STANDOUT)
            else:
                screen.addstr(yCount, menux, name, curses.A_DIM)
            description = str(entry[1]['Description'])
            screen.addstr(yCount, menux + len(name) + 2, description)
            yCount += 1

        inp = inputHandler.getInput(screen)

        if inp == 'Quit':
            exit()
        elif inp == 'Down':
            selected = min(selected+1, len(options)-1)
        elif inp == 'Up':
            selected = max(selected-1, 0)
        elif inp == 'Select':
            selection = options[selected]
            if 'Function' in selection.keys():
                selection['Function'](*selection['Params'])
        elif inp == 'Escape':
            return inputHandler

    return inputHandler

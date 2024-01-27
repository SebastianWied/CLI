#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 11:33:21 2023

@author: sebastianwiedenhoeft
"""
import cursesMenu
import curses
'''
Self-built input handling class

Contains a universal keymapping that each program that accesses this uses
Each program that uses this input module runs an initialization function
    This initialization function passes in any custom keybinds
    specific to said program.
'''


class InputHandler:
    # =========================================================================
    # Default Key Mapping
    # This default mapping is used for all programs using this module.
    # Programs using this module run the updateKeyMapping function
    # =========================================================================
    keyMapping = {
        119: 'Up',  # Default: w
        115: 'Down',  # Default: s
        97: 'Left',  # Default: a
        100: 'Right',  # Default: d
        10: 'Select',  # Default: enter
        113: 'Quit',  # Default: q
        259: 'Up',  # Default: Up arrow
        258: 'Down',  # Default: Down arrow
        260: 'Left',  # Default: Left arrow
        261: 'Right',  # Default: Right arrow
        27: 'Escape',
        1000: 'No input',
        114: 'Run/reload',
        }

    keycodes = {
        97: 'a', 98: 'b', 99: 'c', 100: 'd', 101: 'e', 102: 'f', 103: 'g',
        104: 'h', 105: 'i', 106: 'j', 107: 'k', 108: 'l', 109: 'm', 110: 'n',
        111: 'o', 112: 'p', 113: 'q', 114: 'r', 115: 's', 116: 't', 117: 'u',
        118: 'v', 119: 'w', 120: 'x', 121: 'y', 122: 'z', 10: 'Enter',
        259: 'Up arrow',  258: 'Down arrow', 260: 'Left arrow',
        261: 'Right arrow', 27: 'Escape', 1000: 'No value'
        }

    def updateMapping(self, keycode, newMapping):
        self.keyMapping[keycode] = str(newMapping)

    def updateFromMenu(self, screen, keycode):
        newCode = screen.getch()
        if newCode in self.keyMapping.keys():
            return
        newVal = self.keyMapping[keycode]
        self.keyMapping.update({newCode: newVal})
        self.keyMapping.pop(keycode)
        self.showMappings(screen)

    def getInput(self, screen):
        inp = screen.getch()
        if inp == -1:
            inp = 1000
        return self.keyMapping[inp]

    def showMappings(self, screen, depth=0):
        toDisplay = {}
        keys = list(self.keyMapping.items())
        keys.sort()
        for count, item in enumerate(keys):
            toDisplay[count] = {'Name': str(self.keycodes[item[0]]),
                                'Description': str(item[1]),
                                'Function': self.updateFromMenu,
                                'Params': [screen, item[0]]}
        header = 'Program keymappings'
        cursesMenu.main(screen, toDisplay, header=header, menuPos=(1, 2))


# =============================================================================
# updateKeyMapping
# This function is called when the caller program is initialized.
# Returns an inputHandler class to be used program wide.
# Input dictionary is in the form {keycode:New mapping}
# Keycode is an int, new mapping is a string.
# =============================================================================

def initializeKeyMapping(updatedMaps):
    inputObject = InputHandler()
    for mapping in updatedMaps.items():
        code = mapping[0]
        value = mapping[1]
        inputObject.updateMapping(code, value)
    return inputObject


def main(stdscr):
    curses.curs_set(0)
    inputObject = initializeKeyMapping({})
    inputObject.showMappings(stdscr)


if __name__ == '__main__':
    curses.wrapper(main)

import curses
# =============================================================================
# Curses Toolkit
# Built by Sebastian Wiedenhoeft
# December 13, 2023
#
# This is a wrapper for curses, and as such requires an installation of curses
# =============================================================================
# =============================================================================
# OVERVIEW
#
# The main functionality of this library is the creation and handling of
# interactive menus. At the center of everything, the Menu class handles all of
# the functionality.
# =============================================================================


class Menu:
    def __init__(self, header=None, headerPosition=(0, 0), menuStart='DEFAULT',
                 xs=0, ys=0, fullScreen=False, screen=None):
        if menuStart == 'DEFAULT':
            self.menuStart = (headerPosition[0], headerPosition[1] + 1)
        else:
            self.menuStart = menuStart
        self.header = header
        self.headerPosition = headerPosition
        self.maxEntryLen = max(0, len(header))
        self.menuEntries = []
        self.currentSelection = 0
        self.fullScreen = fullScreen
        self.embeddedMenus = []
        self.xs = self.maxEntryLen
        if header:
            self.ys = 1
        else:
            self.ys = 0
        self.ys += abs(self.menuStart[1] - headerPosition[1])

    def addEntry(self, listPosition='end', name='', description='',
                 functionCall=None, params=[], visualAtts=[],
                 embeddedMenu=None):
        newEntry = MenuEntry(name=name, description=description,
                             visualAtts=visualAtts,
                             functionCall=functionCall, params=params)

        if listPosition == 'end':
            listPosition = len(self.menuEntries)
        self.embeddedMenus.insert(listPosition, embeddedMenu)

        self.menuEntries.insert(listPosition, newEntry)
        length = (len(name) + 2 + len(description))
        self.maxEntryLen = max(self.maxEntryLen, length)
        self.xs = max(self.xs, self.maxEntryLen)
        self.ys += 1

    def getEntry(self, position):
        return self.menuEntries[position]

    def getSelected(self):
        return self.menuEntries[self.currentSelection]

    def getSubMenu(self):
        return self.embeddedMenus[self.currentSelection]

    def removeEntry(self, position):
        self.menuEntries.pop(position)

    def moveSelection(self, move):
        if move == 'Up':
            self.currentSelection = max(0, self.currentSelection-1)
        if move == 'Down':
            self.currentSelection = min(len(self.menuEntries)-1,
                                        self.currentSelection+1)

    def moveMenu(self, newX, newY):
        self.headerPosition = (newX, newY)
        self.menuStart = (newX, newY+1)

    def drawMenu(self, screen):
        sh, sw = screen.getmaxyx()
        if self.fullScreen:
            for y in range(sh):
                if y >= sh:
                    continue
                screen.addstr(y, 0, ' '*(sw-1))
        else:
            screen.addstr(self.headerPosition[1], self.headerPosition[0],
                          ' '*self.xs)
            for y in range(self.ys-2):
                screen.addstr(self.menuStart[1]+y, self.menuStart[0],
                              ' '*self.xs)

        if self.header:
            headerX = self.headerPosition[0]
            headerY = self.headerPosition[1]
            # Add new header
            screen.addstr(headerY, headerX, self.header)

        menuX = self.menuStart[0]
        menuY = self.menuStart[1]
        for current, entry in enumerate(self.menuEntries):
            # Add new entry
            tag = entry.getName()
            if current == self.currentSelection:
                screen.addstr(menuY+current, menuX, tag, curses.A_STANDOUT)
                if self.embeddedMenus[self.currentSelection]:
                    embeddedX = self.headerPosition[0]+self.xs+1
                    embeddedY = self.headerPosition[1]
                    embedded = self.embeddedMenus[self.currentSelection]
                    embedded.moveMenu(embeddedX, embeddedY)
                    embedded.drawMenu(screen)
            else:
                screen.addstr(menuY+current, menuX, tag)
            desc = entry.getDescription()
            atts = entry.getAttributes()
            screen.addstr(menuY+current, menuX + 2 + len(tag), desc, *atts)


class MenuEntry:
    # =========================================================================
    # Internal only! Handles the storage of individual menu entries
    # =========================================================================

    def __init__(self, name='', description='',
                 visualAtts=[], functionCall=None, params=[]):
        self.name = name
        self.description = description
        self.visualAtts = visualAtts
        self.call = functionCall
        self.params = params

    def getName(self):
        return self.name

    def changeName(self, newName):
        self.name = newName

    def getDescription(self):
        return self.description

    def changeDescription(self, newDesc):
        self.description = newDesc

    def getAttributes(self):
        return self.visualAtts

    def changeAttributes(self, newAtts):
        self.visualAtts = newAtts

    def addAttribue(self, newAtt):
        self.visualAtts.append(newAtt)

    def executeCall(self):
        call = self.call
        if call:
            output = call(*self.params)
            return output
        return -1

    def changeParams(self, newParams):
        self.params = newParams


class InputHandler:
    defaultBinds = {
        'Select': [10],
        'Up': [119, curses.KEY_UP],
        'Down': [115, curses.KEY_DOWN],
        'Left': [curses.KEY_LEFT],
        'Right': [curses.KEY_RIGHT],
        'Quit': [113],
        '1': [49],
        '2': [50],
        '3': [51],
        '4': [52],
        '5': [53],
        '6': [54],
        '7': [55],
        '8': [56],
        '9': [57],
        '0': [48],
        }

    def getInput(self, screen):
        inp = screen.getch()
        for bind in self.defaultBinds:
            if inp in self.defaultBinds[bind]:
                return bind
        return False

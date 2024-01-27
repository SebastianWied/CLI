import CursesTools as tools
import curses
import MyDataTypes as data


def Quit():
    exit()


def main(stdscr):
    stdscr.clear()
    curses.curs_set(0)
    sh, sw = stdscr.getmaxyx()
    sw -= 1

    menu = tools.Menu(header='Test', headerPosition=(40, 10), fullScreen=True)

    subMenu = tools.Menu(header='Submenu', headerPosition=(30, 10))
    subsubmenu = tools.Menu(header='Sub sub menu', headerPosition=(50, 10))
    subsubmenu.addEntry(name='F', description='SubSubOption F')
    subsubmenu.addEntry(name='G', description='SubSubOption G',
                        functionCall=Quit)
    
    subMenu.addEntry(name='a', description='SubOption A')
    subMenu.addEntry(name='b', description='SubOption B')
    subMenu.addEntry(name='c', description='SubOption C',
                     embeddedMenu=subsubmenu)
    inputHandler = tools.InputHandler()
    
    menu.addEntry(name='1', description='Option 1')
    menu.addEntry(name='2', description='Option 2')
    menu.addEntry(name='3', description='Option 3')
    menu.addEntry(name='4', description='Option 4', embeddedMenu=subMenu)
    menu.addEntry(name='5', description='Option 5')
    menu.addEntry(name='6', description='Option 6')
    menu.addEntry(name='7', description='Option 7', functionCall=Quit)

    inp = False

    selectedMenu = menu
    parentMenu = data.Stack()
    parentMenu.push(selectedMenu)
    while True:
        for x in range(sw):
            for y in range(sh):
                stdscr.addstr(y, x, '-')
        menu.drawMenu(stdscr)
        stdscr.refresh
        inp = inputHandler.getInput(stdscr)
        if inp == 'Quit':
            break
        if inp == 'Up':
            selectedMenu.moveSelection(inp)
        if inp == 'Down':
            selectedMenu.moveSelection(inp)
        if inp == '1':
            selectedMenu = menu
        if inp == 'Right':
            embeddedMenu = selectedMenu.getSubMenu()
            if embeddedMenu:
                parentMenu.push(selectedMenu)
                selectedMenu = embeddedMenu
        if inp == 'Left':
            selectedMenu = parentMenu.pop()
        if inp == 'Select':
            selectedMenu.getSelected().executeCall()


if __name__ == '__main__':
    curses.wrapper(main)

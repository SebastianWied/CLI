#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 13:07:36 2023

@author: sebastianwiedenhoeft
"""

import curses

def main(stdscr):
    stdscr.clear()
    curses.curs_set(0)
    
    
    
    for _ in range(10):
        inp = stdscr.getch()
        stdscr.addstr(0,0,str(inp))
        stdscr.refresh()
        
curses.wrapper(main)
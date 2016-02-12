#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
import curses
import os

# Get rid of delay on Escape press
os.environ.setdefault('ESCDELAY', '25')

class ConsoleScreen(object):
	"""Handles the output to screen in console"""
	def __init__(self):
		super(ConsoleScreen, self).__init__()
		self.key_handlers = None

	def initKeyHandlers(self, key_handlers):
		self.key_handlers = key_handlers

	def getInput(self):
		kh = self.key_handlers
		c = self.stdscr.getch()
		
		if c == curses.KEY_RIGHT:
			kh.on_RIGHT_ARROW()
		elif c == curses.KEY_LEFT:
			kh.on_LEFT_ARROW()
		elif c == curses.KEY_UP:
			kh.on_UP_ARROW()


	def update(self, game_screen):
		self.stdscr.clear()
		self.stdscr.addstr(game_screen)

		self.stdscr.refresh()

	def initScreen(self):
		self.stdscr = curses.initscr()


		curses.cbreak()
		curses.noecho()
		self.stdscr.keypad(True)
		# Removes the pause on getting user input
		self.stdscr.nodelay(True)
		# self.stdscr.timeout(0)

	def destroyScreen(self):
		curses.nocbreak()
		self.stdscr.keypad(False)
		# self.stdscr.timeout(-1)
		curses.echo()
		curses.endwin()
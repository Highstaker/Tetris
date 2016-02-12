#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
from consoleScreen import ConsoleScreen
from keyHandlers import KeyHandlers
from tetrisTimer import TetrisTimer

FALL_PERIOD = 0.7


class TetrisConsole(object):
	"""docstring for TetrisConsole"""
	def __init__(self):
		super(TetrisConsole, self).__init__()
		self.console_screen = ConsoleScreen()
		self.tetris_timer = TetrisTimer(self.console_screen)


	def run(self):
		self.tetris_timer.runGame()



def main():
	tetris = TetrisConsole()
	tetris.run()

if __name__ == '__main__':
	main()
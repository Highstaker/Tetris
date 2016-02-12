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
		# self.tetris_abstract = self.tetris_timer.tetris_abstract



		# self.key_handlers = KeyHandlers(tetris_abstract=self.tetris_abstract)

		# self.addKeyHandlers()

		# self.stay_time_start = time.time()

		# self.key_handler.main_loop()


	# def addKeyHandlers(self):
	# 	# kh = self.key_handler
	# 	ab = self.tetris_abstract
	#
	# 	kh.addKeyHandler(kh.KEY_LEFT, ab.moveLeft())

	# def mainRoutine(self):
	# 	ab = self.tetris_abstract
	#
	# 	if (time.time()-self.stay_time_start) > FALL_PERIOD:
	# 		#try to move piece down
	# 		ab.pieceStepDown()
	# 		ab.formatGrid(_print=False)
	#
	# 		stay_time_start = time.time()


	def run(self):
		self.tetris_timer.runGame()



def main():
	tetris = TetrisConsole()
	tetris.run()

if __name__ == '__main__':
	main()
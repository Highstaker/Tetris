#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
from time import time

from keyHandlers import KeyHandlers
from tetrisAbstract import TetrisAbstract

FALL_PERIOD = 0.3

class TetrisTimer(object):
	"""docstring for TetrisTimer"""
	def __init__(self, screenClass):
		super(TetrisTimer, self).__init__()

		# class of Tetris rules and game state
		self.tetris_abstract = TetrisAbstract()

		# class handling the output to screen
		self.screenClass = screenClass

		# class containing functions invoked on button presses
		self.key_handlers = KeyHandlers(tetris_abstract=self.tetris_abstract, screenClass=screenClass, timerClass=self)

		# pass key handler functions to screen class, if it can manage the input
		screenClass.initKeyHandlers(self.key_handlers)

		# start point for the timer
		self.stay_time_start = time()

	def resetFallTimer(self):
		"""
		Sets the start time for fall timer to current, thus resetting it
		:return:
		"""
		self.stay_time_start = time()

	def runGame(self):
		ab = self.tetris_abstract
		self.screenClass.initScreen()

		try:
			while True:
				# When the game is over, get out of game loop
				if ab.flag_gameover:
					break

				self.screenClass.getInput()

				if (time()-self.stay_time_start) > FALL_PERIOD:
					# try to move piece down
					ab.pieceStepDown()

					self.screenClass.update(ab.formatGrid(_print=False))

					# ab.formatGrid(_print=False)

					self.stay_time_start = time()
		finally:
			self.screenClass.destroyScreen()

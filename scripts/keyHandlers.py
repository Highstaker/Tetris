#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-

class KeyHandlers(object):
	"""Contains handles to functions invoked on key presses"""
	def __init__(self, tetris_abstract, screenClass, timerClass):
		super(KeyHandlers, self).__init__()
		self.tetris_abstract = tetris_abstract
		self.screenClass = screenClass
		self.timerClass = timerClass

	def on_RIGHT_ARROW(self):
		self.tetris_abstract.moveRight()
		self.screenClass.update(self.tetris_abstract.formatGrid(_print=False))

	def on_LEFT_ARROW(self):
		self.tetris_abstract.moveLeft()
		self.screenClass.update(self.tetris_abstract.formatGrid(_print=False))

	def on_UP_ARROW(self):
		self.tetris_abstract.rotatePiece()
		self.screenClass.update(self.tetris_abstract.formatGrid(_print=False))

	def on_DOWN_ARROW(self):
		# Make a step down
		self.tetris_abstract.pieceStepDown()
		# Reset fall timer
		self.timerClass.resetFallTimer()
		#Update screen
		self.screenClass.update(self.tetris_abstract.formatGrid(_print=False))
from copy import deepcopy
from random import choice
from time import sleep

N_ROWS = 13
N_COLUMNS = 10
N_SAFETY_ROWS = 4


class TetrisAbstract(object):
	"""Class containing Tetris rules and game state"""

	# Contains available tetriminos, local positions of their blocks, and specific options
	# Make (0,0) the first, the program will treat its position as the position of the root (global tetrimino position)
	PIECES = {
			"Stick": {"points": ((0, 0), (-1, 0), (1, 0), (2, 0)), "options": tuple()},
			"Cube": {"points": ((0, 0), (1, 0), (0, 1), (1, 1)), "options": ("NO_ROTATE",)},
			"T-piece": {"points": ((0, 0), (-1, 0), (1, 0), (0, 1)), "options": tuple()},
			"L-piece": {"points": ((0, 0), (1, 0), (0, 1), (0, 2)), "options": tuple()},
			"inv-L-piece": {"points": ((0, 0), (-1, 0), (0, 1), (0, 2)), "options": tuple()},
			"S-piece": {"points": ((0, 0), (-1, 0), (0, 1), (1, 1)), "options": tuple()},
			"inv-S-piece": {"points": ((0, 0), (1, 0), (0, 1), (-1, 1)), "options": tuple()}
			}

	def __init__(self):
		super(TetrisAbstract, self).__init__()

		# Game over flag. When game is over, it is set to True
		self.flag_gameover = False

		# Counter of cleared lines
		self.lines_cleared = 0

		# Initializing the main array. [row number starting from bottom][column starting from left]
		self.grid = [x[:] for x in [[0] * N_COLUMNS] * (N_ROWS + N_SAFETY_ROWS)]

		# Holds positions of cubes of current piece
		self.cur_piece_pos = []

		# Piece that will eb the next
		self.next_piece = self.getRandomPiece()

		# Coordinates of spawn point
		self.spawn_point = (4, 13)

		# Spawn the first piece
		self.spawnPiece()

	def getRandomPiece(self):
		return self.PIECES[choice(list(self.PIECES.keys()))]

	def spawnPiece(self):
		"""
		Spawns a random piece.
		"""
		# Initialize current piece
		self.cur_piece_pos = []

		# The next piece becomes the current
		cur_piece = self.next_piece

		# assign global positions to all blocks of the tetrimino, as list of lists [row, col]
		for point in cur_piece["points"]:
			self.cur_piece_pos += [[(self.spawn_point[0] + point[0]), (self.spawn_point[1] + point[1]), ]]

		# Generate new next piece
		self.next_piece = self.getRandomPiece()

	def getLocalPos(self):
		"""
		Returns the local positions of blocks of current piece
		:return: a list of positions (lists [row,column])
		"""
		cur_pos = self.cur_piece_pos
		result = [(0,0),]
		for i in cur_pos[1:]:
			# substract global position of root piece (with index 0) from global position of another piece.
			result += [[i[0]-cur_pos[0][0], i[1]-cur_pos[0][1]]]
		return result

	def localToGlobalPos(self, local_pos):
		"""
		Takes the list of local positions of blocks and makes them into global positions
		:param local_pos:
		:return: a list of positions (lists [row,column])
		"""
		cur_pos = self.cur_piece_pos
		global_pos = []
		for i in local_pos:
			# sum the local position of a piece and global position of root piece
			global_pos += [[i[0]+cur_pos[0][0],i[1]+cur_pos[0][1]],]
		return global_pos

	def rotatePiece(self):
		"""
		Rotate a piece if possible
		:return:
		"""

		#Get global positions of blocks in a piece AFTER rotation
		rotated_piece = self.getRotatedPiece()

		#check if it collided with anything

		#Set the current piece to a new state (rotated)
		self.cur_piece_pos = rotated_piece

	def getRotatedPiece(self):
		"""
		returns the global positions of blocks in a piece after rotation
		:return: a list of lists [row, col] of global positions of block in a piece
		"""
		rotated_piece_local = []
		piece_local = self.getLocalPos()
		for block in piece_local:
			rotated_piece_local += [(block[1],-block[0])]

		# print("rotated_piece_local", rotated_piece_local)#debug
		# sleep(5)#debug

		rotated_piece = self.localToGlobalPos(rotated_piece_local)

		return rotated_piece

	def fixPiece(self):

		#Position the piece
		for point in self.cur_piece_pos:
			self.grid[point[1]][point[0]] = 1

		#Clear the row if it is full, move other rows down
		for rowN, row in enumerate(self.grid):
			# If the row is full
			if all(row):
				# Add to counter
				self.lines_cleared += 1

				# Iterate over rows above the cleared one
				for n, r in self.grid[rowN+1:N_ROWS+1]:
					# Only rows above the cleared one and below the top of the glass
					if N_ROWS > n > rowN:
						for colN, block in enumerate(row):
							#Set the row to values of a row directly above it
							self.grid[n][colN] = self.grid[n-1][colN]


		#Check GameOver
		if self.isToppedOut():
			self.flag_gameover = True
		else:
			#Continue game
			self.spawnPiece()


	def isToppedOut(self):
		"""
		Returns True is glass is overfilled (which is generally a gameover)
		:return: Bool
		"""
		return any(self.grid[N_ROWS+1])

	def pieceStepDown(self):
		"""
		Makes a piece move one step down.
		Fixes the piece if there is something immediately below it
		"""

		def stepDown():
			"""
			Move piece one step down
			:return:
			"""
			for i in self.cur_piece_pos:
				i[1] -= 1

		if self.somethingBelow():
			# Something is belo2. Fix the piece.
			self.fixPiece()
		else:
			stepDown()

	def moveLeft(self):
		"""
		Move the current piece to the left one step
		:return:
		"""
		if self.canMoveLeft():
			for i in self.cur_piece_pos:
				i[0] -= 1

	def moveRight(self):
		"""
		Move the current piece to the left one step
		:return:
		"""
		if self.canMoveRight():
			for i in self.cur_piece_pos:
				i[0] += 1

	def somethingBelow(self):
		"""
		Checks if any of tetrimino parts has something below it - glass bottom or a fixed tetrimino part
		"""
		if True in [j[1] <= 0 for j in self.cur_piece_pos]:
			return True
		elif any([self.grid[j[1] - 1][j[0]] for j in self.cur_piece_pos]):
			return True
		else:
			return False

	def canMoveLeft(self):
		if any([j[0] <= 0 for j in self.cur_piece_pos]):
			return False
		elif any([self.grid[j[1]][j[0] - 1] for j in self.cur_piece_pos]):
			return False
		else:
			return True

	def canMoveRight(self):
		'''
		Returns true if the current piece can move to the right.
		'''
		if True in [j[0]>=(N_COLUMNS-1) for j in self.cur_piece_pos]:
			return False
		elif any([self.grid[j[1]][j[0] + 1] for j in self.cur_piece_pos]):
			return False
		else:
			return True

	def formatGrid(self, _print=True):
		"""
		Returns the grid as a string in a formatted manner.
		:param _print: if True, prints grid to console.
		:return: formatted grid as a string
		"""
		grid = deepcopy(self.grid)

		for i in self.cur_piece_pos:
			grid[i[1]][i[0]] = 2

		grid = grid[::-1]

		result = ""

		for n, row in enumerate(grid):
			if n >= N_SAFETY_ROWS:
				result += "||" + "".join([(str(i) if i else " ") for i in row]) + "||" + "\n"
			else:
				result += "  " + "".join([(str(i) if i else " ") for i in row]) + "  " + "\n"

		result += "=" * (N_COLUMNS + 4) + "\n"

		if _print:
			print(result)

		return result


if __name__ == '__main__':
	tetris = TetrisAbstract()
	tetris.spawnPiece()

	tetris.formatGrid()

	while True:
		sleep(1)
		tetris.pieceStepDown()
		tetris.formatGrid()

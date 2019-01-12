from boardSetup import pairing
import time

N, E, S, W = 8, 1, -8, -1
directions = {
    'N': [N+N+E, E+N+E, E+S+E, S+S+E, S+S+W, W+S+W, W+N+W, N+N+W],
    # N+N+E = 17, E+N+E = 10, E+S+E = -6, S+S+E = -15, S+S+W = -17, W+S+W = -10, W+N+W = 6, N+N+W = 15
    'K': [N, E, S, W, N+E, S+E, S+W, N+W],
    # N = 8, E = 1, S = -8, W = -1, N+E = 9, S+E = -7, S+W = -9, N+W = 7
    'R': [N, E, S, W]
    # N = 8+, E = 1+, S = -8-, W = -1-
}


def returnWeight(pieceType):
	weight = {'N':2, 'R':3, 'K':5, 'n':2, 'k':5}
	pieceWeight = weight.get(pieceType)
	return pieceWeight


def isValidMove(board, pieceType, current, new): #board is a list, pieceType is a string, new is an integer
	#print("Current:%s , New:%s" % (board[current], board[new]))
	if new < 0 or new > 63: #first check if new is a square on the board
		return False
	if pieceType == '*': #safety check
		return False
	else: #check if piece can move in that direction
		if pieceType == 'K' or pieceType == 'k': #if the current piece is a king
			for k, directionList in directions.items(): # cycle through dictionary
				if k == 'K': #if the key is 'K'
					for item in directionList: #for all values attached to that key
						if new - current == item: #if a possible move for that piece
							if pieceType == 'K': #player x
								if board[new] == 'R' or board[new] == 'N':
									return False
								return True
							if pieceType == 'k': #player y
								if board[new] == 'r' or board[new] == 'n':
									return False
								return True
		elif pieceType == 'N' or pieceType == 'n': #if the current piece is a knight
			for k, directionList  in directions.items(): # cycle through dictionary
				if k == 'N': #if the key is 'N'
					for item in directionList: #for all values attached to that key
						if new - current == item: #if a possible move for that piece
							temp = (new%8) - (current%8)
							if temp in range(-2,3):
								if pieceType == 'N': #if player X
									if board[new] == 'R' or board[new] == 'K': #if another of your pieces is in the way
										return False
									return True
								if pieceType == 'n': #if player Y
									if board[new] == 'k': #if another of your pieces is in the way
										return False
									return True
		elif pieceType == 'R': #if the current piece is a rook
			for k, v in directions.items(): # cycle through dictionary
				if k == 'R': #if the key is 'R'
					for x in v: #for all values attached to that key
						if (new % 8 == current % 8 ) and (new != current): #if they are on same colum
							counter = current
							if new > current: #check going up
								while counter <= new:
									if board[counter] == 'N' or board[counter] == 'K':
										return False
									else:
										counter = counter + 8
							elif new < current: #check going down
								while counter >= new:
									if board[counter] == 'N' or board[counter] == 'K':
										return False
									else:
										counter = counter - 8
							return True
						counter = current
						while counter % 8 != 0:
							counter -= 1
							if board[counter] == 'N' or board[counter] == 'K':
								return False
							if(counter == new):
								return True
						counter = current
						while counter % 8 != 7:
							counter += 1
							if board[counter] == 'N' or board[counter] == 'K':
								return False
							if(counter == new):
								return True
						return False
		else:
			time.sleep(.0001)
#move
def move(board, player, pieceType, current, newSpot): #player is string, pieceType is string, newSpot is integer
	#global moveCount
	valid = isValidMove(board, pieceType, current, newSpot)
	if valid == True:
		for x in range(64): #find where the piece currently resides
			if board[x] == pieceType:
				current = x #set current to the location the piece currently resides
		board[newSpot] = pieceType #move the chess piece to the new location
		board[current] = '*' #remove the chess piece from its last location
		#showMove(board) #print out the board as it exists now

#showMove
def showMove(board): #board is a list
	currentLine = ''
	for i in range (0,64):
		if i%8 == 0:
			print(currentLine)
			currentLine = ''
			currentLine = currentLine + board[i] + ' '
		elif i == 63:
			currentLine = currentLine + board[i] + ' '
			print(currentLine)
		else:
			currentLine = currentLine + board[i] + ' '
	print("------------------\n")

#newBoardMove
def newBoardMove(board, current, new): #board is a list, current is an integer, new is an integer
	newBoard = list(board)
	piece = newBoard[current]
	newBoard[current] = '*'
	newBoard[new] = piece
	#showMove(newBoard)
	return newBoard

import time, random, move, sys, pdb
from boardSetup import pairing


random.seed()

def minMax(board, player):
	maxTime = 10000000.0 #set a max amount of time to work the minMax function
	start = time.time() #set start time
	currentTime = 0.0 #set current time
	maxValue = 0
	pieceType = ''
	minList =[]
	childRoot = {} #Dictionary of children states of the root. (tuple for current spot, new spot) : newBoard[]
	leafNodes = {} #Dictionary of leaf nodes. (tuple for opponent current spot, opponent new spot) : newOponnentBoard[]

	while currentTime < maxTime:
		#CREATE FIRST DEPTH
		#print("About to start the 1st depth")
		for i in range(64):#i = integer / board[i] = list[strings]
			if player == 'X':
				if board[i] == 'K' or board[i] == 'N' or board[i] == 'R': #If spot has Player X piece
					current = i
					for j in range(64): #j = integer / board[j] = string
						valid = move.isValidMove(board, board[current], i, j) #Check if valid move
						if valid == True: #generates first depth
							tempBoard = move.newBoardMove(board, current, j) #tempBoard = list[strings]
							tempTuple = (current, j) #tempTuple = (int, int)
							childRoot[tempTuple] = tempBoard#Add tuple (current location, new location) as key and new board as value
			if player == 'Y':
				if board[i] == 'k' or board[i] == 'n':
					current = i
					for j in range(64):
						valid = move.isValidMove(board, board[current], i, j)
						if valid == True:
							tempBoard = move.newBoardMove(board, current, j)
							tempTuple = (current, j)
							childRoot[tempTuple] = tempBoard

			currentTime = time.time() - start #update time
		#CREATE SECOND DEPTH
		for k,v in childRoot.items(): #k = key of childRoot (string, string) / v = value at key k (list[strings])
			temp = 0
			for m in v:
				if player == 'X':  #m = string / v = list[strings]
					if m == 'k' or m == 'n': #If piece is a Player Y piece
						current = m
						for n in range(0,64): #Check every spot on the board foter their piece to move to
							valid = move.isValidMove(v, m, v.index(m), n) #Check if valid move / #board is a list, pieceType is a string, new is an integer
							if valid == True: #generate leaf
								tempTuple = (v.index(m), n)
								leafNodes[tempTuple] = move.newBoardMove(v, v.index(m), n)#v is a list, m is an integer, n is an integer
				if player == 'Y':
					if m == 'K' or m == 'N' or m == 'R':
						current = m
						for n in range(0,64):
							valid = move.isValidMove(v,m,v.index(m), n)
							if valid == True:
								tempTuple = (v.index(m), n)
								leafNodes[tempTuple] = move.newBoardMove(v, v.index(m), n)
			#PROGRAM HAS RUN THROUGH ALL POSSIBLE MOVES FOR THE OPPONENT GIVEN THE CURRENT CHILD
			#RUN HEURISTIC FUNCTION FOR EACH LEAF NODE
			for a,b in leafNodes.items():
				temp =  heuristic(b, player, a, k)#heuristic(b, 'player', a, k) #Set temp  =  heuristic function
				leafNodes[a] = temp


			if player == 'X':
				minList = leafNodes.values()
				if 1000 in minList:
					childRoot[k] = 1000
				elif 500 in minList:
					childRoot[k] = 500
				else:
					childRoot[k] = min(minList)
			if player == 'Y':
				maxList = leafNodes.values()
				if -1000 in maxList:
					childRoot[k] = -1000
				elif -500 in maxList:
					childRoot[k] = -500
				else:
					childRoot[k] = max(maxList)
			currentTime = time.time() - start #update current time

		if player == 'X':
			maxValue = max(childRoot.values())
			for key, value in childRoot.items():
				if value == maxValue:
					move.move(board, 'X', board[key[0]], key[0], key[1]) #player is string, pieceType is string, newSpot is integer
					return (key[0], key[1])
		if player == 'Y':
			minValue = min(childRoot.values())
			for key, value in childRoot.items():
				if value == minValue:
					move.move(board, 'Y', board[key[0]], key[0], key[1])
					return (key[0], key[1])
	else:
		print(minList)
		print("Time has run out")

def heuristic(heuristicBoard, player, opponentMove, ourMove): #returns value and boolean if checkmate
	checkAttackList = [] #list of all possible check moves
	kingSpot = 0 #where the enemy king is
	if player == 'X':
		#opponent move first
		xLocation = ourMove[1] #Where our piece is GOING
		xPiece = heuristicBoard[xLocation] #What piece we are moving
		yLocation = opponentMove[1] #Where their piece is GOING
		yPiece = heuristicBoard[yLocation] #What piece they are moving
		attackList = getAttackList(heuristicBoard, xPiece, xLocation) #all possible moves our piece can make
		#If THEIR king is in check, this is good
		for i in range(0,64): #cycle through the board and find all other pieces besides the current piece
			if heuristicBoard[i] == 'N' or heuristicBoard[i] == 'K' or heuristicBoard[i] == 'R': #if one of the x pieces
				checkAttackList.extend(getAttackList(heuristicBoard, heuristicBoard[i], i)) #Make a super attack list of all pieces
		for i in range(0,64): #find the enemy king spot
			if heuristicBoard[i] == 'k':
				kingSpot = i
		if kingSpot in checkAttackList: #If we can attack the king
			checkBoolean = True #set the boolean to true
			kingMoveList = getAttackList(heuristicBoard, 'k', kingSpot)
			for items in kingMoveList: #cycle through all possible attaks
				if items not in checkAttackList: #If there is any attack that CANNOT kill enemy king
					return 500
			return 1000

		#calculate opponent possible moves
		possibleMoveList = getAttackList(heuristicBoard, yPiece, yLocation)
		intersect = set(attackList).intersection(possibleMoveList) #check if any possible moves for the opponent piece match a square our piece can attack
		numMoves = 1
		if len(intersect) == 0: #if the set is empty...try again
			possMov2 = []
			for items in attackList:
				possMov2.extend(getAttackList(heuristicBoard, yPiece, items))
			intersect2 = set(attackList).intersection(possMov2)
			numMoves = 2
			if len(intersect2) == 0:  #still havent found a move
				numMoves = 3
				FirstMoveChoice = random.choice(possMov2) #grab random move from first poss moves
			else: #set is not empty
				setToList = list(intersect2)
				if len(intersect2) > 1: #more than one item in the set
					worstOpponentMove = random.choice(setToList)
				else: #just one item in the set
					worstOpponentMove = setToList[0]
				numMoves = 2
		else: #set is not empty
			setToList = list(intersect)
			if len(intersect) > 1: #more than one item in the set
				worstOpponentMove = random.choice(setToList)
			else: #just one item in the set
				worstOpponentMove = setToList[0]
			numMoves = 1
		if numMoves == 1: #opponent piece is in a bad spot (for them)
			return 5 + move.returnWeight(yPiece)
		elif numMoves == 2: #opponent piece is in an ok spot (for them)
			return 10 + move.returnWeight(yPiece)
		elif numMoves == 3: #opponent piece is in a good spot (for them)
			return 20 + move.returnWeight(yPiece)
		else:
			print("No Heuristic Value")

		#---------PLAYER Y HEURISTIC----------#
	else: #if Player Y
		#opponent move first
		yLocation = ourMove[1] #Where OUR piece is GOING
		yPiece = heuristicBoard[yLocation] #What piece we are moving
		xLocation = opponentMove[1] #Where THEIR piece is GOING
		xPiece = heuristicBoard[xLocation] #What piece they are moving
		runAwayList = getAttackList(heuristicBoard, yPiece, yLocation) #all possible moves our piece can make

		#If OUR king is in check, this is bad
		for i in range(0,64): #cycle through the board and find all other pieces besides the current piece
			if heuristicBoard[i] == 'N' or heuristicBoard[i] == 'K' or heuristicBoard[i] == 'R': #if one of the x pieces
				checkAttackList.extend(getAttackList(heuristicBoard, heuristicBoard[i], i)) #Make a super attack list of all pieces
		for i in range(0,64): #find the enemy king spot
			if heuristicBoard[i] == 'k':
				kingSpot = i
		if kingSpot in checkAttackList: #If we can attack the king
			kingMoveList = getAttackList(heuristicBoard, 'k', kingSpot) #get list of moves king can make
			for items in kingMoveList: #cycle through all possible moves
				if items not in checkAttackList: #If there is any attack that CANNOT kill enemy king
					if yPiece == 'k':
						return -500
			if yPiece == 'k':
				return -1000
		#calculate opponent possible moves
		if yLocation in checkAttackList:
			return -50
		else:
			if yLocation in range(0,8):
				return -10 + move.returnWeight(yPiece)
			if yLocation in range(55-64):
				return -10 + move.returnWeight(yPiece)
			if yLocation % 8 == 0:
				return -10 + move.returnWeight(yPiece)
			if yLocation % 8 == 7:
				return -10 + move.returnWeight(yPiece)
			return 10 + move.returnWeight(yPiece)

def getAttackList(heuristicBoard, piece, location):
	attackList = []
	if  piece == 'K' or piece == 'k': #if our piece is a king
		checkAlist = [location+7, location+8, location+9, location+1, location-7, location-8, location-9, location-1]
		for items in checkAlist:
			if move.isValidMove(heuristicBoard, piece, location, items) == True:
				attackList.append(items)
	elif piece == 'N' or piece == 'n': #if our piece is a knight
		checkAlist = [location+17, location+10, location-6, location-15, location-17, location-10, location+6, location+15]
		for items in checkAlist:
			if move.isValidMove(heuristicBoard, piece, location, items) == True:
				attackList.append(items)
	elif piece == 'R': #if our piece is a rook #any spot to the left or right of the rook
		horizontalAttackList = []
		temp = location
		if temp % 8 == 0 or temp % 8 == 7: #if on either edge
			if temp % 8 == 0: #moving right side
				for i in range(1,8):
					horizontalAttackList.append(temp + i)
			if temp % 8 == 7: #moving left side
				for i in range(1,8):
					horizontalAttackList.append(temp - i)
		else:
			temp = location-1
			while temp % 8 != 0: #left moves for the rook
				horizontalAttackList.append(temp)
				temp = temp - 1
			else:
				horizontalAttackList.append(temp)

			temp = location+1
			while temp % 8 != 7: #right moves for the rook
				horizontalAttackList.append(temp)
				temp = temp + 1
			else:
				horizontalAttackList.append(temp)
		#any spot above or below the rook
		verticalAttackList = []
		for i in range(0,64):
			if i % 8 == location % 8:
				if i != location:
					verticalAttackList.append(i)
		#put them together
		attackList = horizontalAttackList + verticalAttackList
	else:
		print("Something went wrong")

	return attackList

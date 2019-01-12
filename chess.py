#chess
import minMax, boardSetup, move, time, os
board = boardSetup.setUpBoard()
print("Beginning of game")

def fileEmpty(path):
    return os.stat(path).st_size==0

def play(n):
	player = input("Choose player (X or Y): ")
	numLines = 0
	while n > (n/2):
		if player == 'X' or player == 'x': #Play as Player X
			log = open('log_Y.txt', 'r') #open the log_player.txt file in read only mode
			if fileEmpty('log_Y.txt') == False:#If there are logged moves in the text file
				log.seek(0)
				listLines = log.readlines() #read all lines into a list
				numLines = numLines + 1
				lastLine = listLines[-1] #grab just the last line of the list
				otherLog = open('log_X.txt', 'a')
				otherLog.write(lastLine)
				otherLog.close()
				lastLine = lastLine[2:] #Grabs only player, pieceType, and newSpot
				lastLine = lastLine[0:7]
				lastMove = lastLine.split(':') #Separates the strings into members of a list
				#lastMove[0] = Player #lastMove[1] = Old Spot #lastMove[2] = New Spot
				#board, player, pieceType, current, newSpot
				oldSpot = boardSetup.pairing[lastMove[1]]
				newSpot = boardSetup.pairing[lastMove[2]]
				move.move(board, lastMove[0], board[oldSpot], oldSpot, newSpot) #update board
			else:
				numLines = numLines + 1
			log.close()#close the file
			returnedTuple = minMax.minMax(board, player)
			oldLocation = boardSetup.reverse.get(returnedTuple[0])
			newLocation = boardSetup.reverse.get(returnedTuple[1])
			log = open('log_X.txt', 'a') #open the log_player.txt file in append mode
			log.write(str(numLines))
			log.write(' X:')
			log.write(oldLocation)
			log.write(':')
			log.write(newLocation)
			log.write('\n')
			log.close() #close the file
			move.showMove(board)
			input()
			n -= 1
		else:#Play as Player Y
			log = open('log_X.txt', 'r') #open the log_player.txt file in read only mode
			if fileEmpty('log_X.txt') == False:#If there are logged moves in the text file
				log.seek(0)
				listLines = log.readlines() #read all lines into a list
				numLines = numLines + 1
				lastLine = listLines[-1] #grab just the last line of the list
				otherLog = open('log_Y.txt', 'a')
				otherLog.write(lastLine)
				otherLog.close()
				lastLine = lastLine[2:] #Grabs only player, pieceType, and newSpot
				lastLine = lastLine[0:7]
				lastMove = lastLine.split(':') #Separates the strings into members of a list
				oldSpot = boardSetup.pairing[lastMove[1]]
				newSpot = boardSetup.pairing[lastMove[2]]
				move.move(board, lastMove[0], board[oldSpot], oldSpot, newSpot) #update board
			log.close()#close the file
			returnedTuple = minMax.minMax(board, player)
			oldLocation = boardSetup.reverse.get(returnedTuple[0])
			newLocation = boardSetup.reverse.get(returnedTuple[1])
			log = open('log_Y.txt', 'a') #open the log_player.txt file in append mode
			log.write(str(numLines))
			log.write(' Y:')
			log.write(oldLocation)
			log.write(':')
			log.write(newLocation)
			log.write('\n')
			log.close() #close the file
			move.showMove(board)
			n -= 1
			input()

	if n == 0: #If maximum number of moves has been reached
		print()
		print("Maximum amount of moves has been made.")
	elif n == -1: #If opponent King has been killed
		print()
		print("Opponet King has been captured. You win!")
	elif n == -2: #If player King has been killed
		print()
		print("Your King has been captured. You lose.")
	elif n == -3: #If stalemate
		print()
		print("Stalemate. Game is a tie.")
	else: #If some other reason
		print()
		print("Something went wrong.")

play(100)

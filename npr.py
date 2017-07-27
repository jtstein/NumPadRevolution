# Jordan Stein
# npr.py
# github.com/jtstein

# This game currently runs on Linux, to run on Windows change 'clear' to 'cls' for the clear argument below
clear = 'clear' # change to 'cls' if using Windows
global emojis
emojis = ['<(o.o<)','<(o.o)>','(>o.o)>','^(o.o)^','v(o.o)v','^(o.o)v','v(o.o)^']
lastEmoji = -1

from random import randint
from threading import Thread
import time,readline,thread,sys,os

def rules():
	print "Welcome to NumPad Revolution\n"
	for emoji in emojis:
		print emoji,
	print "\n\nHow to play:"
	print "Hit the number present on the screen\nright before it hits the ground\n\n"
	
def menu():
	rules()
	difficulty = int(raw_input("Chose Game Difficulty:\n1) Very Easy\n2) Easy\n3) Medium\n4) Hard\n5) Impossible\n"))

	# returns the game speed (lower is faster)
	if difficulty == 1:
		return difficulty, 3
	elif difficulty == 2:
		return difficulty, 2
	elif difficulty == 3:
		return difficulty, 1
	elif difficulty == 4:
		return difficulty, .5
	elif difficulty == 5:
		return difficulty, .2

def printDancers(): # prints dancing emojis if you win the game
	delay = .01
	count = 0
	space = ''
	direction = 'right'

	def printEmoji(count, direction, space, emoji):
		time.sleep(delay) # delay for each emoji
		count += 1
		if direction == 'right': # add a space if emojis are dancing to the right
			space += ' '
		else:
			space = space[:-1] # remove the last space if emojis are dancing to the left
		print space + emoji # print emoji
		return count, space

	for x in range(0,90):
		print "				YOU WON				"
		for emoji in emojis: # print each emoji
			count, space = printEmoji(count, direction, space, emoji)

		if (count % 50 == 0 or count % 60 == 0 or count % 70 == 0): # change dancing direction
			if direction == 'right': # if going right, go left
				direction = 'left'
			else:
				direction = 'right' # if going left, go right
	print "Have a great day!			Press Ctrl+C to exit"

def printGame(moves,score,streak,moveCount,speed,hitAnimation,moveNum = 0):
	global lastEmoji
	os.system(clear) # clear screen
	rules() # print rules

	while True:
		randEmoji = randint(0,len(emojis)-1) # generate random emoji
		if randEmoji != lastEmoji: # make sure the emoji generated changes each game tick
			break
	lastEmoji = randEmoji

	print 'Score: {}	Streak: {}   Move: {}'.format(score, streak-1, moveCount) # print score data
	print '============== ' + emojis[randEmoji] + ' =============='	# print headline with random emoji
	for move in moves: # print all moves
		print move
	print '>>>>>>>>>>>>>>>>>><<<<<<<<<<<<<<<<<<<' # print footer

	if hitAnimation: # if we are printing the hit animation, quickly delay
		time.sleep(.1)
	else:
		time.sleep(speed) # otherwise, delay by the game speed


def game_thread(difficulty, speed):
	score = 0 # set initial score
	scoreToWin = 1000 # set score required to win game
	scoreMultiplier = 10*difficulty # set score multiplier
	streak = 1 # initialize hit streak
	missStreak = 1 # initialized miss streak
	moveCount = 0 # counts the total amount of moves
	moves = ["                                     ", # holds all moves
			 "                                     ",
			 "                                     ",
			 "                                     ",
			 "                                     ",
			 "                                     ",
			 "                                     "]
	while True: # main game loop
		numNumbers = 1
		if difficulty >= 3: # if medium or higher diffuculty
			if randint(0,2) == 2: # 1/3 chance to print multiple numbers per line
				numNumbers = 2
		newMove = '                                    ' # initiate the new move
		lastRand = -1
		randposition = -1
		for num in range(1,numNumbers+1): # generate numNumbers number of new numbers
			while randposition == lastRand:
				randposition = randint(0, len(newMove)) # generate random position for move
			lastRand = randposition
			rand = randint(0, 9) # generate random number for move
			newMove = newMove[:randposition] + str(rand) + newMove[randposition:] # store new move at position
		moves.insert(0,newMove) # insert new move into moves list
		moveCount += 1 # increment move count
		printGame(moves,score,streak,moveCount,speed,False,int(rand))
		inputBuffer = readline.get_line_buffer() # read input from buffer
		numNumbers = len(moves[7])-moves[7].count(' ') # calculate bottom lines numNumbers
		if moveCount >= 8: # only check for input after the first move hits the footer
			for num in range(1,numNumbers+1):
				if inputBuffer != '' and inputBuffer[-num] in moves[7]: # check if the last move in the buffer is in the most recent move
					streak += 1 # increment streak if hit
					missStreak = 1 # reset missed streak
					score += scoreMultiplier + int(streak) # adjust score
					index = moves[7].index(inputBuffer[-num])
					moves[7] = moves[7][:index] + str('*') + moves[7][index+1:]
					printGame(moves,score,streak,moveCount,speed,True,int(inputBuffer[-num])) # quickly print * where the number was
				else:
					streak = 1 # reset streak
					missStreak += 1 # increment missed streak
					score -= scoreMultiplier + 1.25*int(scoreMultiplier*(missStreak)) # adjust score
			if score < 0: # never let the score go below 0
				score = 0
			if score > scoreToWin:
				printDancers() # print the dancing win screen
				break
		inputBuffer = ' ' # reset inputBuffer
		sys.stdout.flush() # flush the buffer
		for num in range(0,numNumbers):
			readline.insert_text(':') # overwrite buffer
		if len(moves) > 7: # never allow the moves list to grow beyond 7
			moves = moves[:-1]

os.system(clear) # clear screen
difficulty, speed = menu() # print menu
thread.start_new_thread(game_thread, (difficulty,speed,)) # start game thread

while True:
	s = raw_input('') # constantly read from user

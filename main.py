import highscores

import os
import random
import sys
import time
import winsound



'''
-----TABLE OF CONTENTS-----

01. alp_to_int()
02. boxify()
03. clear()
04. demo_game()
05. init_board()
06. input_coord()
07. print_board()
08. quit_game()
09. reformat_coord()
10. start_game()
11. typing()
12. validate_input()
13. main()

-----END TABLE-----
'''


def alp_to_int(alphabet):
	"""Returns correct index for rows in alphabet."""
	alphabet = alphabet.lower() #ensures both upper & lower work
	ascii_val = ord(alphabet)
	if ascii_val >= 97 and ascii_val <= 100: #between 'a' and 'd'
		return ascii_val - 97
	else:
		return False


def boxify(elem):
	"""Pads elem with left and right border"""
	return '| ' + str(elem) + ' |'


def clear():
	"""Clears terminal"""
	os.system('cls' if os.name=='nt' else 'clear')


def demo_game():
	"""Basic instructions for how to play the game"""
	clear()
	board_star, board_game = init_board()
	print_board(board_star)

	typing('\nFirst, you enter the first set of coordinates. For example, "A, 1".', .07)
	time.sleep(1)

	print('\n>>> First set of coordinates: ', end='')
	time.sleep(2)
	typing('A, 1', .07)
	time.sleep(2)
	print()

	board_star[0][0] = board_game[0][0] #fetch num at 'A, 1'
	print_board(board_star)

	typing('\nNext, you enter the second set of coordinates. Let\'s go with "C, 3". ', .07)
	time.sleep(1)

	print('\n>>> Second set of coordinates: ', end='')
	time.sleep(2)
	typing('C, 3', .07)
	time.sleep(2)
	print()

	board_star[2][2] = board_game[2][2] #fetch num at 'C, 3'
	print_board(board_star)

	print('\nIf they are a match, then they will remain opened throughout the rest of the game.')
	demo_match = board_game[0][0] == board_game[2][2] #check if same
	if demo_match:
		print('\nIn this case, it is a match! Hurray!')
	else:
		print('Since they are different, they will be flipped back. Try to remember them. Quick! ')
		print('Refreshing in ', end='')
		for i in range(10,0,-1):
			print(str(i) + '..', end='',flush=True)
			time.sleep(1)
		clear()
		board_star[0][0] = '*'
		board_star[2][2] = '*'
		print_board(board_star)

	input('\nThat is it! Now, if you are ready, hit Enter to go back to the main menu.')


def init_board():
	"""
	Initialises board_game with random numbers,
	board_game is hidden from player, only board_star is updated
	"""
	x = [i for i in range(10)]*2 #generate 10 pairs of numbers
	random.shuffle(x)

	board_star = [['✶']*5 for i in range(4)] #output board
	board_game = [['']*5 for i in range(4)] #logic board

	for row in range(4):
		for col in range(5):
			board_game[row][col] = x.pop()

	return (board_star, board_game)


def input_coord(msg):
	"""
	Prompts player for coordinates, then reformats and validates them.
	Prompts again until correct format is entered.
	Returns formatted and validated coordinates.
	"""
	while True:
		user_input = input(msg)
		if user_input == 'q':
			quit_game() #quits anytime during gameplay
		coord = reformat_coord(user_input)
		if coord is False:
			print('Invalid coordinates. Try again!')
			continue
		else:
			return coord


def print_board(board):
	"""Prints board with borders and labels"""
	board_width = len(board[0]) * 5
	print('\n'+'Current Board\n'.center(board_width))

	#horizontal labels
	print('   ', end='')
	for i in range(1, 6):
		print('  '+str(i)+'  ', end='')
	print()

	i = 65 #ascii for 'A'
	for row in board:
		print('   ' + ' ___ '*len(row))
		print('   ' + '|   |'*len(row))
		print(' '+chr(i)+' ', end='') #vertical labels
		i += 1 #counter for labels
		for col in row:
			col = boxify(col) #pads with leftand right borders
			print(col, end='')
		print()
		print('   ' + '|___|'*len(row))


def quit_game():
	"""Exits game after a delay"""
	print('\nThank you and see you next time, adventurer.')
	time.sleep(3)
	sys.exit()


def reformat_coord(dirty_coord):
	"""Validates dirty_coord. Returns False if unaccepted."""
	if ',' not in dirty_coord:
		return False

	dirty_coord = [x.strip() for x in dirty_coord.split(',')]

	if len(dirty_coord) != 2: #makes sure no extra comma
		return False

	dirty_x, dirty_y = dirty_coord[0], dirty_coord[1]

	clean_x = validate_input('x', dirty_x)
	clean_y = validate_input('y', dirty_y)

	if clean_x is False or clean_y is False:
		return False

	return (clean_x, clean_y)


def start_game(board_star, board_game, my_highscore):
	"""Starts the game"""
	matched_nums = []
	game_ended = False
	start_time = time.time() # Start time counter

	while game_ended == False:
		# print_board(board_game) #for testing purpose
		print_board(board_star)

		coords_one = input_coord('\n>>> First set of coordinates: ') #First input
		num_one = board_game[coords_one[0]][coords_one[1]] #fetch num at coord

		while num_one in matched_nums: #if already guessed and matched
			print('You already have a match here, try again!')
			coords_one = input_coord('\n>>> First set of coordinates: ')
			num_one = board_game[coords_one[0]][coords_one[1]]

		board_star[coords_one[0]][coords_one[1]] = num_one
		print_board(board_star)

		coords_two = input_coord('\n>>> Second set of coordinates: ') #Second input
		num_two = board_game[coords_two[0]][coords_two[1]] #fetch num at coord

		while num_two in matched_nums: #if already guessed and matched
			print('You already have a match here, try again!')
			coords_two = input_coord('\n>>> Second set of coordinates: ')
			num_two = board_game[coords_two[0]][coords_two[1]]

		while coords_one == coords_two: #if both guesses at same location
			print('No guessing the same card, try again!')
			coords_two = input_coord('\n>>> Second set of coordinates: ')
			num_two = board_game[coords_two[0]][coords_two[1]]

		board_star[coords_two[0]][coords_two[1]] = num_two
		print_board(board_star)

		if num_one == num_two:
			matched_nums.append(num_one) #adds num to list of matched num
			winsound.PlaySound(dirname+'\\sfx\\correct.wav', winsound.SND_ASYNC | winsound.SND_LOOP) #correct sfx
			time.sleep(.5)
			winsound.PlaySound(dirname+'\\sfx\\bgm.wav', winsound.SND_ASYNC | winsound.SND_LOOP) #start bgm async
			print('\n>>> It is a match!', end=' ')
		else:
			board_star[coords_one[0]][coords_one[1]] = '✶'
			board_star[coords_two[0]][coords_two[1]] = '✶'
			print('\n>>> No match, try again!', end=' ')

		if len(matched_nums) == 10:
			game_ended = True #exits main loop
			end_time = time.time() #stops time counter
			winsound.PlaySound(dirname+'\\sfx\\finish.wav', winsound.SND_ASYNC) #play finish sfx
		else:
			print('Refreshing in ', end='')
			for i in range(5,0,-1):
				print(str(i) + '..', end='',flush=True)
				time.sleep(1)
			clear()


	player_score = round(end_time - start_time, 2)
	print('\nGame ended!')
	print('You took {} seconds.'.format(player_score))

	high_scores = my_highscore.get_highscores() #get current highscores

	for high_score in high_scores:
		if player_score < high_score['player_score']: #if player faster than any highscore
			index = high_scores.index(high_score) #gets index of next fastest highscore

			player_name = input('Congratulations! You are in the Top 10. Please tell me your name: ')
			high_scores.insert(index, {'player_name': player_name, 'player_score': player_score})
			high_scores.pop() #removes slowest highscore
			my_highscore.save_highscores(high_scores)
			my_highscore.print_highscores()
			break


def typing(msg, delay):
	"""Simulates typing using delay"""
	for letter in msg:
		print(letter, end='', flush=True)
		time.sleep(delay)


def validate_input(position, value):
	"""
	Ensures input in correct format. Returns False if unaccepted.
	Accepts two arg, position - (x/y), value - var at position
	"""
	if position == 'x':
		if value.isalpha():
			value = alp_to_int(value) #convert alphabet to int
			return value
		else:
			return False #not an alphabet
	if position == 'y':
		try:
			value = int(value)
		except ValueError:
			return False
		else:
			if value in range(1, 6):
				return(int(value) - 1) #produce correct index
			else:
				return False #not in board's range


def main():
	"""First function to be called"""
	my_highscore = highscores.Highscores(dirname+'\\highscores.json')

	while True:
		clear()
		welc_msg = ('''
	 _____  _____  _____  _____  _____  _____  _____                                      
	|   | ||  |  ||     || __  ||   __|| __  ||   __|                                     
	| | | ||  |  || | | || __ -||   __||    -||__   |                                     
	|_|___||_____||_|_|_||_____||_____||__|__||_____|                                     

	 _____  _____  _____  _____  _____  _____  _____  _____    _____  _____  _____  _____ 
	|     ||  _  ||_   _||     ||  |  ||     ||   | ||   __|  |   __||  _  ||     ||   __|
	| | | ||     |  | |  |   --||     ||-   -|| | | ||  |  |  |  |  ||     || | | ||   __|
	|_|_|_||__|__|  |_|  |_____||__|__||_____||_|___||_____|  |_____||__|__||_|_|_||_____|                   
			''')
		print(welc_msg)
		print('This is a simple number matching game that trains your memory.'+
			'\nFor each guess, the player enters the coordinates in the format "A, 0" to reveal a number.'+
			'\nEnter "q" anytime during the game to quit.')

		winsound.PlaySound(dirname+'\\sfx\\bgm.wav', winsound.SND_ASYNC | winsound.SND_LOOP) #start bgm async
		print('\n1 - {0}\t\t 2 - {1}\t\t 3 - {2}\t\t 4 - {3}\t\t 5 - {4}\t\t'.format('Start', 'Demo', 'Highscore', 'Delete Highscore', 'Quit')) #options
		option = input('Your choice: ')

		if option == '1':
			clear()
			board_star, board_game = init_board()
			start_game(board_star, board_game, my_highscore)
		elif option == '2':
			demo_game()
		elif option == '3':
			clear()
			my_highscore.print_highscores()
			input("\nPress Enter to go back to main menu.")
		elif option == '4':
			confirm = input('Are you sure you want to delete the highscore (Y/N)?').lower()
			if confirm == 'y':
				my_highscore.del_highscores()
		elif option == '5':
			quit_game()
		else:
			print('Choose from 1-5, try again.')
			time.sleep(2)


if __name__ == "__main__":
	dirname = os.path.abspath(os.path.join(os.path.realpath(__file__), '..')) #gets correct path regardless setup type
	main()
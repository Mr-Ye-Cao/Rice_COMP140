def play(board, player, num_moves):
	"""
	Input: board: a sequence consisting 8 different sequence
	              representing a 8x8 chess board where the individual
	              square on the board can be accessed by (row,col) where
	              row and col are integers and 0<=row<=7 0<=col<=7; also the board
	              at (row,col) is one of the following integers +1, -1, 0
	       player: an integer number either -1 or +1 indicating
	       		   red or black player correspondingly
	       		   is to play in the current configuration
	       num_moves: an integer number representing the total number of
	       			  moves ahead to check for both players
	Output: an indication of which play can win if either then return
			the "red" if red player can win or "black" if black player
			can win or "No One" if neither player can win
	"""
	if num_moves != 0:
		copy_board = []
		for seq in board:
			copy_board.append(list(seq))
		
		bool black_moved, red_moved = False, False
		if player == 1:
			for row_ind in range(8):
				for col_ind in range(8):
					if board[row_ind][col_ind] == 1:
						if col_ind == 0 or board[row_ind+1][col_ind-1] == 0:
							if col_ind != 7:
								if copy_board[row_ind+1][col_ind+1] == 0:
									black_moved = True
									copy_board[row_ind+1][col_ind+1] = 1
									copy_board[row_ind][col_ind] = 0
									result = play(copy_board, -1, num_moves-1)
									if result != "No One":
										return result
									copy_board[row_ind+1][col_ind+1] = 0
									copy_board[row_ind][col_ind] = 1
							if col_ind != 0:
								if copy_board[row_ind+1][col_ind-1] == 0:
									black_moved = True
									copy_board[row_ind+1][col_ind-1] = 1
									copy_board[row_ind][col_ind] = 0
									result = play(copy_board, -1, num_moves-1)
									if result != "No One":
										return result
									copy_board[row_ind+1][col_ind-1] = 0
									copy_board[row_ind][col_ind] = 1
			if black_moved == False:
				return "Red Wins"

		elif player == -1:
			for row_ind in range(8):
				for col_ind in range(8):
					if board[row_ind][col_ind] == -1:
						if col_ind == 7 or board[row_ind-1][col_ind+1] == 0:
							if col_ind != 0:
								if copy_board[row_ind-1][col_ind-1] == 0:
									red_moved = True
									copy_board[row_ind-1][col_ind-1] = -1
									copy_board[row_ind][col_ind] = 0
									result = play(copy_board, 1, num_moves-1)
									if result != "No One":
										return result
									copy_board[row_ind-1][col_ind-1] = 0
									copy_board[row_ind][col_ind] = -1
							if col_ind != 7:
								if copy_board[row_ind-1][col_ind+1] == 0:
									red_moved = True
									copy_board[row_ind-1][col_ind+1] = -1
									copy_board[row_ind][col_ind] = 0
									result = play(copy_board, 1, num_moves-1)
									if result != "No One":
										return result
									copy_board[row_ind-1][col_ind+1] = 0
									copy_board[row_ind][col_ind] = -1
			if red_moved == False:
				return "Black Wins"
	else:
		return "No One"

	return "No One"

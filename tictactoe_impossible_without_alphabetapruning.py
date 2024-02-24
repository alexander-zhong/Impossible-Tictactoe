# Utilities needed to run tictactoe impossible

import math
import copy

X = "X"
O = "O"


# Returns a set moves that are possible on the current board that has been inputted
def nextMoves(board):
    free_space = set()

    # Counter for rows
    counter = 0
    for row in board:

        # Counter for columns
        counter2 = 0
        
        # Iterates through the board to find empty spots
        for column in row:
            if column is None:
                free_space.add((counter, counter2))
            counter2 += 1
        counter += 1
    
    return free_space


# Checks if X is going or O is going
def whichTurn(board):
    num_X = 0
    num_O = 0
    turn = None

    for rows in board:
        num_X += rows.count(X)
        num_O += rows.count(O)

    if num_O == num_X:
        return X
    elif num_X > num_O:
        return O
    
    
# Returns the winner of the current board state
def winner(board):

    # Defining the horizontal win conditions
    horizontal_x_win = [X, X, X]
    horizontal_o_win = [O, O, O]

    # Checks horizontal wins 
    for row in board:
        if row == horizontal_x_win:
            return X
        elif row == horizontal_o_win:
            return O
        
    # Checks vertical wins & checks if one of them != None that means all of them are not == to None if the whole condition is true
    for column in range(3):
        if board[0][column] == board[1][column] and board[1][column] == board[2][column] and board[2][column] == board[0][column] and board[0][column] != None:
            return board[0][column]
        
    
    # Checks horizontal wins & checks if one of them != None that means all of them are not == to None if the whole condition is true
    if board[0][0] == board[1][1] and board[1][1] == board[2][2] and board[0][0] != None:
        return board[0][0]
    elif board[0][2] == board[1][1] and board[2][0] == board[1][1] and board[0][2] != None:
        return board[0][2]
    
    return None


# Returns true if the board game is finished, else false 
def finish(board):
    if winner(board) != None:
        return True
    
    for row in board:
        for cell in row:
            if cell == None:
                return False
    return True


# Returns the board after applying a move to the board inputted
def resultBoard(board, action):
    if board[action[0]][action[1]] != None:
        raise ValueError("Spot is already occupied")
    
    # Create a new independent copy of the board with new addition of the move/action performed
    new_board = copy.deepcopy(board)

    new_board[action[0]][action[1]] = whichTurn(board)
    
    return new_board


# Returns 1 if X won, -1 if O won and 0 if it is a tie (used to evaluate outcomes)
def state_evaluation(board):
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0
    


# Minimax algorithm used to determine the most optimal move (returns tuple of two values) (row, column) 
def minimax(board):
    current_player = whichTurn(board) 

    if finish(board) == True:
            return None

    if current_player == X:
        # Creates an infinitely small value
        game_value = -float('inf')
        
        best_move = None
        moves = nextMoves(board)
        
        # Loops over the possibilities 
        for move in moves:
            if move == None:
                break
            temp_game_value = min_value(resultBoard(board, move))
            if game_value < temp_game_value:
                best_move = move
                game_value = temp_game_value
        return best_move
    elif current_player == O:

        # Creates an infinitely large value
        game_value = float('inf')
        
    
        best_move = None
        moves = nextMoves(board)

        # Loops over the possibilities 
        for move in moves:
            if move == None:
                break
            temp_game_value = max_value(resultBoard(board, move))
            if game_value > temp_game_value:
                best_move = move
                game_value = temp_game_value

        return best_move

    

# Defining the max_value and min_value of the board

# Helper function for minimax to maximize values
def max_value(board):
    
    # Infinitely low value 
    game_value = -float('inf')
    
    # If board is finished return the value of the board
    if finish(board) == True:
        return state_evaluation(board)
    
    # Else, mutally recurse through the possible movesets to maximize the state evaluation
    for move in nextMoves(board):
        game_value = max(game_value, min_value(resultBoard(board, move)))

    return game_value
    


# Helper function for minimax to minimize values
def min_value(board):
    # Infinitely large value
    game_value = float('inf')
    
    # If board is finished return the value of the board
    if finish(board) == True:
        return state_evaluation(board)
    
    # Else, mutally recurse through the possible movesets to maximize the state evaluation
    for move in nextMoves(board):
        game_value = min(game_value, max_value(resultBoard(board, move)))
    return game_value
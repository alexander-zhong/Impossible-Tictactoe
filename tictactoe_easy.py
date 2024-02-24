# Utilities needed to run tictactoe easy - Same helper functions as impossible mode but with a heuristic function and a depth limited minimax with alpha beta pruning
import math
import copy
import random


# How far can our depth limited minimax go on into the arbitrary arity tree
MAX_DEPTH = 3

X = "X"
O = "O"

# How far can our depth limited minimax go on into the arbitrary arity tree
MAX_DEPTH = 3


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
    
    
# Heuristic Function (estimated value of the game board)
def heuristic_function(board):
    
    # Default board value is 0
    game_value = 0
    
    # Each possible win condition adds or substracts (depending if it is max player or min player) 0.042 to the game_value
    # There are 8 possible win conditions and 3 possible ways each to get to that win condition
    # (Example Win Condition of the top horizontal is [[O   , O   , None],
    #                                                  [None, None, None]
    #                                                  [None, None, None]]
    
    # There are 3 different ways to satisfy that [[O, O, None], [O, None, O], [O, None, O]]
    # There for, 8 win conditions and 3 ways to get to a win conditions, there are 24 different ways to get to a win condition. Winning is 1 or -1, we will divide 1 / 24 to ensure 
    # that a non-complete board will never get a value that positively/negatively exceeds a finished board that has a winner
    
    # Defining the horizontal possible win conditions for maximizing player
    horizontal_x_possible_win = [[X, X, None], [X, None, X], [None, X, X]]
    
    # Defining the horizontal possible win conditions for minimizing player
    horizontal_o_possible_win = [[O, O, None], [O, None, O], [O, None, O]]
    
    # Checks horizontal possible wins
    for row in board:
        if row in horizontal_x_possible_win:
            game_value += 0.042
        elif row == horizontal_o_possible_win:
            game_value += -0.042
        
    # Checks vertical possible wins
    for column in range(3):
        # Maximizing Player
        if board[0][column] == X and board[1][column] == X and board[2][column] == None:
            game_value += 0.042
        elif board[0][column] == X and board[1][column] == None and board[2][column] == X:
            game_value += 0.042
        elif board[0][column] == None and board[1][column] == X and board[2][column] == X:
            game_value += 0.042
            
        # Minimizing Player
        elif board[0][column] == O and board[1][column] == O and board[2][column] == None:
            game_value -= 0.042
        elif board[0][column] == O and board[1][column] == None and board[2][column] == O:
            game_value -= 0.042
        elif board[0][column] == None and board[1][column] == O and board[2][column] == O:
            game_value -= 0.042
        

    # Checks horizontal possible wins 
    
    
    # Maximizing Player for top left corner to bottom right corner
    if board[0][0] == X and board[1][1] == X and board[2][2] == None:
        game_value += 0.042
    elif board[0][0] == X and board[1][1] == None and board[2][2] == X:
        game_value += 0.042
    elif board[0][0] == X and board[1][1] == None and board[2][2] == X:
        game_value += 0.042
    # Minimizing Player for top left corner to bottom right corner
    elif board[0][0] == O and board[1][1] == O and board[2][2] == None:
        game_value -= 0.042
    elif board[0][0] == O and board[1][1] == None and board[2][2] == O:
        game_value -= 0.042
    elif board[0][0] == O and board[1][1] == None and board[2][2] == O:
        game_value -= 0.042
        
    
    # Maximizing Player for top right corner to bottom left corner        
    if board[0][2] == X and board[1][1] == X and board[2][0] == None:
        game_value += 0.042
    elif board[0][2] == X and board[1][1] == None and board[2][0] == X:
        game_value += 0.042
    elif board[0][2] == None and board[1][1] == X and board[2][0] == X:
        game_value += 0.042
    # Minimizing Player for top right corner to bottom left corner
    elif board[0][2] == O and board[1][1] == O and board[2][0] == None:
        game_value -= 0.042
    elif board[0][2] == O and board[1][1] == None and board[2][0] == O:
        game_value -= 0.042
    elif board[0][2] == None and board[1][1] == O and board[2][0] == O:
        game_value -= 0.042
    
    
    return game_value
    
    
    

    
# Depth Limited Minimax algorithm with alpha beta pruning used to determine the most optimal move (returns tuple)
def minimax(board):
    current_player = whichTurn(board) 

    # Setting the default alpha_value and beta_value for alpha beta pruning
    alpha_value = -float('inf')
    beta_value = float('inf')

    if finish(board):
            return None

    if current_player == X:
        # Creates an infinitely small value
        game_value = -float('inf')
        
        # Possible moves we can make
        moves = nextMoves(board)
        
        # Initialize at least one move will be chosen
        random_choice = random.choices(list(moves))
        best_move = random_choice[0]
 
        # Loops over the possibilities 
        for move in moves:
            if move == None:
                break
            temp_game_value = min_value(resultBoard(board,move), alpha_value, beta_value, 1)
            
            # Minimize the score and assigns new move
            if game_value < temp_game_value:
                best_move = move
                game_value = temp_game_value
                
            # Maximizes the alpha value and prunes branches if possible
            alpha_value = max(game_value, alpha_value)
            if alpha_value >= beta_value:
                break
            
        return best_move

    elif current_player == O:

        # Creates an infinitely large value
        game_value = float('inf')
    
        # Possible next moves    
        moves = nextMoves(board)
        
        # Initialize at least one move will be chosen
        random_choice = random.choices(list(moves))
        best_move = random_choice[0]
    
        # Loops over the possibilities 
        for move in moves:
            if move == None:
                break
            temp_game_value = max_value(resultBoard(board, move), alpha_value, beta_value, 1)
            
            # Maximizes the score and assigns new move
            if game_value > temp_game_value:
                best_move = move
                game_value = temp_game_value
                
            # Minimize the beta value and prunes branches if possible
            beta_value = min(game_value, beta_value)
            if alpha_value >= beta_value:
                break
            
        return best_move



# Defining the max_value and min_value of the board

# Helper function for minimax to maximize values
def max_value(board, alpha_value, beta_value, depth):
    
    # Infinitely low value 
    game_value = -float('inf')
    
    # If board is finished return the value of the board
    if finish(board):
        return state_evaluation(board)
    
    if depth >= MAX_DEPTH:
        return heuristic_function(board)
    
    moves = nextMoves(board)
    
    # Else, mutally recurse through the possible movesets to maximize the state evaluation
    for move in moves:
        temp_game_value = min_value(resultBoard(board, move), alpha_value, beta_value, depth + 1)
        
        if temp_game_value > game_value:
            game_value = temp_game_value
            
        # Maximizes the alpha value and prunes branches if possible
        alpha_value = max(game_value, alpha_value)
        if alpha_value >= beta_value:
            break
    
    return game_value
    

# Helper function for minimax to minimize values
def min_value(board, alpha_value, beta_value, depth):
    # Infinitely large value
    game_value = float('inf')

    
    # If board is finished return the value of the board
    if finish(board) == True:
        return state_evaluation(board)
    
    if depth >= MAX_DEPTH:
        return heuristic_function(board)
    
    moves = nextMoves(board)
    
    # Else, mutally recurse through the possible movesets to maximize the state evaluation
    for move in moves:
        temp_game_value = max_value(resultBoard(board, move), alpha_value, beta_value, depth + 1)
        
        if temp_game_value < game_value:
            game_value = temp_game_value
            
        # Minimize the beta value and prunes branches if possible
        beta_value = min(game_value, beta_value)
        if alpha_value >= beta_value:
            break

    return game_value
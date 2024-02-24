import pygame
import sys
import tictactoe_impossible_without_alphabetapruning as impossibleMode
import tictactoe_easy as easyMode
import time
# import tictactoe_easy as easyMode

pygame.init()

# Settings for the scene/window & font sizes & colors
WIDTH, HEIGHT = 500, 500
SCENE = pygame.display.set_mode((WIDTH, HEIGHT))

header_font = pygame.font.Font("arial.ttf", 36)
message_font = pygame.font.Font("arial.ttf", 20)
symbol_font = pygame.font.Font("arial.ttf", 80)

white = (255, 255, 255)
black = (0, 0, 0)
bright_green = (170, 255, 0)
bright_red =  (238, 75, 43)
gold = (255, 215, 0)

# The symbols that the users and AI will use
user = None
ai = None
user_turn = True
X = "X"
O = "O"

# Winning line drawn? 
line_drawn = False

# Two dimension list to represent the board 
current_board = [[None, None, None],
                 [None, None, None],
                 [None, None, None]]

# Difficulty of the game will determine which algorithms will be used
difficulty = None

# Functions for generating texts and buttons
def buttonMaker(rect, button_text, text_color):
    pygame.draw.rect(SCENE, white, rect)
    button_text = message_font.render(button_text, True, text_color)
    button_text_rect = button_text.get_rect(center=rect.center)
    SCENE.blit(button_text, button_text_rect)
    
# Function for making a text appear
def textMaker(message, dimension, large):
    display_text = None
    if large:
        display_text = header_font.render(message, True, white)
    else:
        display_text = message_font.render(message, True, white)
    display_text_rect = display_text.get_rect()
    display_text_rect.center = dimension    
    SCENE.blit(display_text, display_text_rect)


# Function for drawing the grid
def makeBoard(board):
    # Draw two lines of both horizontal and vertical
    for x in [1, 2]:
        # Drawing Horizontal Lines
        pygame.draw.line(SCENE, white, (0, x * HEIGHT / 3), (WIDTH, x * HEIGHT / 3), 3)
        # Drawing Vertical Lines
        pygame.draw.line(SCENE, white, (x * WIDTH / 3, 0), (x * WIDTH / 3, HEIGHT), 3)
    
    # Drawing the Xs and Os on the board
    
    # The current coordinates 
    current_x = 0
    current_y = 0
    for row in board:
        for cell in row:
            if cell is None:
                pass
            else:
                symbolPlacer(current_x, current_y)
            current_x += 1
        current_x = 0
        current_y += 1

# Places the correct symbols onto the screen based on current coordinates (coordinates must be within domain of [1, 3] and integers)
def symbolPlacer(x, y):
    symbol = symbol_font.render(current_board[y][x], True, white)
    symbol_rect = symbol.get_rect(center=((x + .5) * WIDTH / 3, (y + .5) * HEIGHT / 3))
    SCENE.blit(symbol, symbol_rect)
    
    
# Draws the winning line of the section that was won
def winningLine(board):
        # Defining the horizontal win conditions
    horizontal_x_win = [X, X, X]
    horizontal_o_win = [O, O, O]

    # Checks horizontal wins 
    row_counter = 0
    for row in board:
        if row == horizontal_x_win or row == horizontal_o_win:
            pygame.draw.line(SCENE, gold, (20 ,((row_counter + 0.5) * HEIGHT / 3)), (WIDTH - 20 ,((row_counter + 0.5) * HEIGHT / 3)), 2)
            return None
        row_counter += 1       
        
    # Checks vertical wins
    for column in range(3):
        if board[0][column] == board[1][column] and board[1][column] == board[2][column] and board[2][column] == board[0][column] and board[0][column] != None:
            pygame.draw.line(SCENE, gold, (((column + 0.5) * WIDTH / 3), 20), (((column + 0.5) * HEIGHT / 3), HEIGHT - 20), 2)
            return None
        
    
    # Checks horizontal wins & checks if one of them != None
    if board[0][0] == board[1][1] and board[1][1] == board[2][2] and board[0][0] != None:
        pygame.draw.line(SCENE, gold, (20, 20), (WIDTH - 20, HEIGHT - 20))
        return None
    elif board[0][2] == board[1][1] and board[2][0] == board[1][1] and board[0][2] != None:
        pygame.draw.line(SCENE, gold, (WIDTH - 20, 20), (20, HEIGHT - 20))
        return None
    
    return None


# Inserts symbol if it is none at that location
def symbolInserter(row, column):
    if current_board[row][column] != None:
        return False
    else:
        current_board[row][column] = user


# Running the game
running = True

while running:    

    # Allows the screen to refresh
    SCENE.fill(black)
            
    # Start off menu
    if difficulty is None:
        
        # Welcome Message
        welcome_message = "Welcome to TicTacToe!"
        textMaker(welcome_message, (WIDTH / 2, HEIGHT / 4), True) 
    
        # Instruction Message
        instruction_message = "Please Select the Difficulty Level:"
        textMaker(instruction_message, (WIDTH / 2, HEIGHT / 3), False) 
        
        # Buttons
        easy_button_rect = pygame.Rect(WIDTH / 4 - 20, HEIGHT / 2, 100, 50)
        buttonMaker(easy_button_rect, "Easy", bright_green)
        impossible_button_rect = pygame.Rect(WIDTH - (WIDTH / 2.7) - 10, HEIGHT / 2, 100, 50)
        buttonMaker(impossible_button_rect, "Impossible", bright_red)
    
        # Event Listener for button clicks of difficulty
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if easy_button_rect.collidepoint(event.pos):
                    difficulty = "easy"
                elif impossible_button_rect.collidepoint(event.pos):
                    difficulty = "impossible"
    
    # User Selects to be X or O
    elif user is None:
        # Welcome Message
        welcome_message = "Welcome to TicTacToe!"
        textMaker(welcome_message, (WIDTH / 2, HEIGHT / 4), True) 
    
        # Instruction Message
        instruction_message = "Please Select X or O"
        textMaker(instruction_message, (WIDTH / 2, HEIGHT / 3), False) 
        
        o_button_rect = pygame.Rect(WIDTH / 4 - 20, HEIGHT / 2, 100, 50)
        buttonMaker(easy_button_rect, "Play as O", black)
        x_button_rect = pygame.Rect(WIDTH - (WIDTH / 2.7) - 10, HEIGHT / 2, 100, 50)
        buttonMaker(impossible_button_rect, "Play as X", black)
    
        
        # Event Listener for button clicks of X or Os
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if o_button_rect.collidepoint(event.pos):
                    user = O
                    ai = X
                elif x_button_rect.collidepoint(event.pos):
                    user = X
                    ai = O
    else:
        makeBoard(current_board)
        
        if difficulty == "impossible":
            
            # Checking for winners
            winner = impossibleMode.winner(current_board)
            
            if winner != None:
                if winner == user:
                    SCENE.fill(bright_green)
                    makeBoard(current_board)
                    winningLine(current_board)
                    winning_message = "You have won!"
                    winning_text = header_font.render(winning_message, True, black)
                    winning_rect = winning_text.get_rect(center=((WIDTH/2), (HEIGHT/2)))
                    pygame.draw.rect(SCENE, white, (WIDTH/2 - 125, HEIGHT/2 - 50 , 250, 100))
                    SCENE.blit(winning_text, winning_rect)
                elif winner == ai:
                    SCENE.fill(bright_red)
                    makeBoard(current_board)
                    winningLine(current_board)
                    winning_message = "You have lost!"
                    winning_text = header_font.render(winning_message, True, black)
                    winning_rect = winning_text.get_rect(center=((WIDTH/2), (HEIGHT/2)))
                    pygame.draw.rect(SCENE, white, (WIDTH/2 - 125, HEIGHT/2 - 50 , 250, 100))
                    SCENE.blit(winning_text, winning_rect)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        
            elif impossibleMode.finish(current_board):
                makeBoard(current_board)
                winning_message = "Its a tie!"
                winning_text = header_font.render(winning_message, True, black)
                winning_rect = winning_text.get_rect(center=((WIDTH/2), (HEIGHT/2)))
                pygame.draw.rect(SCENE, white, (WIDTH/2 - 125, HEIGHT/2 - 50 , 250, 100))
                SCENE.blit(winning_text, winning_rect)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        
            else:     
                # Checks if it's user's turn
                if user == impossibleMode.whichTurn(current_board):
                    user_turn = True
                else:
                    user_turn = False
                
                # AI Turn
                if user_turn == False:
                    best_move = impossibleMode.minimax(current_board)
                    if current_board[best_move[0]][best_move[1]] != None:
                        raise ValueError
                    makeBoard(current_board)
                    time.sleep(.25)
                    
                    # Prints Ai Computing Message (Add dots every 0.25 seconds)
                    for x in [1, 2, 3]:
                        dots = ""
                        for y in range(x):
                            dots = dots + "."
                        loading_message = "AI Computing" + dots
                        loading_text = header_font.render(loading_message, True, black)
                        loading_text_rect = loading_text.get_rect(center=((WIDTH/2), (HEIGHT/2)))
                        pygame.draw.rect(SCENE, white, (WIDTH/2 - 125, HEIGHT/2 - 50 , 250, 100))
                        SCENE.blit(loading_text, loading_text_rect)
                        pygame.display.flip()
                        time.sleep(0.25)
                    time.sleep(.25)
                    current_board[best_move[0]][best_move[1]] = ai
                    
                # User Turn
                else:
                    # Defining each boxes for users to click onto
                
                    # Row 1
                    rect00 = pygame.Rect(0, 0, WIDTH / 3, HEIGHT / 3)
                    rect01 = pygame.Rect((WIDTH / 3), 0, (WIDTH / 3), HEIGHT / 3)
                    rect02 = pygame.Rect(2 * (WIDTH / 3), 0, (WIDTH / 3), HEIGHT / 3)
                
                    # Row 2
                    rect10 = pygame.Rect(0, HEIGHT / 3, (WIDTH / 3), HEIGHT / 3)
                    rect11 = pygame.Rect((WIDTH / 3), HEIGHT / 3, (WIDTH / 3), HEIGHT / 3)
                    rect12 = pygame.Rect(2 * (WIDTH / 3), HEIGHT / 3, (WIDTH / 3), HEIGHT / 3)
                
                    # Row 3
                    rect20 = pygame.Rect(0, 2 * (HEIGHT / 3), (WIDTH / 3), HEIGHT / 3)
                    rect21 = pygame.Rect((WIDTH / 3), 2 * (HEIGHT / 3), (WIDTH / 3), HEIGHT / 3)
                    rect22 = pygame.Rect(2 * (WIDTH / 3), 2 * (HEIGHT / 3), (WIDTH / 3), HEIGHT / 3)
                
                
                    # Event listener
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                        # inserts a symbol if there is a space
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if rect00.collidepoint(event.pos):
                               symbolInserter(0, 0)
                            elif rect01.collidepoint(event.pos):
                                symbolInserter(0, 1)
                            elif rect02.collidepoint(event.pos):
                                symbolInserter(0, 2)
                            elif rect10.collidepoint(event.pos):
                                symbolInserter(1, 0)
                            elif rect11.collidepoint(event.pos):
                                symbolInserter(1, 1)
                            elif rect12.collidepoint(event.pos):
                                symbolInserter(1, 2)
                            elif rect20.collidepoint(event.pos):
                                symbolInserter(2, 0)
                            elif rect21.collidepoint(event.pos):
                                symbolInserter(2, 1)
                            elif rect22.collidepoint(event.pos):
                                symbolInserter(2, 2)
                    makeBoard(current_board)
        
        
        # Easy mode
        elif difficulty == "easy":
            # Checking for winners
            winner = easyMode.winner(current_board)
            
            # Winner Menus for the winners of the game
            if winner != None:
                if winner == user:
                    SCENE.fill(bright_green)
                    makeBoard(current_board)
                    winningLine(current_board)
                    winning_message = "You have won!"
                    winning_text = header_font.render(winning_message, True, black)
                    winning_rect = winning_text.get_rect(center=((WIDTH/2), (HEIGHT/2)))
                    pygame.draw.rect(SCENE, white, (WIDTH/2 - 125, HEIGHT/2 - 50 , 250, 100))
                    SCENE.blit(winning_text, winning_rect)

                elif winner == ai:
                    SCENE.fill(bright_red)
                    makeBoard(current_board)
                    winningLine(current_board)
                    winning_message = "You have lost!"
                    winning_text = header_font.render(winning_message, True, black)
                    winning_rect = winning_text.get_rect(center=((WIDTH/2), (HEIGHT/2)))
                    pygame.draw.rect(SCENE, white, (WIDTH/2 - 125, HEIGHT/2 - 50 , 250, 100))
                    SCENE.blit(winning_text, winning_rect)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
            # Tie menu if the game reached a tie
            elif easyMode.finish(current_board):
                makeBoard(current_board)
                winning_message = "Its a tie!"
                winning_text = header_font.render(winning_message, True, black)
                winning_rect = winning_text.get_rect(center=((WIDTH/2), (HEIGHT/2)))
                pygame.draw.rect(SCENE, white, (WIDTH/2 - 125, HEIGHT/2 - 50 , 250, 100))
                SCENE.blit(winning_text, winning_rect)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
            else:     
                # Checks if it's user's turn
                if user == easyMode.whichTurn(current_board):
                    user_turn = True
                else:
                    user_turn = False
                
                # AI Turn
                if user_turn == False:
                    best_move = easyMode.minimax(current_board)
                    if current_board[best_move[0]][best_move[1]] != None:
                        raise ValueError("There are no best moves available")
                    makeBoard(current_board)
                    time.sleep(.25)
                    
                    for x in [1, 2, 3]:
                        dots = ""
                        for y in range(x):
                            dots = dots + "."
                        loading_message = "AI Computing" + dots
                        loading_text = header_font.render(loading_message, True, black)
                        loading_text_rect = loading_text.get_rect(center=((WIDTH/2), (HEIGHT/2)))
                        pygame.draw.rect(SCENE, white, (WIDTH/2 - 125 - ((x - 1) * 10)/2, HEIGHT/2 - 50 , 250 + ((x - 1) * 10), 100))
                        SCENE.blit(loading_text, loading_text_rect)
                        pygame.display.flip()
                        time.sleep(0.25)
                    time.sleep(.25)
                    current_board[best_move[0]][best_move[1]] = ai
                    
                # User Turn
                else:
                    # Defining each boxes
                
                    # Row 1
                    rect00 = pygame.Rect(0, 0, WIDTH / 3, HEIGHT / 3)
                    rect01 = pygame.Rect((WIDTH / 3), 0, (WIDTH / 3), HEIGHT / 3)
                    rect02 = pygame.Rect(2 * (WIDTH / 3), 0, (WIDTH / 3), HEIGHT / 3)
                
                    # Row 2
                    rect10 = pygame.Rect(0, HEIGHT / 3, (WIDTH / 3), HEIGHT / 3)
                    rect11 = pygame.Rect((WIDTH / 3), HEIGHT / 3, (WIDTH / 3), HEIGHT / 3)
                    rect12 = pygame.Rect(2 * (WIDTH / 3), HEIGHT / 3, (WIDTH / 3), HEIGHT / 3)
                
                    # Row 3
                    rect20 = pygame.Rect(0, 2 * (HEIGHT / 3), (WIDTH / 3), HEIGHT / 3)
                    rect21 = pygame.Rect((WIDTH / 3), 2 * (HEIGHT / 3), (WIDTH / 3), HEIGHT / 3)
                    rect22 = pygame.Rect(2 * (WIDTH / 3), 2 * (HEIGHT / 3), (WIDTH / 3), HEIGHT / 3)
                
                    # Event listener
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            running = False
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            if rect00.collidepoint(event.pos):
                               symbolInserter(0, 0)
                            elif rect01.collidepoint(event.pos):
                                symbolInserter(0, 1)
                            elif rect02.collidepoint(event.pos):
                                symbolInserter(0, 2)
                            elif rect10.collidepoint(event.pos):
                                symbolInserter(1, 0)
                            elif rect11.collidepoint(event.pos):
                                symbolInserter(1, 1)
                            elif rect12.collidepoint(event.pos):
                                symbolInserter(1, 2)
                            elif rect20.collidepoint(event.pos):
                                symbolInserter(2, 0)
                            elif rect21.collidepoint(event.pos):
                                symbolInserter(2, 1)
                            elif rect22.collidepoint(event.pos):
                                symbolInserter(2, 2)
                    makeBoard(current_board)
                
                
        # Updates the screen and controlling the frame rate
    pygame.display.flip()
    pygame.time.Clock().tick(30)
        
# Clean up resources and quit
pygame.quit()
            
            

            
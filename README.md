# Impossible-Tictactoe

## Description
A game that is built on pygame where the users can select which symbol to play as (X or O) as well as the difficulty level of the AI that they will be facing. In this game, there would be two AIs that are available, easy and impossible. 

### Date:
Built during summer of 2023 

### Types of AIs

#### Impossible mode 
The hardest and impossible AI that can be beaten. Using the minimax algorithm to find the optimal move as well as alpha-beta pruning for efficiency and runtime purposes, the AI will be able to find the most optimal move on the board that will either lead to a tie or a win for the AI.

#### Easy Mode
This AI will be using the depth-limited minimax algorithm as well as alpha-beta pruning for efficiency. I have introduced a heuristic function that allows the AI to evaluate the game state without it being fully finished and placed a limit (depth-limited minimax) on how far the AI is allowed to calculate within the arbitrary arity tree of game states to find the most optimal moves that the AI can take to reach its desired game state. This will easily decrease the difficulty of the AI and allow users to finally have a chance to beat it.

Note: The easy mode is adjustable within the code. In the file, "tictactoe_easy.py", the global variable MAX_DEPTH on line 8, as you increase the number, the AI gets to see more game states and becomes more difficult to beat but as you decrease the MAX_DEPTH, it will allow the AI to look at fewer game states meaning, it becomes more increasingly easy to defeat.

## How to run
Run "python3 game.py" in the terminal to start the game. 
Please Ensure that pygame is installed

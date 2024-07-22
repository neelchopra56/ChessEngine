# Python Chess Engine

## Introduction
Chess is a board game for two players, called White and Black, each controlling an army of chess pieces, with the objective to checkmate the opponent's king. <br>

## Project Description
This project is a chess game implemented in Python. It uses the Pygame library for the graphical user interface, allowing players to interact with the game using mouse clicks. The game supports both human vs human and human vs AI modes. The chessboard is represented as an 8x8 2D list, with each element containing two characters representing the piece color and type. It keeps track of the current state, including the positions of all pieces, the player whose turn it is, and the log of all moves made. It also supports special chess moves such as castling, en-passant, and pawn promotion. When a pawn reaches the other side of the board, it is automatically promoted to a queen.
The game checks for checkmate and stalemate conditions after each move. If either condition is met, it ends and a message is displayed indicating the result. It also includes an undo feature, allowing players to take back their last move. This is done by removing the last move from the move log and reverting It state to what it was before that move. Algorithms are used by AI and are crucial in this project as they allow the AI to make intelligent decisions based on the current state of the game. They enable the AI to look ahead and evaluate the consequences of its moves, leading to more strategic gameplay. It also includes a move log panel that displays a history of all moves made during It in standard chess notation. This panel is updated after each move.
The game's settings are configurable, including the dimensions of the chessboard and the move log panel, the frame rate, and the image files used for the chess pieces.

## Algorithms 
**1. MiniMax Algorithm:** The MinMax algorithm is a decision-making algorithm used for minimizing the worst-case scenario or maximizing the best-case scenario. It is used in two-player games such as chess, where each player tries to minimize the maximum benefit of their opponent. In this project, the MinMax algorithm is used to evaluate the best move for the current player by considering all possible future game states up to a certain depth.<br>
**2. NegaMax Algorithm:** NegaMax is a simplification of the MinMax algorithm that relies on the zero-sum property of two-player games. This means that any positive change for one player is an equal negative change for the other player. In this project, the NegaMax algorithm is used to simplify the evaluation of the best move by considering all possible future game states up to a certain depth from the perspective of the current player.<br>
**3. MiniMax with AlphaBeta Pruning:** AlphaBeta pruning is an optimization technique for the MinMax algorithm. It reduces the number of nodes that need to be evaluated in the game tree by eliminating branches that do not need to be explored. This is done by maintaining two values, alpha and beta, which represent the minimum score that the maximizing player is assured of and the maximum score that the minimizing player is assured of, respectively. In this project, the MinMax algorithm with AlphaBeta pruning is used to improve the efficiency of the AI by reducing the number of moves it needs to evaluate.<br><br>
These algorithms are crucial in this project as they allow the AI to make intelligent decisions based on the current state of the game. They enable the AI to look ahead and evaluate the consequences of its moves, leading to more strategic gameplay.


## Learnt from 
[YouTube channel](https://www.youtube.com/channel/UCaEohRz5bPHywGBwmR18Qww)

[First episode of "Chess engine in Python"](https://www.youtube.com/watch?v=EnYui0e73Rs&ab_channel=EddieSharick)

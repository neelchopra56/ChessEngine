'''
Main Driver File
Handles User Input and Displaying the Current Game State object.
'''
import pygame as p
import ChessEngine
import ChessAI
import os
from multiprocessing import Process, Queue


WIDTH = HEIGHT = 512
MOVE_LOG_PANEL_WIDTH = 250  
MOVE_LOG_PANEL_HEIGHT = HEIGHT  

Dimension = 8
sq_size = HEIGHT // Dimension 
Max_FPS = 15

images = {} 

'''

Global Dictionary of Images. +

To be called exactly once
'''

def loadImages():
    os.chdir(r'C:/Users/HP Pavilion/Desktop/Chess/Engine/Chess/')
    
    pieces = ['wp', 'bp','wR','bR','wN','bN','wQ','bQ','wK','bK','wB','bB']
    for piece in pieces:
        try:
            images[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (sq_size, sq_size))
        except Exception as e:
            print(f"Error loading image for {piece}: {str(e)}")
'''
Handling User Inputs and Updating the graphics+
'''
def main():
    p.init()
    screen = p.display.set_mode((WIDTH + MOVE_LOG_PANEL_WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    moveLogFont = p.font.SysFont('Arial', 15, False, False)
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False #flag variable for when the move is made 
    loadImages() #Doing this once 
    running = True
    sqSelected = () #keep track of last tick of the user (tuple: row, col)
    playerClicks = [] #Initial and next click
    animate = False #Flag variable when we should animate a move
    gameOver = False #Flag variable for when game is over
    playerOne = True #If a human is playing white, then this will be true, if ai is white, false
    playerTwo = True #Same for black
    AIThinking = False #True when AI is thinking
    moveFinderProcess = None

    while running:
        humanTurn = (gs.whiteToMove and playerOne) or (not gs.whiteToMove and playerTwo)
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
 
            #mouse handler 
            
            elif e.type == p.MOUSEBUTTONDOWN:
                if not gameOver and humanTurn:
                    location = p.mouse.get_pos() #(x,y) location ofthe mouse
                    col = location[0]//sq_size
                    row = location[1]//sq_size
                    if sqSelected == (row, col) or col >= 8: #Same square selected twice or clicked mouse log    
                        sqSelected =() #deselect
                        playerClicks = []
                    else: 
                        sqSelected =(row,col)
                        playerClicks.append(sqSelected)
                    
                    if len(playerClicks) == 2 :
                        move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                        print(move.getChessNotation())
                        for i in range(len(validMoves)):
                            if move == validMoves[i]:
                                gs.makeMove(validMoves[i])  
                                moveMade = True
                                animate = True
                                sqSelected = () #reset user clicks
                                playerClicks = []

                        if not moveMade:
                            playerClicks = [sqSelected]

                   

            #key handler
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: 
                    gs.undoMove()
                    moveMade = True
                    animate = False
                    gameOver = False
                
                if e.key == p.K_ESCAPE:
                    gs =ChessEngine.GameState()
                    validMoves = gs.getValidMoves()
                    sqSelected = ()
                    playerClicks = []
                    moveMade = False 
                    animate = False
                    gameOver = False

                if move.isPawnPromotion:
                    if e.key == p.K_q:
                        gs.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'
                        moveMade = True
                    elif e.key == p.K_r:
                        gs.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'R'
                        moveMade = True
                    elif e.key == p.K_b:
                        gs.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'B'
                        moveMade = True
                    elif e.key == p.K_n:
                        gs.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'N'
                        moveMade = True
        
        if moveMade:
            if animate:
                animateMoves(gs.moveLog[-1], screen, gs.board, clock)
            validMoves = gs.getValidMoves()
            moveMade = False
            animate = False

        #AI move finder
        if not gameOver and not humanTurn:
            AIMove = ChessAI.findBest(gs, validMoves)
            if AIMove is None:
                AIMove = ChessAI.findRandomMoves(validMoves)
            gs.makeMove(AIMove)
            moveMade = True
            animate = True
            
        #             #AI move finder
        # if not gameOver and not humanTurn:
        #     if not AIThinking:
        #         AIThinking = True
        #         print('Thinking...')
        #         returnQueue = Queue() #Pass data between threads
        #         moveFinderProcess = Process(target=ChessAI.findBest, args=(gs, validMoves, returnQueue))
        #         moveFinderProcess.start() #call findBestMove(gs, validMoves, returnQueue)
            
        #     if not moveFinderProcess.is_alive():
        #         print("done thinking...")
        #         AIMove = returnQueue.get()
        #         AIMove = ChessAI.findBest(gs, validMoves, returnQueue)
        #         if AIMove is None:
        #             AIMove = ChessAI.findRandomMoves(validMoves)
        #         gs.makeMove(AIMove)
        #         moveMade = True
        #         animate = True
        #         AIThinking = False

        

        drawGameState(screen, gs, validMoves, sqSelected, moveLogFont)

        if gs.checkMate or gs.checkMate:
            gameOver = True
            if gs.staleMate:
                text = 'Stalemate'
            else:
                text = 'Black wins by CheckMate' if gs.whiteToMove else 'White wins by CheckMate'
            drawEndGametext(screen, text)
        clock.tick(Max_FPS)

        p.display.flip()



def drawGameState(screen, gs, validMoves, sqSelected, moveLogFont):
    drawBoard(screen) #draw squares on the board
    highlightSquares(screen, gs, validMoves, sqSelected)
    drawPieces(screen, gs.board) #draw pieces
    drawMoveLog(screen, gs, moveLogFont)




def drawBoard(screen):
    global colors
    colors = [p.Color("white"), p.Color("grey")]
    for r in  range(Dimension):
        for c in range(Dimension):
            color = colors[((r+c)%2)] 
            p.draw.rect(screen, color, p.Rect(c*sq_size, r*sq_size, sq_size, sq_size))


'''
Highlight square selected and moves for piece selected.
'''
def highlightSquares(screen, gs, validMoves, sqSelected):   
    if sqSelected != ():
        r,c  = sqSelected
        if gs.board[r][c][0] ==('w' if gs.whiteToMove else 'b'): #square selected is a piece that can be moved
            #highlighting the square selected
            s = p.Surface((sq_size, sq_size))
            s.set_alpha(100) #Transperancy value 
            s.fill(p.Color('blue'))
            screen.blit(s, (c*sq_size, r*sq_size))
            #highlight moves from that square
            s.fill(p.Color('yellow'))
            for move in validMoves:
                if move.startRow == r and move.startCol == c:
                    screen.blit(s, (move.endCol*sq_size, move.endRow*sq_size))



def drawPieces(screen, board):
    for r in range(Dimension):
        for c in range(Dimension):
            piece = board[r][c]
            if piece != "--": # piece is not empty
                if piece in images:  # Check if piece is a valid key in the images dictionary
                    screen.blit(images[piece], p.Rect(c * sq_size, r * sq_size, sq_size, sq_size))
                else:
                    print(f"Invalid piece: {piece}")

'''
Draws the Move Log
'''
def drawMoveLog(screen, gs, font):
    
    moveLogRect = p.Rect(WIDTH, 0, MOVE_LOG_PANEL_WIDTH, MOVE_LOG_PANEL_HEIGHT)
    p.draw.rect(screen, p.Color("black"), moveLogRect)
    moveLog = gs.moveLog
    moveTexts = []
    for i in range(0, len(moveLog), 2):
        moveString = str(i//2 + 1) + ". " + moveLog[i].getChessNotation() + " "
        if i+1 < len(moveLog): #Making Sure Black Has Made A Move
            moveString += " " + moveLog[i+1].getChessNotation()
        moveTexts.append(moveString)


    movesPerRow = 3
    padding = 5
    textY = padding

    for i in range(0, len(moveTexts), movesPerRow):
        text = ""
        for j in range(movesPerRow):
            if i + j < len(moveTexts):
                text += moveTexts[i + j]
        textObject = font.render(text, True, p.Color('white'))
        textLocation =moveLogRect.move(padding, textY)
        screen.blit(textObject, textLocation)
        textY += textObject.get_height() + padding

'''
Animating Moves
'''

# def animateMoves(move, screen, board, clock):
#     global colors
#     coords = [] #List of co-ordinates that the animation will move through
#     dR = move.endRow - move.startRow
#     dC = move.endCol - move.startCol
#     framesPerSquare = 10 #Frames moved per animation
#     frameCount = (abs(dR) + abs(dC))*framesPerSquare
#     for frame in range(frameCount + 1):
#         r,c = (move.startRow + dR*frame/frameCount, move.startCol + dC*frame/frameCount)
#         drawBoard(screen)
#         drawPieces(screen, board)
#     #erase piece moved from it ending square
#     color = colors[(move.endRow + move.endCol)%2]
#     endSquare = p.Rect(move.endCol*sq_size, move.endRow*sq_size, sq_size, sq_size)
#     p.draw.rect(screen, color, endSquare)
#     #Draw Captured Piece onto the rectangle
#     if move.pieceCaptured != '--':
#         screen.blit(images[move.pieceCaptured], endSquare)
#     #Draw the moving Piece
#     screen.blit(images[move.pieceMoved], p.Rect(c*sq_size, r*sq_size, sq_size, sq_size))
#     p.display.flip()
#     clock.tick(60)

def animateMoves(move, screen, board, clock):
    global colors
    coords = [] #List of co-ordinates that the animation will move through
    dR = move.endRow - move.startRow
    dC = move.endCol - move.startCol
    framesPerSquare = 4 #Frames moved per animation
    frameCount = (abs(dR) + abs(dC))*framesPerSquare

    for frame in range(frameCount + 1):
        r,c = (move.startRow + dR*frame/frameCount, move.startCol + dC*frame/frameCount)
        drawBoard(screen)
        drawPieces(screen, board)
        #erase piece moved from it ending square
        color = colors[(move.endRow + move.endCol)%2]
        endSquare = p.Rect(move.endCol*sq_size, move.endRow*sq_size, sq_size, sq_size)
        p.draw.rect(screen, color, endSquare)
        #Draw Captured Piece onto the rectangle
        if move.pieceCaptured != '--':
            if move.isEnpassantMove:
                enPassantRow = (move.endRow + 1) if move.pieceCaptured[0] == 'b' else move.endRow - 1
                endSquare = p.Rect(move.endCol*sq_size, enPassantRow*sq_size, sq_size, sq_size)


            screen.blit(images[move.pieceCaptured], endSquare)
        #Draw the moving Piece 
        screen.blit(images[move.pieceMoved], p.Rect(c*sq_size, r*sq_size, sq_size, sq_size))
        p.display.flip()
        clock.tick(60)

def drawEndGametext(screen, text):
    font = p.font.SysFont('Helvitca', 45, False, False)
    textObject = font.render(text, 0, p.Color('Dark Blue'))
    textLocation = p.Rect(0,0, WIDTH, HEIGHT).move(WIDTH/2 - textObject.get_width()/2, HEIGHT/2 - textObject.get_height()/2)
    screen.blit(textObject, textLocation)
    

if __name__ == "__main__":
    main()



















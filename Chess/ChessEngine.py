'''
This Class is responsiblle for storing all the info of the current state and determining the valid moves at the current state.
Will Also keep a move log 
'''


class GameState():
    def __init__(self):
        # 8*8 2D list and each element with 2 chars, piece color and piece type, '--' : Empty String
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]

        ]

        self.moveFunctions = {
            "p": self.getPawnMoves,
            "R": self.getRookMoves,
            "N": self.getKnightMoves,
            "Q": self.getQueenMoves,
            "K": self.getKingMoves,
            "B": self.getBishopMoves,


        }

        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7,4) 
        self.blackKingLocation = (0,4) 
        self.checkMate = False
        self.staleMate = False
        self.enpassantPossible = () #co-ordinates for a square where en-passant capture is possible 
        self.enpassantPossibleLog = [self.enpassantPossible]
        self.currentCastlingRights = CastleRights(True, True, True, True) 
        self.castleRightsLog =  [CastleRights(self.currentCastlingRights.wks, self.currentCastlingRights.bks,
                                              self.currentCastlingRights.wqs,self.currentCastlingRights.bqs)]

    '''
    Does not work for castling, pawn-promotion and en-passant
    '''

    

    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)  # log the move so that we can undo it later
        self.whiteToMove = not self.whiteToMove  # swap players
        #updating the kings location if moved 
        if move.pieceMoved == "wK":
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == "bK":
            self.blackKingLocation = (move.endRow, move.endCol)
        
        # Pawn Promotion
        if move.isPawnPromotion:
            # x = input("Enter piece to be promoted to: ")
            self.board[move.endRow][move.endCol] = move.pieceMoved[0] + 'Q'

        #Enpassant Move
        if move.isEnpassantMove:
            self.board[move.startRow][move.endCol] = '--' #Capturing the pawn
            self.board[move.endRow][move.endCol] = move.pieceMoved

        
        #updating isEnpassantPossible variable 
        if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
            self.enpassantPossible = ((move.startRow + move.endRow)//2, move.startCol)
        else:
            self.enpassantPossible = ()

        #Castle Move
        if move.isCastleMove:
            if move.endCol - move.startCol == 2: #kingside castle
                self.board[move.endRow][move.endCol - 1] = self.board[move.endRow][move.endCol + 1]
                self.board[move.endRow][move.endCol + 1] = '--'
            else: #Queenside Castle
                self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 2]
                self.board[move.endRow][move.endCol - 2] = '--'

        self.enpassantPossibleLog.append(self.enpassantPossible)

             #Update Castling Rights : - Whenever it is a rook or a king move
        self.updateCastlingRights(move) 
        self.castleRightsLog.append(CastleRights(self.currentCastlingRights.wks, self.currentCastlingRights.bks,
                                              self.currentCastlingRights.wqs,self.currentCastlingRights.bqs))

                  
  
    '''
    Undo last move made    
    '''
    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
            # updating the kings location if moved
            if move.pieceMoved == "wK":
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == "bK":
                self.blackKingLocation = (move.startRow, move.startCol)

            # undo Enpassant Move
            if move.isEnpassantMove:
                self.board[move.endRow][move.endCol] = "--"  # leaving the landing square blank
                self.board[move.startRow][move.endCol] = move.pieceCaptured
                # self.enpassantPossible = (move.endRow, move.endCol)

            self.enpassantPossibleLog.pop()
            self.enpassantPossible = self.enpassantPossibleLog[-1]

            # # undo 2 square pawn advance
            # if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
            #     self.enpassantPossible = ()
            
            #undo Castling Rights:
            self.castleRightsLog.pop() #get rid of current castle rights from the move we are undoing
            newRights = self.castleRightsLog[-1] #set the current castle rights to the previous ones
            self.currentCastlingRights = CastleRights(newRights.wks, newRights.bks, newRights.wqs, newRights.bqs)
            
            #Undo Castle Move
            if move.isCastleMove:
                if move.endCol - move.startCol == 2: #kingside 
                    self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 1]
                    self.board[move.endRow][move.endCol - 1] = '--' 
                else:
                    self.board[move.endRow][move.endCol - 2] = self.board[move.endRow][move.endCol + 1]
                    self.board[move.endRow][move.endCol + 1] = '--' 

            self.checkMate = False
            self.checkMate = False

    # def undoMove(self):
    #     if len(self.moveLog) != 0:
    #         move = self.moveLog.pop()
    #         self.board[move.startRow][move.startCol] = move.pieceMoved
    #         self.board[move.endRow][move.endCol] = move.pieceCaptured
    #         self.whiteToMove = not self.whiteToMove
    #         # updating the kings location if moved
    #         if move.pieceMoved == "wK":
    #             self.whiteKingLocation = (move.startRow, move.startCol)
    #         elif move.pieceMoved == "bK":
    #             self.blackKingLocation = (move.startRow, move.startCol)

    #         # undo Enpassant Move
    #         if move.isEnpassantMove:
    #             self.board[move.endRow][move.endCol] = "--"  # leaving the landing square blank
    #             self.board[move.startRow][move.endCol] = move.pieceCaptured
    #             self.enpassantPossible = (move.endRow, move.endCol)

    #         # undo 2 square pawn advance
    #         if move.pieceMoved[1] == 'p' and abs(move.startRow - move.endRow) == 2:
    #             self.enpassantPossible = ()
            
    #         #undo Castling Rights:
    #         self.castleRightsLog.pop() #get rid of current castle rights from the move we are undoing
    #         self.currentCastlingRights = self.castleRightsLog[-1] #set the current castle rights to the previous ones
             
    #         # castleRights = self.currentCastlingRights[-1]
    #         # self.currentCastlingRights = castleRights

    #         #Undo Castle Move
    #         if move.isCastleMove:
    #             if move.endCol - move.startCol == 2: #kingside 
    #                 self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][move.endCol - 1]
    #                 self.board[move.endRow][move.endCol - 1] = '--' 
    #             else:
    #                 self.board[move.endRow][move.endCol - 2] = self.board[move.endRow][move.endCol + 1]
    #                 self.board[move.endRow][move.endCol + 1] = '--' 
                    

    def updateCastlingRights(self, move):
        if move.pieceMoved == 'wK':
            self.currentCastlingRights.wks = False
            
            self.currentCastlingRights.wqs = False
        elif move.pieceMoved == 'bK':
            self.currentCastlingRights.bks = False
            self.currentCastlingRights.bqs = False
        elif move.pieceMoved == 'wR':
            if move.startRow == 7:
                if move.startCol == 0:  #Left Rook
                    self.currentCastlingRights.wqs = False
                elif move.startCol == 7: #RightRook
                    self.currentCastlingRights.wks = False
        elif move.pieceMoved == 'bR':
            if move.startRow == 0:
                if move.startCol == 0:  #Left Rook
                    self.currentCastlingRights.bqs = False
                elif move.startCol == 7: #RightRook
                    self.currentCastlingRights.bks = False

        #if a rook is captured
        if move.pieceCaptured == 'wR':
            if move.endRow == 7:
                if move.endCol == 0:
                    self.currentCastlingRights.wqs = False
                elif move.endCol == 7:
                    self.currentCastlingRights.wks = False
        elif move.pieceCaptured == 'bR':
            if move.endRow == 0:
                if move.endCol == 0:
                    self.currentCastlingRights.bqs = False
                elif move.endCol == 7:
                    self.currentCastlingRights.bks = False
        

            



    '''
    All Moves Considering Checks 
    '''

    '''
    Using Naive Algorithm approach
    1. Generate All Possible Moves
    2. For each move, calculate
    3. Generate All oppopnents move
    4. For Each Opponent Move check if it attacks the king
    5. If it does not, valid move                
    '''

    def getValidMoves(self):
        tempEnpassantPossible= self.enpassantPossible
        tempCastlingRights = CastleRights(self.currentCastlingRights.wks, self.currentCastlingRights.bks, 
                                          self.currentCastlingRights.wqs, self.currentCastlingRights.bqs) #Copy the current castling rights
        moves = self.getAllPossibleMoves()

        if self.whiteToMove:
            self.getCastleMoves(self.whiteKingLocation[0], self.whiteKingLocation[1], moves)
        else:
            self.getCastleMoves(self.blackKingLocation[0], self.blackKingLocation[1], moves)
        for i in range(len(moves) - 1, -1, -1):
            self.makeMove(moves[i])
            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
                moves.remove(moves[i])
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
        if len(moves) == 0:
            if self.inCheck():
                self.checkMate = True
            else:
                self.staleMate = True
    
        self.enpassantPossible = tempEnpassantPossible
        self.currentCastlingRights = tempCastlingRights 

       
        return moves
    

    '''
    Determine if current player is in check
    '''
    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])


    '''
    Determine if the enemy can attack the square r, c
    '''

    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove

        for move in oppMoves:
            if move.endRow == r and move.endCol == c: #square is under attack 
                return True
        return False 


    '''
    All Moves Without Considering Checks
    '''
    

    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):  # no of rows
            for c in range(len(self.board[r])):  # no of cols in given row
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    # Calls the appropriate move function based on piece type
                    self.moveFunctions[piece](r, c, moves)

        return moves

    '''
    Get all moves for possible pieces located at (row,col) and add them to list of possibble moves 
    '''

    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:  # white pawn move
            if self.board[r-1][c] == '--':  # one square pawn advance
                moves.append(Move((r, c), (r-1, c), self.board))
                if r == 6 and self.board[r-2][c] == '--':
                    # 2 square
                    moves.append(Move((r, c), (r-2, c), self.board))
            if c-1 >= 0:
                if self.board[r-1][c-1][0] == "b":  # enemy piece to capture
                    moves.append(Move((r, c), (r-1, c-1), self.board))
                elif (r-1, c-1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r-1, c-1), self.board, isEnpassantMove=True))
            
            if c+1 <= 7:
                if self.board[r-1][c+1][0] == "b":  # enemy piece to capture
                    moves.append(Move((r, c), (r-1, c+1), self.board))
                elif (r-1, c+1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r-1, c+1), self.board, isEnpassantMove=True))

        if not self.whiteToMove:  # black pawn move
            if self.board[r+1][c] == '--':  # one square pawn advance
                moves.append(Move((r, c), (r+1, c), self.board))
                if r == 1 and self.board[r+2][c] == '--':
                    # 2 square
                    moves.append(Move((r, c), (r+2, c), self.board))
            if c-1 >= 0:
                if self.board[r+1][c-1][0] == "w":  # enemy piece to capture
                    moves.append(Move((r, c), (r+1, c-1), self.board))
                elif (r+1, c-1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r+1, c-1), self.board, isEnpassantMove=True))
            if c+1 <= 7:
                if self.board[r+1][c+1][0] == "w":  # enemy piece to capture
                    moves.append(Move((r, c), (r+1, c+1), self.board))
                elif (r+1, c+1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r+1, c+1), self.board, isEnpassantMove=True))

    def getRookMoves(self, r, c, moves):
        # up, left, down, right
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):  # rook can move up to 7 squares
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:  # on board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":  # empty space valid
                        moves.append(
                            Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:  # enemy piece valid
                        moves.append(
                            Move((r, c), (endRow, endCol), self.board))
                        break
                    else:  # friendly piece invalid
                        break
                else:  # off board
                    break

    def getKnightMoves(self, r, c, moves):
        knightMoves = ((-2,-1), (-2,1),(2,-1), (2,1), (-1,-2), (-1,2),(1,-2), (1,2))
        allyColor = "w" if self.whiteToMove else "b"
        for m in knightMoves:
            endRow = r + m[0] 
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:  # on board
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:  # empty space valid
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    def getBishopMoves(self, r, c, moves):
        directions = ((-1,-1), (-1,1),(1,-1), (1,1))
        enemyColor = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):  # rook can move up to 7 squares
                endRow = r + d[0] * i
                endCol = c + d[1] * i
                if 0 <= endRow < 8 and 0 <= endCol < 8:  # on board
                    endPiece = self.board[endRow][endCol]
                    if endPiece == "--":  # empty space valid
                        moves.append(
                            Move((r, c), (endRow, endCol), self.board))
                    elif endPiece[0] == enemyColor:  # enemy piece valid
                        moves.append(
                            Move((r, c), (endRow, endCol), self.board))
                        break
                    else:  # friendly piece invalid
                        break
                else:  # off board
                    break


    def getKingMoves(self, r, c, moves):
        kingMoves = ((-1,-1), (-1,1),(0,-1), (0,1), (1,-1), (1,1),(1,0), (-1,0))
        allyColor = "w" if self.whiteToMove else "b"
        for m in kingMoves:
            endRow = r + m[0] 
            endCol = c + m[1]
            if 0 <= endRow < 8 and 0 <= endCol < 8:  # on board
                endPiece = self.board[endRow][endCol]
                if endPiece[0] != allyColor:  # empty space valid
                    moves.append(Move((r, c), (endRow, endCol), self.board))

    
    '''
    Generating all valid castle moves for king and add them to the moves list
    '''
    def getCastleMoves(self, r, c, moves):
        if self.squareUnderAttack(r,c):
            return
        if (self.whiteToMove and self.currentCastlingRights.wks) or (not self.whiteToMove and self.currentCastlingRights.bks) :
            self.getKingsideCastleMoves(r,c,moves)

        if (self.whiteToMove and self.currentCastlingRights.wqs) or (not self.whiteToMove and self.currentCastlingRights.bqs) :
            self.getQueensideCastleMoves(r,c,moves)
    
    def getKingsideCastleMoves(self, r, c, moves):
        if self.board[r][c+1] == '--' and self.board[r][c+2] == '--':
            if not self.squareUnderAttack(r, c+1) and not self.squareUnderAttack(r, c+2):
                moves.append(Move((r, c), (r, c+2), self.board, isCastleMove = True))

    def getQueensideCastleMoves(self, r, c, moves):
        if self.board[r][c-1] == '--' and self.board[r][c-2] == '--' and self.board[r][c-3] == '--':
            if not self.squareUnderAttack(r, c-1) and not self.squareUnderAttack(r, c-2):
                moves.append(Move((r, c), (r, c-2), self.board, isCastleMove = True))




    def getQueenMoves(self, r, c, moves):
        self.getRookMoves(r,c,moves)
        self.getBishopMoves(r,c,moves)

class CastleRights():
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs


class Move():

    # Mapping notations on the board
    ranksToRows = {
        "1": 7,
        "2": 6,
        "3": 5,
        "4": 4,
        "5": 3,
        "6": 2,
        "7": 1,
        "8": 0
    }
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {
        "a": 0,
        "b": 1,
        "c": 2,
        "d": 3,
        "e": 4,
        "f": 5,
        "g": 6,
        "h": 7
    }
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board, isEnpassantMove = False, isCastleMove = False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]

        self.isPawnPromotion = False
        #Pawn Promotion
        if (self.pieceMoved == "wp" and self.endRow == 0) or  (self.pieceMoved == "bp" and self.endRow == 7):
            self.isPawnPromotion = True


        #Enpassant
        self.isEnpassantMove = isEnpassantMove
        # if self.pieceMoved[1] == "p" and (self.endRow, self.endCol) == enpassantPossible:
        #     self.isEnpassantMove = True
        if self.isEnpassantMove:
            self.pieceCaptured = 'wp' if self.pieceMoved == 'bp' else 'bp'

        self.isCapture = self.pieceCaptured != '--'


        #Castling
        self.isCastleMove = isCastleMove
    
        self.moveId = self.startRow*1000 + self.startCol * \
            100 + self.endRow*10 + self.endCol
        
 
        # print(self.moveId)

    '''
    Overriding the equals method
    '''

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveId == other.moveId
        return False

    def getChessNotation(self):
        # Can be changed to be like real chess notations later om
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]


    # # Overiding the str() method
    # def __str__(self):
    #     # Castle Move 
    #     if self.castle:
    #         return "O-O" if self.endCol == 6  else "O-O-O"
        
    #     endSquare = self.getRankFile(self.endRow, self.endCol)
    #     # pawn move
    #     if self.pieceMoved[1] == 'p':   
    #         if self.isCaptured:
    #             return self.colsToFiles[self.startCol] + 'x' + endSquare
    #         else:
    #             return endSquare
        
    #     # Two same types of piece moving to the same square:

    #     # Also Adding + for a check and # for a checkmate


    #     #piece moves:
    #     moveString = self.pieceMoved[1]
    #     if self.isCaptured:
    #         moveString += 'x'
    #     return moveString + endSquare 



class EstadoJogo():
    def __init__(self):
        self.tabuleiro = [
            ["bR","bN","bB","bQ","bK","bB","bN","bR"],
            ["bp","bp","bp","bp","bp","bp","bp","bp"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["--","--","--","--","--","--","--","--"],
            ["wp","wp","wp","wp","wp","wp","wp","wp"],
            ["wR","wN","wB","wQ","wK","wB","wN","wR"],
        ]
        self.movimentoDasBrancas = True
        self.registroDeMovimentos = []

    def makeMovie(self, move):
        self.tabuleiro[move.startRow][move.startCol] = '--'
        self.tabuleiro[move.endRow][move.endCol] = move.pieceMoved
        self.registroDeMovimentos.append(move)
        self.movimentoDasBrancas = not self.movimentoDasBrancas

    def undoMovie(self):
        if len(self.registroDeMovimentos) != 0:
            self.tabuleiro[self.registroDeMovimentos[-1].startRow][self.registroDeMovimentos[-1].startCol] = self.registroDeMovimentos[-1].pieceMoved
            self.tabuleiro[self.registroDeMovimentos[-1].endRow][self.registroDeMovimentos[-1].endCol] = self.registroDeMovimentos[-1].pieceCaptured
            self.registroDeMovimentos.pop()
            self.movimentoDasBrancas = not self.movimentoDasBrancas

    def getValidMoves(self):
        return self.getAllPossibleMoves()

    def getAllPossibleMoves(self):
        moves = [Move((6,4), (4,4), self.tabuleiro)]
        for r in range(len(self.tabuleiro)):
            for c in range(len(self.tabuleiro[r])):
                turn = self.tabuleiro[r][c][0]
                if (turn == 'w' and self.movimentoDasBrancas) and (turn == 'b' and not self.movimentoDasBrancas):
                    piece = self.tabuleiro[r][c][1]
                    if piece == 'p':
                        self.getPawnMoves(r, c, moves)
                    elif piece == 'R':
                        self.getRookMoves(r, c, moves)
        return moves
    
    def getPawnMoves(self, r, c , moves):
        if self.movimentoDasBrancas:
            if self.tabuleiro[r-1][c] == '--':
                move.append((r,c),(r-1, c), self.tabuleiro)

    def getRookMoves(self, r, c, moves):
        pass

    
class Move():

    ranksToRows = {"1":7, "2":6, "3":5,"4":4,"5":3,"6":2,"7":1, '8':0}
    rowToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a":0, "b":1, "c":2,"d":3,"e":4,"f":5,"g":6, 'h':7}
    colsToFiles = {v:k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow + 10 *self.endCol

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)
    
    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowToRanks[r]
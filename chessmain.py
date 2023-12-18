import pygame as p
import chessengine

ALTURA = 690
LARGURA = 700
DIMENSAO = 15
QUADRADO_TAMANHO = ALTURA // DIMENSAO
MAX_FPS = 15
IMAGENS = {}
line = []
colreal = rowreal= 0
QUADRANTE = 0

for num in range(8):
    line.append(f'{num}--')

def CarregarImagens():
    pieces = []
    boards = 9
    #nB: number of the board
    for nb in range(boards):
        pieces.extend((f"{nb}wR",f"{nb}wN",f"{nb}wB",f"{nb}wQ",f"{nb}wK",f"{nb}wp",f"{nb}bR",f"{nb}bN",f"{nb}bB",f"{nb}bQ",f"{nb}bK",f"{nb}bp"))
    for piece in pieces:
        #print(piece[1:])
        IMAGENS[piece] = p.transform.scale(p.image.load("images/" + piece[1:] + ".png"), (30, 30))

def main():
    p.init()
    screen = p.display.set_mode((ALTURA, LARGURA))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = chessengine.EstadoJogo()
    #validMoves = gs.getValidMoves()
   # moveMade = False

    CarregarImagens()
    running = True
    sqSelected = ()
    playerClicks = []

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False 
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                for multiplicador in range(25):
                    #29,18 cada quadrante aproximadamente. 467/16
                    if location[0] < 29.18*multiplicador:
                        col = multiplicador-1
                        colreal = col
                        break
                for multiplicador in range(25):
                    #29,16 cada quadrante aproximadamente. 700/24
                    if location[1] < 29.18*multiplicador:
                        row = multiplicador-1
                        rowreal = row
                        break
                #col = location[0]//25
                #row = location[1]//25
                if 8 <= col < 16:
                    colreal -= 8
                elif 16 <= col:
                    colreal -= 16
                if 8 <= row < 16:
                    rowreal -= 8
                elif 16 <= col:
                    rowreal -= 16
                print('row',rowreal,row)
                if sqSelected == (row, colreal):
                     sqSelected = ()
                     playerClicks = []
                else:
                    if int(row / 8) == 0 and int(col / 8) == 0:
                         QUADRANTE = 0
                    elif int(row / 8) == 0 and int(col / 8) == 1:
                         QUADRANTE = 1 
                    elif int(row / 8) == 0 and int(col / 8) == 2:
                         QUADRANTE = 2
                    elif int(row / 8) == 1 and int(col / 8) == 0:
                         QUADRANTE = 3
                    elif int(row / 8) == 1 and int(col / 8) == 1:
                         QUADRANTE = 4
                    elif int(row / 8) == 1 and int(col / 8) == 2:
                         QUADRANTE = 5
                    elif int(row / 8) == 2 and int(col / 8) == 0:
                         QUADRANTE = 6
                    elif int(row / 8) == 2 and int(col / 8) == 1:
                         QUADRANTE = 7
                    elif int(row / 8) == 2 and int(col / 8) == 2:
                         QUADRANTE = 8
                    sqSelected = (row, colreal, QUADRANTE)
                    playerClicks.append(sqSelected)
                    print(QUADRANTE)
                if len(playerClicks) == 2:
                    print('testando',playerClicks)
                    move = chessengine.Move(playerClicks[0], playerClicks[1], gs.board)
                    move.getChessNotation()
                    sqSelected = ()
                    gs.makeMovie(move)
                    # if move in validMoves:
                    #    gs.makeMovie(move)
                    #    moveMade = True 
                    playerClicks = []
            # elif e.type == p.KEYDOWN:
            #     if e.key == p.K_z:
            #         gs.undoMovie()
            #         moveMade = True
        # if moveMade:
        #     validMoves = gs.getValidMoves()
        #     moveMade = False

        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()

def drawGameState(screen, gs):
    drawboard(screen)
    drawPieces(screen ,gs.board)
              
def drawboard(screen):
    larg = 0
    altu = 0
    for horizontal in range(25):
        if horizontal % 2 == 0:
            for vertical in range(25):
                if vertical % 2 == 0:
                    p.draw.rect(screen, (190,190,190), (larg, altu, QUADRADO_TAMANHO, QUADRADO_TAMANHO))
                else:
                    p.draw.rect(screen, (255,255,255), (larg, altu, QUADRADO_TAMANHO, QUADRADO_TAMANHO))
                larg = 29*vertical
        else:
            for vertical in range(25):
                if vertical % 2 != 0:
                    p.draw.rect(screen, (190,190,190), (larg, altu, QUADRADO_TAMANHO, QUADRADO_TAMANHO))
                else:
                    p.draw.rect(screen, (255,255,255), (larg, altu, QUADRADO_TAMANHO, QUADRADO_TAMANHO))
                larg = 29*vertical
        p.draw.line(screen, (0,0,0), (0, 233), (700, 233), 4)
        p.draw.line(screen, (0,0,0), (0, 466), (700, 466), 4)
        p.draw.line(screen, (0,0,0), (233, 0), (233, 700), 4)
        p.draw.line(screen, (0,0,0), (466, 0), (466, 700), 4)

        altu = 29*horizontal

def drawPieces(screen, board):
    SQUARE = 29
    for rowSquares in range(3):
        indRowSquares = rowSquares * 232
        for colSquares in range(3):
            indColSquares = colSquares * 232
            for r in range(8):
                for c in range(8):
                    piece = board[rowSquares+colSquares][r][c]
                    if piece not in line:
                        screen.blit(IMAGENS[piece], p.Rect(c*SQUARE+indRowSquares, r*SQUARE+indColSquares, c*SQUARE+indRowSquares, SQUARE*r+indColSquares))

if __name__ == "__main__":
    main()
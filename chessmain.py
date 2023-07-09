import pygame as p
import chessengine
import time

ALTURA = LARGURA = 512
DIMENSAO = 8
QUADRADO_TAMANHO = ALTURA // DIMENSAO
MAX_FPS = 15
IMAGENS = {}

def CarregarImagens():
    pecas = ["wR","wN","wB","wQ","wK","wp","bR","bN","bB","bQ","bK","bp"]
    for peca in pecas:
        IMAGENS[peca] = p.transform.scale(p.image.load("images/" + peca + ".png"), (QUADRADO_TAMANHO, QUADRADO_TAMANHO))

def main():
    p.init()
    screen = p.display.set_mode((ALTURA, LARGURA))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = chessengine.EstadoJogo()
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
                col = location[0]//QUADRADO_TAMANHO
                row = location[1]//QUADRADO_TAMANHO
                if sqSelected == (row, col):
                    sqSelected = ()
                    playerClicks = []
                else:
                    sqSelected = (row, col)
                    playerClicks.append(sqSelected)
                if len(playerClicks) == 2:
                    move = chessengine.Move(playerClicks[0], playerClicks[1], gs.tabuleiro)
                    print(move.getChessNotation())
                    sqSelected = ()
                    gs.makeMovie(move)
                    playerClicks = []
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z:
                    gs.undoMovie()
        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()

def drawGameState(screen, gs):
    drawboard(screen)
    drawPieces(screen ,gs.tabuleiro)
              
def drawboard(screen):
    larg = 0
    altu = 0
    for horizontal in range(9):
        if horizontal % 2 == 0:
            for vertical in range(8):
                if vertical % 2 == 0:
                    p.draw.rect(screen, (190,190,190), (larg, altu, 64, 64))
                else:
                    p.draw.rect(screen, (255,255,255), (larg, altu, 64, 64))
                larg = 64*vertical
        else:
            for vertical in range(8):
                if vertical % 2 != 0:
                    p.draw.rect(screen, (190,190,190), (larg, altu, 64, 64))
                else:
                    p.draw.rect(screen, (255,255,255), (larg, altu, 64, 64))
                larg = 64*vertical
        altu = 64*horizontal

def drawPieces(screen, board):
    for r in range(DIMENSAO):
        for c in range(DIMENSAO):
            peca = board[r][c]
            if peca != '--':
                screen.blit(IMAGENS[peca], p.Rect(c*QUADRADO_TAMANHO, r*QUADRADO_TAMANHO, QUADRADO_TAMANHO, QUADRADO_TAMANHO))

if __name__ == "__main__":
    main()
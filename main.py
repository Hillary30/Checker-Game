import pygame
from checkers.constants import SQUARE_SIZE, WIDTH, HEIGHT, RED, WHITE
from checkers.game import Game
from minimax.algorithm import minimax

#pygame display where the game is held
#basic event loop: checks if we press key or click 
FPS = 60 #specific to the drawing and not the checkers game
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers') #name od game on top


def get_row_col_from_mouse(pos): #pos = (x, y)
    x, y = pos #base on SQUARE_SIZE we can find position in 
    row = y // SQUARE_SIZE #ex: y=650, 650//100= 6, we are in row 6
    col = x // SQUARE_SIZE
    return row, col


#runs the game + event loop
def main(): 
    run = True
    clock = pygame.time.Clock() #constant frame rate
    game = Game(WIN) #Board object

    while run:
        clock.tick(FPS)

        if game.turn == WHITE:
            value, new_board = minimax(game.get_board(), 3, WHITE, game)
            game.ai_move(new_board) #update the board after AI move


        if game.winner() != None:
            print(game.winner())
            run = False
        
        #check if any events occured 
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                #check if whos moving and any pieces
                #select piece
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)

        game.update()

    pygame.quit()

main()

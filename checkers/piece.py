from .constants import RED, WHITE, SQUARE_SIZE, GREY, CROWN
import pygame

class Piece:
    PADDING = 15
    OUTLINE = 2

    def __init__(self, row, col, color): #make new piece need which row, col to be in and color
        self.row = row
        self.col = col
        self.color = color
        self.king = False
        self.x = 0
        self.y = 0
        self.calc_pos() #will be called multiple times


    #calcs the x, y pos based on row and col we are in
    def calc_pos(self):
        self.x = SQUARE_SIZE*self.col + SQUARE_SIZE//2 #right in the middle of the square (100+50) = middle
        #draw a circle = start in center then radius
        self.y = SQUARE_SIZE*self.row + SQUARE_SIZE//2

    def make_king(self):
        self.king = True

    def draw(self, win):
        radius = SQUARE_SIZE//2 - self.PADDING #padding makes sure it doesn't touch the edge of square
        pygame.draw.circle(win, GREY, (self.x, self.y), radius+self.OUTLINE) #draws outline first = big circle
        pygame.draw.circle(win, self.color, (self.x, self.y), radius) #draws smaller circle for piece
        if self.king:
            win.blit(CROWN, (self.x - CROWN.get_width()//2, self.y - CROWN.get_height()//2))#blit = draw onto display (x,y) - is the top left of the image - it wont be centered

    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()

    def __repr__(self): #makes unique representation of object when debug
        return str(self.color)
        
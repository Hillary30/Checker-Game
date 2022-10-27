#handles the game
#whose turn, which piece, move validation
#interface with the board
#not dependent on the user's move
#AI vs AI

from pickle import NONE
import pygame
from .constants import RED, SQUARE_SIZE, WHITE, BLUE
from .board import Board

class Game:
    def __init__(self, win):
        self._init()
        self.win = win #window


    #update display
    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    
    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = RED
        self.valid_moves = {}


    def winner(self):
        return self.board.winner()


    def reset(self):
        self._init()


    def select(self, row, col): #when you select piece, information stored gives possible moves, or change piece selected
        if self.selected:
            result = self._move(row, col)  #if valid selection, try to move it
            if not result:  #not valid, then select another piece
                self.selected = None 
                self.select(row, col)

        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn: #if there is a piece, and you clicked on YOUR peice
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True

        return False



    def _move(self, row, col):
        piece = self.board.get_piece(row, col) #pos to move to 
        if self.selected and piece == 0 and (row, col) in self.valid_moves: 
            #if we selected something, and the pos/piece is "empty", then we can move it to the row/col in parameter
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)] #find a skipped piece

            if skipped: #if we skipped over something, remove it
                self.board.remove(skipped)
            self.change_turn()
        else: 
            return False
        return True
    
    def draw_valid_moves(self, moves): #moves = {}
        for move in moves: #loops through all the keys, keys are (row col)
            row, col = move
            pygame.draw.circle(self.win, BLUE, (col*SQUARE_SIZE + SQUARE_SIZE//2, row*SQUARE_SIZE + SQUARE_SIZE//2), 15) #15=radius


    def change_turn(self):
        self.valid_moves = {}
        if self.turn == RED:
            self.turn = WHITE
        else: 
            self.turn = RED


    def get_board(self):
        return self.board

    #return board after AI move
    def ai_move(self, board):
        self.board = board #pass new board to the game
        self.change_turn()

#check color R or B?
#if R, then move down -> left diag or right diag

#move 1 left and 1 down from R, check if piece (left diagonal of R)
#if piece == R, our piece so cant move
#if empty, we can move
#if piece == B, check the diagonal - move left 1 and 1 down
    #valid move and can move --> add to valid_moves
    #keep track of the piec being jumped - so we can remove it

    #check for double jump - can be multiple double jumps 
    #once we jumped ONCE, from the position that we are at --> check if we can jump again


#move 1 right and 1 down from R (right diagonal of R)
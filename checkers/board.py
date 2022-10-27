#checkers board, peices and moves - draws onto the board - state of the game 
import pygame
#.constant b/c in the same package = relative import
from .constants import BLACK, ROWS, COLS, RED, SQUARE_SIZE, WHITE 
from .piece import Piece

class Board:
    def __init__(self):
        #2d list with 8 diff elements each - with peices/colors/king piece
        self.board = [] #2d array and holds all the pieces

        #track who's turn it is
        #is there a selected piece
        self.red_left = self.white_left = 12 #there are 12 checker pieces for each player
        self.red_kings = self.white_kings = 0
        self.create_board()

    #give us a "win"dow to draw on
    def draw_squares(self, win):
        win.fill(BLACK)

        for row in range(ROWS):
            #row = 0, row%2= 0, draw red in col 0, step by 2 - 0, 2, 4, 6
            #row = 1, row%2= 1, draw red in col 1, step by 2 - 1, 3, 5, 7
            for col in range(row % 2, COLS, 2): 
                pygame.draw.rect(win, RED, (row*SQUARE_SIZE, col*SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)) #draw rectangle in "win"dow in red
                #(cordX, cordY, drawX, drawY)^


    #given state of board, what is score - considers # pieces and kings
    #white is AI
    #prioritize AI to become a king if it can
    def evaluate(self):
        return self.white_left - self.red_left + (self.white_kings * 0.5 - self.red_kings * 0.5)

    
    #return all pieces of a certain color, and check all of the valid moves of those pieces
    def get_all_pieces(self, color): #loop through all pieces and return all that are color
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces


    def move(self, piece, row, col):
        #to move = delete first, then change position
        #move piece in the list + piece.move()
        #piece we want to move, and piece in position we want to move to = swap
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        #check if make king = check row/col + update piece.king
        if row == ROWS-1 or row == 0: #making the board doesn't call the move function - needs to MOVE
            piece.make_king()
            if piece.color == WHITE:
                self.white_kings += 1
            else: 
                self.red_kings += 1


    def get_piece(self, row, col):
        return self.board[row][col]


    def create_board(self): #function makes the board 2d b/c piece is (row, col)
        #create pieces - red top - white bottom
        for row in range(ROWS):
            self.board.append([]) #add list for each row = holds the pieces
            for col in range(COLS):
                if col%2 == ((row + 1) % 2): #draws row 0 odd cols, row 1 even cols
                    if row < 3: #skip row 3
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row > 4: #skip row 4
                        self.board[row].append(Piece(row, col, RED))
                    else:
                        self.board[row].append(0)
                else: #nothing is drawn = 0
                    self.board[row].append(0)
    
    #draws pieces and squres
    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)


    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == RED:
                    self.red_left -= 1
                else: 
                    self.white_left -= 1


    def winner(self):
        if self.red_left <= 0:
            return WHITE
        elif self.white_left <= 0:
            return RED
        return None


    def get_valid_moves(self, piece):
        moves = {} #store the move as the key, ex: 4,5 can be a valid pos, (4,5):[(3,4)] --> jumped over 3,4 to get to 4,5
        left = piece.col - 1 #move left/right 1 to check diag
        right = piece.col + 1
        row = piece.row

        if piece.color == RED or piece.king: #KING can go up
            moves.update(self._traverse_left(row-1, max(row-3, -1), -1, piece.color, left)) #returns another dictionary
            #stop at -1, we are at row 0 OR we are looking at 2 rows max above us
            moves.update(self._traverse_right(row-1, max(row-3, -1), -1, piece.color, right))
        if piece.color == WHITE or piece.king: #moves down and stops at ROWS
            moves.update(self._traverse_left(row+1, min(row+3, ROWS), 1, piece.color, left)) #returns another dictionary
            moves.update(self._traverse_right(row+1, min(row+3, ROWS), 1, piece.color, right))

        return moves #merges the moves into moves

    
    #look in left diagn
    #step = go up or down row? 
    #skipped: have we skipped
    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0: #if out of range
                break

            current = self.board[r][left]
            if current == 0: #if empty squre
                if skipped and not last: #if skipped and no piece is seen
                    break
                #if jumped piece and there is not another valid move, can not jump again
                elif skipped: #if we already skipped
                    moves[(r, left)] = last+skipped #combine the previous jump and the current jump
                else:
                    moves[(r, left)] = last #if we are at empty and we skipped 

                if last: #if we skipped, prepare to double jump
                    if step == -1:
                        row = max(r-3, 0)
                    else: 
                        row = min(r+3, ROWS)
                    
                    moves.update(self._traverse_left(r+step, row, step, color, left-1, skipped=last)) #check if valid moves after we jumped once
                    moves.update(self._traverse_right(r+step, row, step, color, left+1, skipped=last))
                break
            elif current.color == color: #if our piece = can't move
                break
            else: #opponent color, we could move over it if there is an empty square
                last = [current]

            left -= 1
        return moves


    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS: #if out of range
                break

            current = current = self.board[r][right]
            if current == 0: #if empty squre
                if skipped and not last: #if skipped and no piece is seen
                    break
                #if jumped piece and there is not another valid move, can not jump again
                elif skipped: #if we already skipped
                    moves[(r, right)] = last+skipped #combine the previous jump and the current jump
                else:
                    moves[(r, right)] = last #if we are at empty and we skipped 

                if last: #if we skipped, prepare to double jump
                    if step == -1:
                        row = max(r-3, 0)
                    else: 
                        row = min(r+3, ROWS)
                    
                    moves.update(self._traverse_left(r+step, row, step, color, right-1, skipped=last)) #check if valid moves after we jumped once
                    moves.update(self._traverse_right(r+step, row, step, color, right+1, skipped=last))
                break
            elif current.color == color: #if our piece = can't move
                break
            else: #opponent color, we could move over it if there is an empty square
                last = [current]
                
            right += 1

        return moves

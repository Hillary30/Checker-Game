from copy import deepcopy
import pygame
#copy the board a bunch of times
#deepcopy = copies reference and object itself
#shallowcopy = only by reference
#if modified - the other variable doesn't change

RED = (255, 0, 0)
WHITE = (255, 255, 255)


#position: current position - board object
#based on board, give best position 
#depth: how far will the tree go? 
#^every call will decrease the depth by 1 --> recursive
#max_player: bool, min or max the value?
#^if T then max, if F then min
#Ai can play against each other
#game is game obj passed in main
def minimax(position, depth, max_player, game):
    #determine the depth --> evaluate the position when reach end of tree (end = depth)
    if depth == 0 or position.winner() != None: #BASE CASE: DEPTH == 0 or if winner
        return position.evaluate(), position #evaluate = score = #of pieces and kings, return last position and the "score"
    
    if max_player: #maximize the score , MAX = WHITE PLAYER
        maxEval = float('-inf') 
        best_move = None
        for move in get_all_moves(position, WHITE, game): #for every move, evaluate the move using minimax
            evaluation = minimax(move, depth-1, False, game)[0] #evaluate for the best player - is diff every recursive call
            #[0] b/c we dont care of path, only need eval
            maxEval = max(maxEval, evaluation) #update the best move

            if maxEval == evaluation: #get path when best eval
                best_move = move
        return maxEval, best_move #return value of best board

    else: #minimize the score
        minEval = float('inf') 
        for move in get_all_moves(position, RED, game): #for every move, evaluate the move using minimax
            evaluation = minimax(move, depth-1, True, game)[0] #evaluate for the worst player then turns True -> goes back to max
            minEval = min(minEval, evaluation) #update the worst move

            if minEval == evaluation:
                best_move = move
        return minEval, best_move 


#if depth = 0, give evaluation of position
#if depth != then minimax from the root node
#branch down, and evaluate the board --> keep going till depth = 0 --> "leaf node"
#then pick best score, and go back up from the tree to the root and gives the best move
#min and max - goes back and forth


def simulate_move(piece, move, board, game, skip): #movev = [[new_board, piece]]
    board.move(piece, move[0], move[1]) #piece, row, col
    if skip:
        board.remove(skip)
    return board


#get all moves from current board - use get_all_pieces 
def get_all_moves(board, color, game):
    moves = [] #stores new board if we move the piece [[board, piece], [new_board, piece]]

    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)

        for move, skip in valid_moves.items(): #loop through dictionary - skip == (key, value) = (row, col):[pieces we skipped to get to (row, col)]
            #draw_moves(game, board, piece)
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            #deepcopy b/c we will alter temp, but don't want to modify the "original" board
            new_board = simulate_move(temp_piece, move, temp_board, game, skip) #take piece and the move we want on the piece on the temp_board, then return the new_board
            moves.append(new_board) #score the new_board in minimax
    return moves


#def draw_moves(game, board, piece):
#    valid_moves = board.get_valid_moves(piece)
#    board.draw(game.win) #redraws the board
#    pygame.draw.circle(game.win, (0, 255, 0), (piece.x, piece.y), 50, 5) #50 = radius, 5 = thickness of circle
#    game.draw_valid_moves(valid_moves.keys()) #valid_moves - {(4, 5):[3, 4]}
#    pygame.display.update()



import pygame
import math
import pprint

# pygame colours
WHITE = (255,255,255)
BLACK = (  0,  0,  0)
RED   = (255,  0,  0)
GREEN = (  0,255,  0)
BLUE  = (  0,  0,255)
YELLOW = (255,255, 0)
ORANGE = (255, 69 ,0)
GREY  = ( 30, 30, 30)

'''
 X | O |
---|---|---
   | X |
---|---|---
 O |   | X


== 'xo  x o x'
   '012345678'



 0 | 1 | 2
---|---|---
 3 | 4 | 5
---|---|---
 6 | 7 | 8


'''
class grid():
    def __init__(self, win):
        self.board = [[' ', ' ', ' '],
                      [' ', ' ', ' '],
                      [' ', ' ', ' ']]
        self.win = win
        self.w, self.h = self.win.get_size()
        self.res = self.w // 3

        self.count = 0
                      
        self.crossToGo = True

        pygame.font.init()
        

    def draw(self):
        # drawing grid - the 4 lines
        for i in range(1, len(self.board)):
            pygame.draw.line(self.win, WHITE, (self.res * i, 0), (self.res * i, self.h), 4)
            pygame.draw.line(self.win, WHITE, (0, self.res * i), (self.w, self.res * i), 4)

        # drawing the characters ('o' or 'x') to the screen
        # font
        font = pygame.font.SysFont(None,500)
        # padding
        pdx = self.res * 0.5
        pdy = self.res * 0.5
        # looping through x, y
        for y in range(len(self.board)):
            for x in range(len(self.board)):
                # getting text object
                text = font.render(str(self.board[y][x]), True, WHITE)
                # centering
                textrect = text.get_rect(center=(x * self.res + pdx, y * self.res + pdy))
                # displaying
                self.win.blit(text, textrect)

    
    def print_board(self):
        # function to print board nicely
        for i in self.board:
            print(i)
        print("\n")
                

    def click_in_box(self, pos):
        # ease of use
        x, y = pos

        # getting list indexes
        listX = (x // self.res)
        listY = (y // self.res)
        # checking if a move can go there
        if self.board[listY][listX] == ' ':
            # setting the list element be whos turn it is
            self.board[listY][listX] = 'x' if self.crossToGo else 'o'
            return True
        return False
    

    def game_over(self):
        for i in range(3):
            # vertical
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != ' ':
                return self.board[0][i]
            # horizontal
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != ' ':
                return self.board[i][0]
        
        # diagonal
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != ' ':
            return self.board[0][0]
        if self.board[2][0] == self.board[1][1] == self.board[0][2] != ' ':
            return self.board[2][0]

        # still spaces
        for i in range(3):
            if ' ' in self.board[i]:
                return False
        # tie
        return None


    def board_eval(self):
        result = self.game_over()
        # not finished
        if result != False:
            # tie
            if result == None:
                return 0
            else:
                # o win
                if result == 'o':
                    return -math.inf
                # x win
                elif result == 'x':
                    return math.inf
        return 0


    def get_valid_moves(self):
        # get empty spaces
        moves = []
        for i, y in enumerate(self.board):
            for j, x in enumerate(y):
                if x == ' ':
                    moves.append((i, j))
                    #if (i, j) == (0, 2):
                        #print("Being Gened")
        return moves


    def minimax(self, depth, alpha, beta, isMaximiser):
        # debugging
        self.count +=1
        # getting valid moved
        possibleMoves = self.get_valid_moves()
        # getting evaluation of the board
        value = self.board_eval()

        # if weve gone to bottom of the depth or one of the people have won
        if depth == 0 or value == -math.inf or value == math.inf:
            # returning value
            return value

        # if x
        if isMaximiser:
            # anything good for x becomes best move after 1 iteration
            maxEval = -math.inf
            for move in possibleMoves:
                # make the move
                self.board[move[0]][move[1]] = 'x'
                # change goes
                self.crossToGo = not self.crossToGo
                # evaluates the recusive score
                eval = self.minimax(depth - 1, alpha, beta, False)
                # undo move
                self.board[move[0]][move[1]] = ' '
                # changes turn
                self.crossToGo = not self.crossToGo

                # reassigns max eval
                if eval >= maxEval:
                    maxEval = eval

                # alpha beta pruning
                if alpha >= eval:
                    alpha = eval
                if beta <= alpha:
                    break
                
            return maxEval

        
        else:
            minEval = math.inf
            # goes through possible moves
            for move in possibleMoves:
                # makes move
                self.board[move[0]][move[1]] = 'o'
                # changes turn
                self.crossToGo = not self.crossToGo
                # gets recusive score
                eval = self.minimax(depth - 1, alpha, beta, True)
                # undoes move
                self.board[move[0]][move[1]] = ' '
                # changes turn
                self.crossToGo = not self.crossToGo

                # reassigning min value
                if eval <= minEval:
                    minEval = eval

                #alpha beta pruning
                if beta <= eval:
                    beta = eval
                if beta <= alpha:
                    break
                
            return minEval



    def make_best_move(self):
        # highest possible
        bestScore = math.inf
        # get all valid moves
        possibleMoves = self.get_valid_moves()
        # set best move to be the firstt move
        bestMove = possibleMoves[0]

        #goes through valid moves
        for move in possibleMoves:
            # makes move
            self.board[move[0]][move[1]] = 'o'
            # changes turn
            self.crossToGo = not self.crossToGo
            # gets minimax of each move
            eval = self.minimax(10, -math.inf, math.inf, True)
            # debugging
            print(eval)
            # undoes move
            self.board[move[0]][move[1]] = ' '
            # changes turn
            self.crossToGo = not self.crossToGo
            # gets best move
            if eval <= bestScore:
                bestScore = eval
                bestMove = move
        # debugging
        print(self.count)


        # actually makes move
        self.board[bestMove[0]][bestMove[1]] = 'o'
        self.crossToGo = not self.crossToGo
                    
        
        

        
            
        
        

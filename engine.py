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
# representing in string or 1D array
# easier using 2D
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

        # change to False if AI to go first         
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

        # no more valid moves or the game is a tie
        if len(self.get_valid_moves()) == 0:
            return 'tie'
        

        


    def get_valid_moves(self):
        # get empty spaces
        moves = []
        for i, y in enumerate(self.board):
            for j, x in enumerate(y):
                if x == ' ':
                    moves.append((i, j))
        
        return moves


    def minimax(self, depth, maximiser):
        score = self.game_over()
        # if recusrsion hasnt made it to bottom
        if score != None:
            if score == 'x':
                # multiplying by depth to prioritise winning faster
                return 100 * depth
            elif score == 'o':
                return -100 * depth
            return 0

        moves = self.get_valid_moves()
        if maximiser:
            bestScore = -math.inf
            for move in moves:
                # make the move
                self.board[move[0]][move[1]] = 'x'
                # change goes
                self.crossToGo = not self.crossToGo
                # evaluates the recusive score
                evaluation = self.minimax(depth - 1, False)
                # undo move
                self.board[move[0]][move[1]] = ' '
                # changes turn
                self.crossToGo = not self.crossToGo

                bestScore = max(evaluation, bestScore)
            return bestScore

        else:
            bestScore = math.inf
            for move in moves:
                # make the move
                self.board[move[0]][move[1]] = 'o'
                # change goes
                self.crossToGo = not self.crossToGo
                # evaluates the recusive score
                evaluation = self.minimax(depth - 1, True)
                # undo move
                self.board[move[0]][move[1]] = ' '
                # changes turn
                self.crossToGo = not self.crossToGo

                bestScore = min(evaluation, bestScore)
            return bestScore

    def make_best_move(self):
        # gets all valid moves
        moves = self.get_valid_moves()
        # setting the bestscore infinitely high so all scores will be lower
        bestScore = math.inf
        # going through valid moves
        for move in moves:
            #making the move
            self.board[move[0]][move[1]] = 'o'
            # changing the go
            self.crossToGo = not self.crossToGo
            # getting score
            score = self.minimax(10, True)
            # undoing move
            self.board[move[0]][move[1]] = ' '
            # changing turn back
            self.crossToGo = not self.crossToGo
            # checking if score is better than previous best
            if score < bestScore:
                bestMove = move
                bestScore = score
        # makes the move which is the bes tmove
        self.board[bestMove[0]][bestMove[1]] = 'o'
        # changes turn
        self.crossToGo = not self.crossToGo

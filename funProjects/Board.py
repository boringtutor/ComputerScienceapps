from copy import deepcopy
from os import system
from queue import Queue
from random import randint,seed

MAX_COL = 4
MAX_ROW = 4
SHUFFLE_BOARD = 50

class Board:
    """Models the board of our game and the functionality of the board"""
    
    
    def __init__(self):
        self.goal  = [["  1","  2","  3","  4"],
                      ["  5","  6","  7","  8"],
                      ["  9"," 10"," 11"," 12"],
                      [" 13"," 14"," 15"," __"]]
        self.board = deepcopy(self.goal)
        
        self.e_loc = [MAX_ROW-1,MAX_COL-1]
        self.moves = {0:self.moveup,1:self.moveright,2:self.movedown,3:self.moveleft}

    def __repr__(self):
        print('Welcome to the game of fifteen ...!!')
        for i in range(MAX_ROW):
            for j in range(MAX_COL):
                print(self.board[i][j],end="")
            print()

        """__repr__ must return something"""    
        return ""

    def shuffle(self):
        """randomize the board using succession of moves"""
        seed()
        for i in range(SHUFFLE_BOARD):
            m = randint(0,3)
            self.moves[m](self.board,self.e_loc)

        """optionaly move the bar to the bottom right corner"""
        for i in range(MAX_ROW):
            self.moves[2](self.board,self.e_loc)
        for i in range(MAX_COL):
            self.moves[1](self.board,self.e_loc)

    def refresh(self):
        system("clear")
        print(self)
        if self.goal == self.board:
            print('Congratulation you won...!!')
            return False
        return True
    

    def move(self,board,e_loc,x,y):
        
        ##check validity of the move
        if self.validity_of_move(e_loc,x,y):
            ##swap
            board[e_loc[0]][e_loc[1]],board[e_loc[0]+x][e_loc[1]+y] = board[e_loc[0]+x][e_loc[1]+y],board[e_loc[0]][e_loc[1]]
            ##update e_loc (emplty location)
            e_loc[0] += x
            e_loc[1] += y

            return board,e_loc

        return board , e_loc

    def validity_of_move(self,e_loc,x,y):
        if e_loc[0]+x < 0 or e_loc[0]+x >3 or e_loc[1]+ y < 0 or e_loc[1] + y < 0 or e_loc[1] + y > 3:
            return False
        return True

    def moveup(self,board,e_loc):
        return self.move(board,e_loc,-1,0)
    
    def movedown(self,board,e_loc):
        return self.move(board,e_loc,1,0)
    
    def moveleft(self,board,e_loc):
        return self.move(board,e_loc,0,-1)

    def moveright(self,board,e_loc):
       return self.move(board,e_loc,0,1)
    
    def solve(self):
        #self.board = deepcopy(self.goal)

        def successors(board,loc):
            b_list = [deepcopy(board),deepcopy(board),deepcopy(board),deepcopy(board),]
            e_loc_list = [list(loc),list(loc),list(loc),list(loc),]
            b_list[0],e_loc_list[0] = self.moveup(b_list[0],e_loc_list[0]) 

            b_list[1],e_loc_list[1] = self.moveright(b_list[1],e_loc_list[1]) 

            b_list[2],e_loc_list[2] = self.movedown(b_list[2],e_loc_list[2]) 

            b_list[3],e_loc_list[3] = self.moveleft(b_list[3],e_loc_list[3]) 

            return [[b_list[0],e_loc_list[0],0],[b_list[1],e_loc_list[1],1],[b_list[2],e_loc_list[2],2],[b_list[3],e_loc_list[3],3]]

        ##searched  = []## naive implementation
        ## lets use the memoized method to get constant time lookup to make the ai more faseter
        searched = set()
        fringe = Queue()
        fringe.put({"board":self.board,"e_loc":self.e_loc,"path":[]})
        while True:
            
            ##base case : quite if no solution is found
            if fringe.empty():
                return []
            
            node = fringe.get()
            if node['board'] == self.goal:
                return node['path']
            
            ##else we will add the node into the searched and then add the successors into the queue
            if str(node['board']) not in searched:
                searched.add(str(node['board']))
                for child in successors(node['board'],node['e_loc']):
                        if str(child[0]) not in searched:
                            fringe.put({"board":child[0],"e_loc":child[1],"path":node['path']+[child[2]]}) 


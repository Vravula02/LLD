class Player:

    def __init__(self,name,color):
        self.name=name
        self.color=color

    def getName(self):
        return self.name

    def getColor(self):
        return self.color

class Board:

    def __init__(self,rows,cols):
        self.rows=rows
        self.cols=cols
        self.grid=[[None for _ in range(self.cols)] for _ in range(self.rows)]

    def canPlace(self,col):

        if col<0 or col>=self.cols:
            return False

        for row in range(self.rows-1,-1,-1):
            if self.grid[row][col] is None:
                return True
        return False

    def place(self,col,color):

        if not self.canPlace(col):
            return "Can not place"

        for row in range(self.rows-1,-1,-1):
            if self.grid[row][col] is None:
                self.grid[row][col]=color
                return row

    def gotWinner(self,row,col):

        color=self.grid[row][col]

        directions=[(1,0),(0,1),(1,1),(1,-1)]

        for dr,dc in directions:
            count=1

            i,j=row+dr,col+dc

            while 0<=i<self.rows and 0<=j<self.cols and self.grid[i][j]==color:
                count+=1

                i+=dr
                j+=dc

            i,j=row-dr,col-dc

            while 0<=i<self.rows and 0<=j<self.cols and self.grid[i][j]==color:
                count+=1

                i-=dr
                j-=dc
        return count>=4

    def isFull(self):

        for col in range(self.cols):
            if self.grid[0][col] is None:
                return False
        return True


class Game:

    def __init__(self,player1,player2,board):
        self.board=board
        self.players=[player1,player2]
        self.playerInd=0
        self.winner=None

    def getCurrentPlayer(self):
        return self.players[self.playerInd]

    def validPlayer(self,player):
        return self.getCurrentPlayer()==player

    def makeMove(self,player,col):

        if self.winner:
            return "Game already finished with the winner as "+self.getWinnerName()

        if self.board.isFull():
            return "Game already finished as a draw "

        if not self.validPlayer(player):
            return "Invalid Player"

        row=self.board.place(col,player.getColor())

        if self.board.gotWinner(row,col):
            self.winner=self.players[self.playerInd]
            return self.winner.getName() + "is the winner and the game is finished"

        if self.board.isFull():
            return "It is a draw game"

        self.playerInd=1-self.playerInd

    def getWinnerName(self):
        return self.winner.getName() if self.winner else "No winner"

    def getWinnerColor(self):
        return self.winner.getColor() if self.winner else "No winner"


from view import View
from maze import Maze
from cardinal import *

class Model:
    """Model implementa um ambiente na forma de um labirinto com paredes e com um agente.
     A indexação da posição do agente é feita sempre por um par ordenado (lin, col). Ver classe Labirinto."""

    def __init__(self, rows, columns):
        """Construtor de modelo do ambiente físico (labirinto)
        @param rows: número de linhas do labirinto
        @param columns: número de colunas do labirinto
        """
        if rows <= 0:
            rows = 6
        if columns <= 0:
            columns = 6

        self.rows = rows
        self.columns = columns

        self.agentPos = [0,0]
        self.rowGoalPos = -1

        self.view = View(self)
        self.maze = Maze(rows,columns)

    def draw(self):
        """Desenha o labirinto em formato texto."""
        self.view.draw()

    def setAgentPos(self, row, col):
        """Utilizada para colocar o agente na posição inicial.
        @param row: a linha onde o agente será situado.
        @param col: a coluna onde o agente será situado.
        @return 1 se o posicionamento é possível, -1 se não for."""
        if (col < 0 or row < 0):
            return -1
        if (col >= self.maze.maxColumns or row >= self.maze.maxRows):
            return -1
        
        if self.maze.walls[row][col] == 1:
            return -1

        if self.maze.walls[row][col] == 2:
            return -1

        self.agentPos[0] = row
        self.agentPos[1] = col
        return 1
    
    def setRowGoalPos(self, row):
        """Utilizada para colocar o objetivo na posição inicial.
        @param row: a linha onde o objetivo será situado.
        @param col: a coluna onde o objetivo será situado.
        @return 1 se o posicionamento é possível, -1 se não for."""
        if (row < 0):
            return -1
        if (row >= self.maze.maxRows):
            return -1
        
        # if self.maze.walls[row][col] == 1:
        #     return -1

        self.rowGoalPos = row
        return 1

    def go(self, direction):
        """Coloca o agente na posição solicitada pela ação go, desde que seja possível.
        Não pode ultrapassar os limites do labirinto nem estar em uma parede.
        @param direciton: inteiro de 0 a 7 representado as coordenadas conforme definido em cardinal.py"""
        row = self.agentPos[0]
        col = self.agentPos[1]

        if direction == N:
            row -= 1
        if direction == L:
            col += 1
        if direction == S:
            row += 1
        if direction == O:
            col -= 1

        # Verifica se está fora do grid
        if col < 0 or col >= self.maze.maxColumns:
            row = self.agentPos[0]
            col = self.agentPos[1]
        if row < 0 or row >= self.maze.maxRows:
            row = self.agentPos[0]
            col = self.agentPos[1]

        # Verifica se bateu em algum obstáculo
        if self.maze.walls[row][col] == 1:
            row = self.agentPos[0]
            col = self.agentPos[1]

        if self.maze.walls[row][col] == 2:
            if self.goBox(direction, row, col) == -1:
                row = self.agentPos[0]
                col = self.agentPos[1]

        self.setAgentPos(row, col)


    def goBox(self, directionBox, row, col):        
        rowBox = row
        colBox = col

        if directionBox == N:
            rowBox -= 1
        if directionBox == L:
            colBox += 1
        if directionBox == S:
            rowBox += 1
        if directionBox == O:
            colBox -= 1
        
        if colBox < 0 or colBox >= self.maze.maxColumns:
            return -1
        if rowBox < 0 or rowBox >= self.maze.maxRows:
            return -1

        if self.maze.walls[rowBox][colBox] == 1:
            return -1
        
        if self.maze.walls[rowBox][colBox] == 2:
            return -1

        #Movo a box para a direcao desejada 
        self.maze.walls[rowBox][colBox] = 2
        return 1
class View:
    """Desenha o ambiente (o que está representado no Model) em formato texto."""
    def __init__(self, model):
        self.model = model

    def drawRowDivision(self):
        print("    ", end='')
        for _ in range(self.model.maze.maxColumns):
            print("+---", end='')
        print("+")

    def drawHeader(self):
        print("--- Estado do Ambiente ---")
        print("Posição agente  : {0},{1}".format(self.model.agentPos[0],self.model.agentPos[1]))
        print("Posição objetivo: {0}\n".format(self.model.rowGoalPos))

        # Imprime números das colunas
        print("   ", end='')
        for col in range(self.model.maze.maxColumns):
            print(" {0:2d} ".format(col), end='')

        print()

    def draw(self):
        """Desenha o labirinto representado no modelo model."""
        self.drawHeader()

        for row in range(self.model.maze.maxRows):
            self.drawRowDivision()
            print(" {0:2d} ".format(row), end='') # Imprime número da linha

            for col in range(self.model.maze.maxColumns):
                if self.model.maze.walls[row][col] == 1: 
                    print("|XXX",end='')    # Desenha parede
                elif self.model.agentPos[0] == row and self.model.agentPos[1] == col:
                    print("|  A",end='')    # Desenha agente
                elif self.model.maze.walls[row][col] == 2:
                    print("|  B",end='')    # Desenha a box
                else:
                    print("|   ",end='')    # Desenha vazio
            
            print("|")
            
            if row == (self.model.maze.maxRows - 1):
                self.drawRowDivision()
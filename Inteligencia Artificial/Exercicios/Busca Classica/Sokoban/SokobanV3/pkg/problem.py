from maze import Maze
from state import State
from cardinal import *

class Problem:
    """Representação de um problema a ser resolvido por um algoritmo de busca clássica.
    A formulação do problema - instância desta classe - reside na 'mente' do agente."""
    def __init__(self):
        self.initialState = State(0,0)
        self.countBoxesGoal = 0

    def createMaze(self, maxRows, maxColumns):
        """Este método instancia um labirinto - representa o que o agente crê ser o labirinto.
        As paredes devem ser colocadas fora desta classe porque este.
        @param maxRows: máximo de linhas do labirinto.
        @param maxColumns: máximo de colunas do labirinto."""
        self.mazeBelief = Maze(maxRows, maxColumns)
        self.maxRows = maxRows
        self.maxColumns = maxColumns
        self.cost = [[0.0 for j in range(maxRows*maxColumns)]for i in range(6)]

    def defInitialState(self, row, col):
        """Define o estado inicial.
        @param row: linha do estado inicial.
        @param col: coluna do estado inicial."""
        self.initialState.row = row
        self.initialState.col = col

    def suc(self, state, action):
        """Função sucessora: recebe um estado e calcula o estado sucessor ao executar uma ação.
        @param state: estado atual.
        @param action: ação a ser realizado a partir do estado state.
        @return estado sucessor"""
        row = state.row
        col = state.col

        # Incrementa a linha e coluna de acordo com a respectiva ação
        # rowIncrement e colIncrement estão definidos em cardinal.py
        row += rowIncrement[action] 
        col += colIncrement[action]

        # Verifica limites
        if row < 0:
            row = 0
        if col < 0:
            col = 0

        if row == self.mazeBelief.maxRows:
            row = self.mazeBelief.maxRows - 1
        if col == self.mazeBelief.maxColumns:
            col = self.mazeBelief.maxColumns - 1
        
        # Se tiver parede agente fica na posição original
        if self.mazeBelief.walls[row][col] == 1: 
            row = state.row
            col = state.col

        if self.mazeBelief.walls[row][col] == 2: 
            if self.sucBox(action, row, col) == -1:
                row = state.row
                col = state.col
        
        return State(row, col)

    def sucBox(self, actionBox, row, col):        
        rowBox = row
        colBox = col

        rowBox += rowIncrement[actionBox] 
        colBox += colIncrement[actionBox]

        if colBox < 0 or colBox >= self.mazeBelief.maxColumns:
            return -1
        if rowBox < 0 or rowBox >= self.mazeBelief.maxRows:
            return -1

        if self.mazeBelief.walls[rowBox][colBox] == 1:
            return -1
        
        if self.mazeBelief.walls[rowBox][colBox] == 2:
            return -1

        self.mazeBelief.walls[row][col] = 0
        #Movo a box para a direcao desejada 
        self.mazeBelief.walls[rowBox][colBox] = 2
        return 1

    def possibleActionsWithoutCollaterals(self, state):
        """Retorna as ações possíveis de serem executadas em um estado, desconsiderando movimentos na diagonal.
        O valor retornado é um vetor de inteiros.
        Se o valor da posição é -1 então a ação correspondente não pode ser executada, caso contrário valerá 1.
        Exemplo: se retornar [1, -1, -1, -1, -1, -1, -1, -1] apenas a ação 0 pode ser executada, ou seja, apena N.
        @param state: estado atual.
        @return ações possíveis"""
        
        actions = [1,1,1,1] # Supõe que todas as ações (menos na diagonal) são possíveis

        # @TODO: Implementação do aluno

        row = state.row
        col = state.col 

        # Esta no limite superior, não pode ir para N
        if row <= 0: 
            actions[N] = -1
        # Esta no limite direito, não pode ir para L
        if col >= self.mazeBelief.maxColumns - 1:
            actions[L] = -1
        # Esta no limite inferior, não pode ir para S
        if row >= self.mazeBelief.maxRows - 1:
            actions[S]= -1
        # Esta no limite esquerdo, não pode ir para O
        if col <= 0:
            actions[O] = -1

        walls = self.mazeBelief.walls
        # Testa se há parede nas direções
        if row - 1 >= 0 and walls[row - 1][col] == 1: # Norte
            actions[N] = -1
        if col + 1 < self.mazeBelief.maxColumns and walls[row][col + 1] == 1: # Leste
            actions[L] = -1
        if row + 1 < self.mazeBelief.maxRows and walls[row + 1][col] == 1: # Sul
            actions[S] = -1
        if col - 1 >= 0 and walls[row][col - 1] == 1: # Oeste
            actions[O] = -1

        # Testa se há box nas direções
        if row - 1 >= 0 and walls[row - 1][col] == 2 and self.possibleBoxActions(row-2, col) == -1: # Norte
            actions[N] = -1
        if col + 1 < self.mazeBelief.maxColumns and walls[row][col + 1] == 2 and self.possibleBoxActions(row, col+2) == -1: # Leste
            actions[L] = -1
        if row + 1 < self.mazeBelief.maxRows and walls[row + 1][col] == 2 and self.possibleBoxActions(row+2, col) == -1: # Sul
            actions[S] = -1
        if col - 1 >= 0 and walls[row ][col - 1] == 2 and self.possibleBoxActions(row, col-2) == -1: # Oeste
            actions[O] = -1

        return actions

    def possibleBoxActions(self, row, col):
        if row <= 0: 
            return -1
        # Esta no limite direito, não pode ir para L
        if col > self.mazeBelief.maxColumns - 1:
            return -1
        # Esta no limite inferior, não pode ir para S
        if row > self.mazeBelief.maxRows - 1:
            return -1
        # Esta no limite esquerdo, não pode ir para O
        if col <= 0:
            return -1

        if self.mazeBelief.walls[row][col] == 1:
            return -1

        if self.mazeBelief.walls[row][col] == 2:
            return -1

        return 1

    def getActionCost(self, action):
        """Retorna o custo da ação.
        @param action:
        @return custo da ação"""
        return 1.0
    
    def goalFinalTest(self):
        """Testa se alcançou o estado objetivo.
        @param currentState: estado atual.
        @return True se o estado atual for igual ao estado objetivo."""
        #Testar aqui se a caixa ja esta na ultima linha
        if self.countBoxesGoal == 4:
            return True
        else: 
            return False

    def goalBoxTest(self):
        """Testa se alcançou o estado objetivo.
        @param currentState: estado atual.
        @return True se o estado atual for igual ao estado objetivo."""
        #Testar aqui se uma caixa atingiu o estado objetivo individualmente
        countBoxes = 0
        walls = self.mazeBelief.walls   
        for col in range(self.mazeBelief.maxColumns):
            if walls[5][col] == 2:
                countBoxes += 1

        if countBoxes > self.countBoxesGoal:
            self.countBoxesGoal = countBoxes
            return True
        else:
            return False

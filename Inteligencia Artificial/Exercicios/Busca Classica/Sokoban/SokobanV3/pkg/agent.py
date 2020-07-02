from model import Model
from problem import Problem
from state import State
from cardinal import action
from tree import TreeNode

UNIFORME_COST = 0
A_START_1 = 1
A_START_2 = 2

# Funções utilitárias
def printExplored(explored):
    """Imprime os nós explorados pela busca.
    @param explored: lista com os nós explorados."""
    #@TODO: Implementação do aluno
    print("--- Explorados --- (TAM: {})".format(len(explored)))
    for stateExp in explored:
        print(stateExp.state,end=' ')
    print("\n")

def printFrontier(frontier):
    """Imprime a fronteira gerada pela busca.
    @param frontier: lista com os nós da fronteira."""
    #@TODO: Implementação do aluno
    print("--- Fronteira --- (TAM: {})".format(len(frontier)))
    for node in frontier:
        print(node,end=' ')
    print("\n")

def buildPlan(solutionNode):
    #@TODO: Implementação do aluno
    depth = solutionNode.depth
    solution = [0 for i in range(depth)]
    parent = solutionNode

    for i in range(len(solution) - 1, -1, -1):
        solution[i] = parent.action
        parent = parent.parent
    return solution


class Agent:
    """"""
    counter = -1 # Contador de passos no plano, usado na deliberação

    def __init__(self, model):
        """Construtor do agente.
        @param model: Referência do ambiente onde o agente atuará."""
        self.model = model

        self.prob = Problem()
        self.prob.createMaze(6,6)
        self.prob.mazeBelief.putVerticalWall(2,4,3)      
        self.prob.mazeBelief.putHorizontalWall(0,1,2)
        self.prob.mazeBelief.putBox(4,1)
        self.prob.mazeBelief.putBox(4,2)
        self.prob.mazeBelief.putBox(3,4)
        self.prob.mazeBelief.putBox(1,3)
      
        # Posiciona fisicamente o agente no estado inicial
        initial = self.positionSensor()
        self.prob.defInitialState(initial.row, initial.col)
        
        # Define o estado atual do agente = estado inicial
        self.currentState = self.prob.initialState

        # Plano de busca
        self.plan = None

    def printPlan(self):
        """Apresenta o plano de busca."""    
        print("--- PLANO ---")
        # @TODO: Implementação do aluno
        for plannedAction in self.plan:
            print("{} > ".format(action[plannedAction]),end='')
        print("FIM\n\n")

    def deliberate(self):
        # Primeira chamada, realiza busca para elaborar um plano
        # @TODO: Implementação do aluno
        if self.counter == -1: 
            self.plan = self.cheapestFirstSearch(1) # 0 = custo uniforme, 1 = A* com colunas, 2 = A* com dist Euclidiana
            if self.plan != None:
                self.printPlan()
            else:
                print("SOLUÇÃO NÃO ENCONTRADA")
                return -1

        # Nas demais chamadas, executa o plano já calculado
        self.counter += 1

        # Atingiu o estado objetivo 
        if self.prob.goalFinalTest():
            print("!!! ATINGIU O ESTADO OBJETIVO !!!")
            return -1
        # Algo deu errado, chegou ao final do plano sem atingir o objetivo
        if self.counter >= len(self.plan):
            print("### ERRO: plano chegou ao fim, mas objetivo não foi atingido.")
            return -1
        currentAction = self.plan[self.counter]

        print("--- Mente do Agente ---")
        print("{0:<20}{1}".format("Estado atual :",self.currentState))
        print("{0:<20}{1} de {2}. Ação= {3}\n".format("Passo do plano :",self.counter + 1,len(self.plan),action[currentAction]))
        self.executeGo(currentAction)

        # Atualiza o estado atual baseando-se apenas nas suas crenças e na função sucessora
        # Não faz leitura do sensor de posição
        self.currentState = self.prob.suc(self.currentState, currentAction)
        return 1

    def executeGo(self, direction):
        """Atuador: solicita ao agente física para executar a ação.
        @param direction: Direção da ação do agente
        @return 1 caso movimentação tenha sido executada corretamente."""
        self.model.go(direction)
        return 1

    def positionSensor(self):
        """Simula um sensor que realiza a leitura do posição atual no ambiente e traduz para uma instância da classe Estado.
        @return estado que representa a posição atual do agente no labirinto."""
        pos = self.model.agentPos
        return State(pos[0],pos[1])

    def hn1(self, state, action):
        """Implementa uma heurísitca - número 1 - para a estratégia A*.
        No caso hn1 é a distância em linhas do estado passado com argumento até a linhas do estado objetivo.
        @param state: estado para o qual se quer calcular o valor de h(n)."""
        distance = 0
        distRow = 0
        distCol = 0
        distColGoal = 0
        for row in range(self.prob.mazeBelief.maxRows - 1):
            for col in range(self.prob.mazeBelief.maxColumns):
                if self.prob.mazeBelief.walls[row][col] == 2:
                    pushesBox = 8
                    # IFs para compracao ao redor da caixa e ver algum cenario de deadlock
                    # consequentemente vejo todas as posicoes ao redor da caixa e 
                    # se a caixa ossui algum obstaculo para movela
                    # se possuir subo o numero de pushesBoes para um numero bem alto
                    # se os movimentos forem livres seto o numero de pushes baseado numa matrix 3 por 3 
                    # e na distancia de manhattan 

                    # Checo se tenho a matrix 3 por 3 em volta da box
                    if (state.col == col - 1 or state.col == col or state.col == col + 1) and (state.row == row - 1 or state.row == row  or state.row == row + 1):
                        pushesBox = 4
                        # vejo se os limites estao dentro da matrix
                        if row - 1 > 0 and col - 1 > 0 and row + 1 < self.prob.maxRows and col + 1 < self.prob.maxColumns:
                            if state.col == col - 1 and state.row == row - 1: # posicao 0,0 na matriz emvolta da Box
                                pushesBox = 2
                            if state.col == col and state.row == row - 1: # posicao 0,1 na matriz emvolta da Box
                                pushesBox = 1
                            if state.col == col + 1 and state.row == row - 1: # posicao 0,2 na matriz emvolta da Box
                                pushesBox = 2
                            if state.col == col - 1 and state.row == row: # posicao 1,0 na matriz emvolta da Box
                                pushesBox = 1 
                            if state.col == col and state.row == row: # posicao 1,1 na matriz emvolta da Box
                                pushesBox = 0
                            if state.col == col + 1 and state.row == row: # posicao 1,2 na matriz emvolta da Box
                                pushesBox = 1 
                            if state.col == col - 1 and state.row == row + 1: # posicao 2,1 na matriz emvolta da Box
                                pushesBox = 2 
                            if state.col == col and state.row == row + 1: # posicao 2,2 na matriz emvolta da Box
                                pushesBox = 1 
                            if state.col == col + 1 and state.row == row + 1: # posicao 2,3 na matriz emvolta da Box
                                pushesBox = 2   
                        # se nao estiverem testo para deadlock   
                        # else:
                    else:
                        # pushesBox = 4
                            #pushesBox = # deixo menos pesado para i para cima do q para baixo pois nas colunas limites 
                            # a caixa so pode so deve se movimentar para baixo
                        # else: 
                        pushesBox = 16
                        # colunas sendo o limite de 0 ou 5 posso testar o movimento para baixo                            
                   
                    distRow = abs(row - 5) # calculo individual da caixa para a linha obj
                    if self.prob.mazeBelief.walls[5][col] == 2:
                        # loop para ver qual objetivo esta mais perto e vazio
                        for colGoal in range(self.prob.mazeBelief.maxColumns): 
                            distColGoal = 5
                            if self.prob.mazeBelief.walls[5][colGoal] != 2:
                                distColGoal = abs(col - colGoal)
                                if distColGoal < distCol:
                                    distCol = distCol + distColGoal
                    else:
                        distCol = 0

                    distance = distance + distRow + distCol + pushesBox

        return distance
    
    def hn2(self, state):
        """Implementa uma heurísitca - número 2 - para a estratégia A*.
        No caso hn1 é a distância distância euclidiana do estado passado com argumento até o estado objetivo.
        @param state: estado para o qual se quer calcular o valor de h(n)."""
        # @TODO: Implementação do aluno
        distCol = abs(state.col - self.prob.goalState.col)
        distRow = abs(state.row - self.prob.goalState.row)
        squared = distRow**2 + distCol**2
        return squared ** 0.5

    def cheapestFirstSearch(self, searchType):
        """Realiza busca com a estratégia de custo uniforme ou A* conforme escolha realizada na chamada.
        @param searchType: 0=custo uniforme, 1=A* com heurística hn1; 2=A* com hn2
        @return plano encontrado"""
        # @TODO: Implementação do aluno
        # Atributos para análise de desempenho
        treeNodesCt = 0 # contador de nós gerados incluídos na árvore
        # nós inseridos na árvore, mas que não necessitariam porque o estado 
        # já foi explorado ou por já estar na fronteira
        exploredDicardedNodesCt = 0
        frontierDiscardedNodesCt = 0 

        # Algoritmo de busca
        solution = None
        solutionBox = []
        root = TreeNode(parent=None)
        root.state = self.prob.initialState
        root.gn = 0
        root.hn = 0
        root.action = -1 
        treeNodesCt += 1

        # cria FRONTEIRA com estado inicial
        frontier = []
        frontier.append(root)

        # cria EXPLORADOS - inicialmente vazia
        explored = []

        print("\n*****\n***** INICIALIZAÇÃO ÁRVORE DE BUSCA\n*****\n")
        print("\n{0:<30}{1}".format("Nós na árvore: ",treeNodesCt))
        print("{0:<30}{1}".format("Descartados já na fronteira: ",frontierDiscardedNodesCt))
        print("{0:<30}{1}".format("Descartados já explorados: ",exploredDicardedNodesCt))
        print("{0:<30}{1}".format("Total de nós gerados: ",treeNodesCt + frontierDiscardedNodesCt + exploredDicardedNodesCt))

        while len(frontier): # Fronteira não vazia
            print("\n*****\n***** Início iteração\n*****\n")
            printFrontier(frontier)

            selNode = frontier.pop(0) # retira nó da fronteira
            selState = selNode.state
            print("Selecionado para expansão: {}\n".format(selNode))

            if self.prob.goalBoxTest():
                solutionBox.append(selNode)
                if self.prob.goalFinalTest():
                    solution = selNode
                    break
            explored.append(selNode)
            printExplored(explored) 

            # Obtem ações possíveis para o estado selecionado para expansão
            actions = self.prob.possibleActionsWithoutCollaterals(selState) # actions é do tipo [-1, -1, -1, 1, 1, -1, -1, -1]
            
            for actionIndex, act in enumerate(actions):
                if(act < 0): # Ação não é possível
                    continue

                # INSERE NÓ FILHO NA ÁRVORE DE BUSCA - SEMPRE INSERE, DEPOIS
                # VERIFICA SE O INCLUI NA FRONTEIRA OU NÃO
                # Instancia o filho ligando-o ao nó selecionado (nSel)  
                child = selNode.addChild()
                # Obtem o estado sucessor pela execução da ação <act>
                sucState = self.prob.suc(selState, actionIndex)
                child.state = sucState
                # Custo g(n): custo acumulado da raiz até o nó filho
                gnChild = selNode.gn + self.prob.getActionCost(actionIndex)
                if searchType == UNIFORME_COST:
                    child.setGnHn(gnChild, 0) # Deixa h(n) zerada porque é busca de custo uniforme
                elif searchType == A_START_1:
                    child.setGnHn(gnChild, self.hn1(sucState,actionIndex))
                elif searchType == A_START_2:
                    child.setGnHn(gnChild, self.hn2(sucState))

                child.action = actionIndex
                # INSERE NÓ FILHO NA FRONTEIRA (SE SATISFAZ CONDIÇÕES)

                # Testa se estado do nó filho foi explorado
                alreadyExplored = False
                # for node in explored:
                #     if child.state == node.state:
                #         alreadyExplored = True
                #         break

                # Testa se estado do nó filho está na fronteira, caso esteja
                # guarda o nó existente em nFront
                nodeFront = None
                if not alreadyExplored:
                    for node in frontier:
                        if(child.state == node.state):
                            nodeFront = node
                            break
                # Se ainda não foi explorado
                if not alreadyExplored:
                    # e não está na fronteira, adiciona à fronteira
                    if nodeFront == None:
                        frontier.append(child)
                        frontier.sort(key=lambda x: x.getFn()) # Ordena a fronteira pelo f(n), ascendente
                        treeNodesCt += 1
                    else:
                        # Se já está na fronteira temos que ver se é melhor
                        if nodeFront.getFn() > child.getFn():       # Nó da fronteira tem custo maior que o filho
                            frontier.remove(nodeFront)              # Remove nó da fronteira (pior e deve ser substituído)
                            nodeFront.remove()                      # Retira-se da árvore 
                            frontier.append(child)                  # Adiciona filho que é melhor
                            frontier.sort(key=lambda x: x.getFn())  # Ordena a fronteira pelo f(n), ascendente
                            # treeNodesCt não é incrementado por inclui o melhor e retira o pior
                        else:
                            # Conta como descartado porque o filho é pior que o nó da fronteira e foi descartado
                            frontierDiscardedNodesCt += 1
                else:
                    exploredDicardedNodesCt += 1
            
            print("\n{0:<30}{1}".format("Nós na árvore: ",treeNodesCt))
            print("{0:<30}{1}".format("Descartados já na fronteira: ",frontierDiscardedNodesCt))
            print("{0:<30}{1}".format("Descartados já explorados: ",exploredDicardedNodesCt))
            print("{0:<30}{1}".format("Total de nós gerados: ",treeNodesCt + frontierDiscardedNodesCt + exploredDicardedNodesCt))


        if(solution != None):
            print("!!! Solução encontrada !!!")
            print("!!! Custo:        {}".format(solution.gn))
            print("!!! Profundidade: {}\n".format(solution.depth))
            print("\n{0:<30}{1}".format("Nós na árvore: ",treeNodesCt))
            print("{0:<30}{1}".format("Descartados já na fronteira: ",frontierDiscardedNodesCt))
            print("{0:<30}{1}".format("Descartados já explorados: ",exploredDicardedNodesCt))
            print("{0:<30}{1}".format("Total de nós gerados: ",treeNodesCt + frontierDiscardedNodesCt + exploredDicardedNodesCt))
            return buildPlan(solution)
        else:
            print("### Solução NÃO encontrada ###")
            return None

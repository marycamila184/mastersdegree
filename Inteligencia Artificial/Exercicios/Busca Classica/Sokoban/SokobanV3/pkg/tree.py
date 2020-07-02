from state import State

class TreeNode:
    """Implementa nó de árvore de busca."""

    def __init__(self, parent):
        """Construtor do nó.
        @param parent: pai do nó construído."""
        self.parent = parent    
        self.state = None   # estado
        self.gn = -1        # g(n) custo acumulado até o nó
        self.hn = -1        # h(n) heurística a partir do nó
        self.depth = 0      # armazena a profundidade do nó
        self.children = []
        self.action = -1    # ação que levou ao estado

    def setGnHn(self, gn, hn):
        """Atribui valores aos atributos gn e hn.
        @param gn: representa o custo acumulado da raiz até o nó.
        @param hn: representa o valor da heurística do nó até o objetivo."""
        self.gn = gn
        self.hn = hn

    def getFn(self):
        """Retorna o valor da função de avaliação f(n)"""
        return self.gn + self.hn

    def addChild(self):
        """Este método instância um nó de self e cria uma associação entre o pai(self) e o filho.
        @return O nó filho instânciado."""
        child = TreeNode(self)
        child.depth = self.depth + 1
        self.children.append(child)
        return child

    def remove(self):
        """Remove-se da árvore cortando a ligação com o nó pai."""
        removed = self.parent.children.remove(self)
        if not removed:
            print("### Erro na remoção do nó: {}".format(self))
            
    def __str__(self):
        return "<{0} g:{1:.2f} h:{2:.2f} f:{3:.2f}>".format(self.state, self.gn, self.hn, self.getFn())

class Maze:
    """Maze representa um labirinto com paredes. A indexação das posições do labirinto é dada por par ordenado (linha, coluna).
    A linha inicial é zero e a linha máxima é (maxLin - 1). A coluna inicial é zero e a máxima é (maxCol - 1)."""

    def __init__(self, maxRows, maxColumns):
        """Construtor do labirinto
        @param maxRows: número de linhas do labirinto
        @param maxColumns: número de colunas do labirinto
        """
        self.maxRows = maxRows
        self.maxColumns = maxColumns
        self.walls = [[0 for j in range(maxColumns)] for i in range(maxRows)] # Matriz que representa o labirinto sendo as posições = 1 aquelas que contêm paredes

    def putHorizontalWall(self, begin, end, row):
        """Constrói parede horizontal da coluna begin até a coluna end(inclusive) na linha row.
        @param begin: coluna inicial entre 0 e maxColumns - 1.
        @param end: coluna final (deve ser maior que begin).
        @param row: linha onde a parede deve ser colocada."""
        if(end >= begin and begin >= 0 and end < self.maxColumns and row >= 0 and row < self.maxRows):
            for col in range(begin,end+1,1):
                self.walls[row][col] = 1
    
    def putVerticalWall(self, begin, end, col):
        """Constrói parede horizontal da linha begin até a linha end(inclusive) na coluna col.
        @param begin: linha inicial entre 0 e maxRows - 1.
        @param end: linha final (deve ser maior que begin).
        @param col: coluna onde a parede deve ser colocada."""
        if(end >= begin and begin >= 0 and end < self.maxRows and col >= 0 and col < self.maxColumns):
            for row in range(begin,end+1,1):
                self.walls[row][col] = 1
    
    def putBox(self, row, col):
        """Constrói parede horizontal da linha begin até a linha end(inclusive) na coluna col.
        @param begin: linha inicial entre 0 e maxRows - 1.
        @param end: linha final (deve ser maior que begin).
        @param col: coluna onde a parede deve ser colocada."""
        if(row >= 0 and row < self.maxRows and col >= 0 and col < self.maxColumns):
            self.walls[row][col] = 2
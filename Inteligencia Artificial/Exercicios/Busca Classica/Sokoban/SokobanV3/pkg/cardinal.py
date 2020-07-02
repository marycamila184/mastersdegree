"""Pontos cardeais: o agente se movimenta em uma direção apontada por um dos pontos cardeais.
São utilizados como parâmetros da ação ir(ponto)"""

N = 0
L = 1
S = 2
O = 3

# Strings que correspondem as ações
action = ["N","L","S","O"]

# Incrementos na linha causado por cada ação
# Exemplo: rowIncrement[0] = rowIncrement[N] = -1 (ao ir para o Norte a linha é decrementada)
rowIncrement = [-1,0,1,0]
# Incrementos na coluna causado por cada ação
# Exemplo: colIncrement[0] = colIncrement[N] = 0 (ao ir para o Norte a coluna não é alterada)
# colIncrement[2] = colIncrement[L] = 1 (ao ir para o Leste a coluna é incrementada)
colIncrement = [0,1,0,-1]
import sys
import random
from common import Common
from individuo import Individuo
from resultado import Resultado

MAX_PESO_MOCHILA = 120
MAX_GENERATIONS = 500
MAX_EXECUCOES = 12
TOTAL_GENES = 42
NP = 15

##Metodo para iniciar a populacao
def iniciaPopulacao(listPop: list):
    if len(listPop) == NP:
        return listPop

    for i in range(NP):
        listInd = generateGenes()
        novoIndividuo = Individuo(listInd, 0, 0, 0)
        listPop.append(novoIndividuo)
        
        for j in range(len(listPop)):
            if listInd == listPop[j].genes and j != 0:
                listPop.remove(novoIndividuo)
            return iniciaPopulacao(listPop)
                        
##Metodo para geracao dos genes aleatoriamente
def generateGenes():
    listIndviduo = []
    for i in range(TOTAL_GENES):
        gene = random.randint(0, 1)
        listIndviduo.append(gene)
    
    return listIndviduo

##Metodo para calculo de fitness, peso total e total de itens
def calculaFitness(objetos, individuos):
    for i in range(len(individuos)):
        somaPeso = 0
        somaValor = 0
        somaItens = 0
        for j in range(TOTAL_GENES):
            if individuos[i].genes[j] == 1:
                somaItens += 1
                somaPeso = somaPeso + objetos[j].peso
                somaValor = somaValor + objetos[j].valor
                    
        individuos[i].fitness = somaValor
        individuos[i].peso = somaPeso
        individuos[i].numItems = somaItens

    return individuos

##Metodo para selecionar individuoes para a nova populacao
def selecionaRoleta(individuos):
    somaFitness = retornaFitnessRoleta(individuos)        
    valorRoleta = random.randint(0, somaFitness) 
    somaSorteio = 0
    indiceSorteado = 0

    for i in range(NP):
        if somaSorteio < valorRoleta:
            somaSorteio = somaSorteio + individuos[i].fitness
        else:
            indiceSorteado = i
            break
              
    return indiceSorteado

##Metodo para somatoria de fitness da roleta
def retornaFitnessRoleta(individuos):
    somaFitness = 0
    for i in range(NP):
        if individuos[i].fitness > 0:
            somaFitness = somaFitness + individuos[i].fitness
    
    return somaFitness

##Metodo para crossover de individuos
def cruzamento(individuos, primIndice, segIndice, pc, pm):
    probCruzamento = random.random()
    novosFilhos = []
    filhoUm = []
    filhoDois = []  

    if probCruzamento <= pc:
        posicaoCruzamento = random.randint(0, TOTAL_GENES - 1)
        
        for i in range(TOTAL_GENES):
            geneUm = 0
            geneDois = 0
            if i <= posicaoCruzamento:
                geneUm = individuos[primIndice].genes[i]
                geneDois = individuos[segIndice].genes[i]
            else:
                geneUm = individuos[segIndice].genes[i]
                geneDois = individuos[primIndice].genes[i]
            filhoUm.append(geneUm)
            filhoDois.append(geneDois)
        
        novosFilhos.append(filhoUm)
        novosFilhos.append(filhoDois)
    
    novosFilhos = mutacao(novosFilhos, pm)  
  
    for i in range(len(novosFilhos)):
        novoFilho = Individuo(novosFilhos[i], 0, 0, 0)
        individuos.append(novoFilho)

    return individuos

##Metodo para mutacao de genes
def mutacao(novosFilhos, pm):
    for i in range(len(novosFilhos)):
        probMutacao = random.random()
        posicoesMutacao = []

        if probMutacao <= pm:
            numeroMutacoes = random.randint(1, TOTAL_GENES)
            for num in range(numeroMutacoes): 
                indiceMutacao = random.randint(0, TOTAL_GENES - 1)
                while indiceMutacao in posicoesMutacao:
                    indiceMutacao = random.randint(0, TOTAL_GENES - 1)

                posicoesMutacao.append(indiceMutacao)

            for indice in range(len(posicoesMutacao)):
                indiceMutacao = posicoesMutacao[indice]
                if novosFilhos[i][indiceMutacao] == 0:
                    novosFilhos[i][indiceMutacao] = 1
                else:
                    novosFilhos[i][indiceMutacao] = 0
    
    return novosFilhos

##Metodo para ordenacao por melhor fitness
def ordenaPorFitness(individuo): 
    return individuo.fitness

#Metodo para Reparar ou penalizar a mochila
def checaPesoMochila(objetos, individuos, penalizar):
    if penalizar:
        mediaFitnessObjetos = 0
        for i in range(len(objetos)):
            mediaFitnessObjetos = mediaFitnessObjetos + objetos[i].valor
        mediaFitnessObjetos = mediaFitnessObjetos/len(objetos)

    for i in range(len(individuos)):
        if individuos[i].peso > MAX_PESO_MOCHILA:
            if penalizar:
                fitnessPenalizado = individuos[i].fitness - mediaFitnessObjetos*(individuos[i].peso - MAX_PESO_MOCHILA)
                individuos[i].fitness = int(fitnessPenalizado)
            else: # Caso Penalizar seja falso entao sei q o metodo escolhido e reparar
                somaPeso = 0
                somaValor = 0
                somaItens = 0

                for j in range(TOTAL_GENES):
                    if individuos[i].genes[j] == 1:
                        pesoComNovoObjeto = somaPeso + objetos[j].peso
                        if pesoComNovoObjeto <= MAX_PESO_MOCHILA:
                            somaItens += 1
                            somaPeso = somaPeso + objetos[j].peso
                            somaValor = somaValor + objetos[j].valor

                        if pesoComNovoObjeto > MAX_PESO_MOCHILA:
                            individuos[i].genes[j] = 0                    
                        
                individuos[i].fitness = somaValor
                individuos[i].peso = somaPeso
                individuos[i].numItems = somaItens

    return individuos

def execucaoAGCanonico(objetos, penalizar, pc, pm):
    melhoresIndividuos = []
    execucao = 1
    
    while execucao < MAX_EXECUCOES:
        individuos = []
        individuos = iniciaPopulacao([])
        individuos = calculaFitness(objetos, individuos)
        geracao = 1
        
        while geracao < MAX_GENERATIONS:
            #Caso não haja mais que um indivíduo com o fitness positivo para o cruzamento
            #então paro a execução e salvo o valor gerado
            numIndFitnessPositivo = 0
            for individuo in individuos:
                if individuo.fitness >= 0:
                    numIndFitnessPositivo += 1
            
            #Caso haja menos de 2 individuos com fitness positivo entao salvo o melhor fitness 
            # e vou para a proxima execucao 
            if numIndFitnessPositivo < 2:
                # melhorInd = Resultado(geracao, individuos[0], individuos[0].fitness, execucao)
                # melhoresIndividuos.append(melhorInd)        
                break
            else:
                sorteioPrimeiro = selecionaRoleta(individuos)
                sorteioSegundo = selecionaRoleta(individuos)           
                #Caso os individuos sejam os mesmos vou sorteando ate serem diferentes
                while sorteioPrimeiro == sorteioSegundo:
                    sorteioSegundo = selecionaRoleta(individuos)

                # print("Primeiro sorteado foi: "+ str(sorteioPrimeiro))
                # print("Segundo sorteado foi: "+ str(sorteioSegundo))

                individuos = cruzamento(individuos, sorteioPrimeiro, sorteioSegundo, pc, pm)
                individuos = calculaFitness(objetos, individuos)

                # Faco a reparacao ou penalizacao
                individuos = checaPesoMochila(objetos, individuos, penalizar)
                    
                individuos.sort(key=ordenaPorFitness, reverse=True)
                if len(individuos) > NP:
                    # Caso tenha sofrido mutacao
                    del individuos[11]
                    del individuos[10]

            melhorInd = Resultado(geracao, individuos[0], individuos[0].fitness, execucao)
            melhoresIndividuos.append(melhorInd)        
            geracao += 1

        execucao+= 1

    return melhoresIndividuos

def main():
    #Inicializo o array com os objetos, pesos e valores
    objetos = Common.inicializaObjetos() 
    geracao = 1      
    melhoresIndividuosReparacao = []
    melhoresIndividuosPenalizacao = []
    Pm = 0.05
    Pc = 0.8
    
    melhoresIndividuosPenalizacao = execucaoAGCanonico(objetos, True, Pc, Pm)        
    melhoresIndividuosPenalizacao.sort(key=ordenaPorFitness, reverse=True)
    with open('out.txt', 'w') as f:
        print("-------------- Informações sobre os melhores individuos - PENALIZAÇÃO --------------", file=f)   

        mochilasComMelhorFitness = []
        mochilasComMelhorFitness.append(melhoresIndividuosPenalizacao[0])
        for i in range(len(melhoresIndividuosPenalizacao)):
            if i!= 0 and melhoresIndividuosPenalizacao[i].fitness == melhoresIndividuosPenalizacao[0].fitness:
                mochilasComMelhorFitness.append(melhoresIndividuosPenalizacao[i])
        
        for i in range(len(mochilasComMelhorFitness)):
            print("Geração:" + str(mochilasComMelhorFitness[i].geracao), file=f) 
            print("Numero de Itens:" + str(mochilasComMelhorFitness[i].individuo.numItems), file=f) 
            print("Peso Total:" + str(mochilasComMelhorFitness[i].individuo.peso), file=f) 
            print("Fitness:" + str(mochilasComMelhorFitness[i].fitness), file=f) 
            print("Execucao:" + str(mochilasComMelhorFitness[i].execucao), file=f) 
            mochila = ""   
            for i in range(len(mochilasComMelhorFitness[i].individuo.genes)):
                mochila += str(mochilasComMelhorFitness[i].individuo.genes[i])
                mochila += ","
            print("Mochila:" + mochila, file=f) 

        mediaFitness = 0
        for i in range(len(melhoresIndividuosPenalizacao)):
            mediaFitness = mediaFitness + melhoresIndividuosPenalizacao[i].fitness
                
        mediaFitness = mediaFitness/len(melhoresIndividuosPenalizacao)
        print("-------------- Metrica para qualidade do algoritmo - PENALIZAÇÃO --------------", file=f)   
        print("Média de fitness dentre as execuções:" + str(mediaFitness), file=f) 

        print("Mochilas com o melhor fitness - Quantidade:" + str(len(mochilasComMelhorFitness)), file=f) 


        
        print("-------------- Informações sobre o melhor individuo - REPARAÇÃO --------------", file=f)   
        melhoresIndividuosReparacao = execucaoAGCanonico(objetos, False, Pc, Pm)
        melhoresIndividuosReparacao.sort(key=ordenaPorFitness, reverse=True)

        mochilasComMelhorFitness = []
        mochilasComMelhorFitness.append(melhoresIndividuosReparacao[0])
        for i in range(len(melhoresIndividuosReparacao)):
            if i!= 0 and melhoresIndividuosReparacao[i].fitness == melhoresIndividuosReparacao[0].fitness:
                mochilasComMelhorFitness.append(melhoresIndividuosReparacao[i])
        
        for i in range(len(mochilasComMelhorFitness)):
            print("Geração:" + str(mochilasComMelhorFitness[i].geracao), file=f) 
            print("Numero de Itens:" + str(mochilasComMelhorFitness[i].individuo.numItems), file=f) 
            print("Peso Total:" + str(mochilasComMelhorFitness[i].individuo.peso), file=f) 
            print("Fitness:" + str(mochilasComMelhorFitness[i].fitness), file=f) 
            print("Execucao:" + str(mochilasComMelhorFitness[i].execucao), file=f) 
            mochila = ""   
            for i in range(len(mochilasComMelhorFitness[i].individuo.genes)):
                mochila += str(mochilasComMelhorFitness[i].individuo.genes[i])
                mochila += ","
            print("Mochila:" + mochila, file=f) 

        print("Mochilas com o melhor fitness - Quantidade:" + str(len(mochilasComMelhorFitness)), file=f) 
        mediaFitness = 0
        for i in range(len(melhoresIndividuosReparacao)):
            mediaFitness = mediaFitness + melhoresIndividuosReparacao[i].fitness
                
        mediaFitness = mediaFitness/len(melhoresIndividuosReparacao)
        print("-------------- Metrica para qualidade do algoritmo - REPARAÇÃO --------------", file=f)     
        print("Média de fitness dentre as execuções:" + str(mediaFitness), file=f) 

if __name__ == '__main__':
    main()

from random import randint, shuffle, random
import matplotlib.pyplot

# numero de cidades e populações
numero_vertices = 100
numero_populacao = numero_vertices * 10

# Cria um grafo na forma de matriz de adjacência
def criar_grafo(nome_arquivo):
    matriz = []
    with open(nome_arquivo, 'r') as arquivo:
        for linha in arquivo:
            valores = list(map(int, linha.split()))
            matriz.append(valores)
    return matriz

# Criar uma população inicial de possiveis caminhos
def populacao_inicial(numero_vertices, numero_populacao):
    populacao = []
    for i in range(numero_populacao):
        vertices = list(range(numero_vertices))
        shuffle(vertices)
        vertices.append(vertices[0])  
        populacao.append(vertices)
    return populacao

# Calcula o fitness para cada caminho da populacao
def fitness(grafo, populacao, numero_vertices, numero_populacao):
    notas = []
    for i in range(numero_populacao):
        distancia = 0
        pop = populacao[i] 
        for j in range(numero_vertices):
            distancia = distancia + grafo[pop[j]][pop[j+1]]
        notas.append(distancia)
    return notas

# Escolhe os pais para fazer crossover
def torneio(populacao, fitness, numero_populacao):
    pais = []
    candidatos = 15
    for _ in range(numero_populacao):
        selecionados = []
        for _ in range(candidatos):
            random_index = randint(0, len(fitness)-1)
            selecionados.append(fitness[random_index])
        selecionados.sort()
        pais.append(populacao[fitness.index(selecionados[0])])        
    return pais

def crossover(selecionados, numero_vertices, numero_populacao):
    filhos = []
    for _ in range(numero_populacao): 
        filho = []
        corte1 = []
        corte2 = []

        pai1 = selecionados[randint(0, (numero_populacao - 1))]
        pai2 = selecionados[randint(0, (numero_populacao - 1))]
        pai2 = pai2[0:numero_vertices]
        
        geneA = int(random() * len(pai1))
        geneB = int(random() * len(pai1))

        incioCorte = min(geneA, geneB)
        fimCorte = max(geneA, geneB)
        
        for i in range(incioCorte, fimCorte):
            corte1.append(pai1[i])
        
        corte2 = [item for item in pai2 if item not in corte1]

        filho = corte1 + corte2
        filho.append(filho[0])
        filhos.append(filho)

    return filhos

def mutacao(populacao, numero_vertices, numero_populacao, taxa_mutacao):
    nova_populacao = []
    for i in range(numero_populacao):
        individuo = populacao[i]
        for x in range(1, numero_vertices):
            if random() < taxa_mutacao:
                troca = randint(1, numero_vertices-1)
                if x != troca:
                    individuo[x], individuo[troca] = individuo[troca], individuo[x]
        nova_populacao.append(individuo)
    return nova_populacao

if __name__ == "__main__":
    valores = []
    grafo = criar_grafo('grafo.txt')
    populacao = populacao_inicial(numero_vertices, numero_populacao)
    
    for gen in range(1000):
        fitness_pop = fitness(grafo , populacao, numero_vertices, numero_populacao)
        menorDistancia = fitness_pop.copy()
        menorDistancia.sort()
        print(f"Geração {gen}:\t{menorDistancia[0]}")
        valores.append(menorDistancia[0])
        selecionados = torneio(populacao, fitness_pop, numero_populacao)
        filhos = crossover(selecionados, numero_vertices, numero_populacao)
        populacao = mutacao(filhos, numero_vertices, numero_populacao, 0.01)

    matplotlib.pyplot.plot(valores)
    matplotlib.pyplot.show()

import matplotlib.pyplot as plt
import networkx as nx

class Grafo:
    def __init__(self, matriz):
        self.matriz = matriz
        self.n = len(matriz)
        self.visitado = [False] * self.n
        self.tempo = 0
        self.low = [0] * self.n
        self.g = [0] * self.n
        self.pai = [-1] * self.n
        self.articulacoes = set()
        self.biconexas = []
        self.pilha = []
        self.arestas_retorno = []

    def dfs(self, u):
        filhos = 0
        self.visitado[u] = True
        self.tempo += 1
        self.g[u] = self.low[u] = self.tempo

        for v in range(self.n):
            if self.matriz[u][v]:
                if not self.visitado[v]:
                    self.pai[v] = u
                    filhos += 1
                    self.pilha.append((u, v))
                    self.dfs(v)

                    self.low[u] = min(self.low[u], self.low[v])

                    if (self.pai[u] == -1 and filhos > 1) or (self.pai[u] != -1 and self.low[v] >= self.g[u]):
                        self.articulacoes.add(u)
                        componente = []
                        while self.pilha and self.pilha[-1] != (u, v):
                            componente.append(self.pilha.pop())
                        if self.pilha:
                            componente.append(self.pilha.pop())
                        self.biconexas.append((u, componente))
                elif v != self.pai[u] and self.g[v] < self.g[u]:
                    self.low[u] = min(self.low[u], self.g[v])
                    self.arestas_retorno.append((u, v))

    def busca_profundidade(self, raiz):
        self.dfs(raiz)

    def mostrar_tabela_lowpt(self):
        print("\nVértice | g(v) | lowpt(v)")
        print("-------------------------")
        for v in range(self.n):
            print(f"   {v+1:2}   |  {self.g[v]:2}  |   {self.low[v]:2}")

    def mostrar_articulacoes(self):
        print("\nArticulações e demarcadores:")
        for art in sorted(self.articulacoes):
            print(f"Vértice {art+1}")

    def mostrar_biconexas(self):
        print("\nComponentes Biconexas:")
        for raiz, comp in self.biconexas:
            comp_formatado = ', '.join([f"({u+1},{v+1})" for u, v in comp])
            print(f"Enraizada em v{raiz+1}: {comp_formatado}")

    def desenhar_grafo(self):
        G = nx.Graph()
        for u in range(self.n):
            for v in range(u, self.n):
                if self.matriz[u][v]:
                    G.add_edge(u+1, v+1)

        pos = nx.spring_layout(G, seed=42)
        nx.draw(G, pos, with_labels=True, node_color='lightblue')
        plt.title('Grafo Original')
        plt.show()

    def desenhar_arvore_dfs(self):
        G = nx.Graph()
        tree_edges = []
        for v in range(self.n):
            u = self.pai[v]
            if u != -1:
                tree_edges.append((u+1, v+1))
                G.add_edge(u+1, v+1)

        back_edges = [(u+1, v+1) for u, v in self.arestas_retorno]
        G.add_edges_from(back_edges)

        pos = nx.spring_layout(G, seed=42)
        nx.draw_networkx_nodes(G, pos, node_color='lightgreen')
        nx.draw_networkx_labels(G, pos)

        nx.draw_networkx_edges(G, pos, edgelist=tree_edges, edge_color='black')
        nx.draw_networkx_edges(G, pos, edgelist=back_edges, edge_color='red', style='dashed')

        plt.title('Árvore DFS (preto) e Arestas de Retorno (vermelho)')
        plt.show()


def ler_matrizes(nome_arquivo):
    with open(nome_arquivo, 'r') as f:
        conteudo = f.read().strip()

    blocos = [bloco.strip().split('\n') for bloco in conteudo.strip().split('\n\n')]
    matrizes = []
    for bloco in blocos:
        if bloco:
            matriz = [list(map(int, linha.strip().split())) for linha in bloco if linha.strip()]
            if matriz:
                matrizes.append(matriz)
    return matrizes


def menu(grafo):
    while True:
        print("\nDigite a Opção Desejada:")
        print("1 - Apresentar Grafo (representação gráfica)")
        print("2 - Apresentar Árvore de Busca em Profundidade")
        print("3 - Apresentar Tabela Lowpt(v) e g(v)")
        print("4 - Listar Articulações com seus Respectivos Demarcadores")
        print("5 - Apresentar Componentes Biconexas")
        print("0 - Sair")

        opcao = input("Opção: ")
        if opcao == '1':
            grafo.desenhar_grafo()
        elif opcao == '2':
            while True:
                try:
                    raiz = int(input(f"Qual será o vértice raiz da busca (1 a {grafo.n})? ")) - 1
                    if 0 <= raiz < grafo.n:
                        break
                    else:
                        print("Vértice inválido.")
                except ValueError:
                    print("Digite um número válido.")
            # Limpa dados anteriores
            grafo.visitado = [False] * grafo.n
            grafo.tempo = 0
            grafo.low = [0] * grafo.n
            grafo.g = [0] * grafo.n
            grafo.pai = [-1] * grafo.n
            grafo.articulacoes = set()
            grafo.biconexas = []
            grafo.pilha = []
            grafo.arestas_retorno = []
            grafo.busca_profundidade(raiz)
            grafo.desenhar_arvore_dfs()
        elif opcao == '3':
            grafo.mostrar_tabela_lowpt()
        elif opcao == '4':
            grafo.mostrar_articulacoes()
        elif opcao == '5':
            grafo.mostrar_biconexas()
        elif opcao == '0':
            break
        else:
            print("Opção inválida.")


def main():
    matrizes = ler_matrizes("grafo.txt")
    print(f"{len(matrizes)} matrizes carregadas.")
    for i in range(len(matrizes)):
        print(f"{i+1} - Matriz {i+1}")

    while True:
        try:
            escolha = int(input("Escolha qual matriz deseja usar: ")) - 1
            if 0 <= escolha < len(matrizes):
                break
            else:
                print("Matriz inválida.")
        except ValueError:
            print("Digite um número válido.")

    grafo = Grafo(matrizes[escolha])
    menu(grafo)


if __name__ == "__main__":
    main()

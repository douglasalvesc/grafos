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

    def dfs(self, v):
        # Implementação baseada no algoritmo da imagem (Jayme, Alg. 4.2)
        self.visitado[v] = True
        self.tempo += 1
        self.g[v] = self.low[v] = self.tempo
        self.pilha.append(v)  # Simula "colocar v na pilha Q"

        for w in range(self.n):
            if self.matriz[v][w]:
                if not self.visitado[w]:
                    # visitar(v, w): aresta de árvore
                    self.pai[w] = v
                    self.dfs(w)
                    self.low[v] = min(self.low[v], self.low[w])
                else:
                    # Se w está na pilha (ancestral) e não são consecutivos em Q, é aresta de retorno
                    if w in self.pilha and w != self.pai[v]:
                        # visitar(v, w): aresta de retorno
                        self.arestas_retorno.append((v, w))

        self.pilha.pop()  # retirar v de Q

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
        import networkx as nx
        import matplotlib.pyplot as plt
        # Grafo só com as arestas de árvore (para layout)
        G_tree = nx.DiGraph()
        tree_edges = []
        for v in range(self.n):
            u = self.pai[v]
            if u != -1:
                tree_edges.append((u+1, v+1))
                G_tree.add_edge(u+1, v+1)

        # Encontrar a raiz (primeiro nó sem pai)
        raiz = None
        for v in range(self.n):
            if self.pai[v] == -1:
                raiz = v+1
                break
        if raiz is None:
            raiz = 1

        # Layout hierárquico só para a árvore
        def hierarchy_pos(G, root, width=1., vert_gap=0.3, vert_loc=0, xcenter=0.5, pos=None, parent=None):
            if pos is None:
                pos = {root: (xcenter, vert_loc)}
            else:
                pos[root] = (xcenter, vert_loc)
            children = [v for u, v in G.edges() if u == root and v != parent]
            if len(children) != 0:
                dx = width / len(children)
                nextx = xcenter - width/2 - dx/2
                for child in children:
                    nextx += dx
                    pos = hierarchy_pos(G, child, width=dx, vert_gap=vert_gap,
                                        vert_loc=vert_loc-vert_gap, xcenter=nextx, pos=pos, parent=root)
            return pos

        pos = hierarchy_pos(G_tree, raiz)

        # Grafo completo para desenhar todas as arestas
        G_full = nx.DiGraph()
        G_full.add_nodes_from(G_tree.nodes())
        G_full.add_edges_from(tree_edges)
        back_edges = [(u+1, v+1) for u, v in self.arestas_retorno]
        for u, v in back_edges:
            G_full.add_edge(u, v)

        nx.draw_networkx_nodes(G_full, pos, node_color='lightgreen', node_size=700)
        nx.draw_networkx_labels(G_full, pos)
        # Arestas de árvore: preto
        nx.draw_networkx_edges(G_full, pos, edgelist=tree_edges, edge_color='black', width=2)
        # Arestas de retorno: vermelho curvado
        arc_rad = 0.3
        for u, v in back_edges:
            if (u, v) not in tree_edges:
                nx.draw_networkx_edges(G_full, pos, edgelist=[(u, v)], edge_color='red', style='dashed', connectionstyle=f'arc3,rad={arc_rad}')
        plt.title('Árvore DFS (preto) e Arestas de Retorno (vermelho)')
        plt.axis('off')
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

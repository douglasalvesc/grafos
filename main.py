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
        self.lowpt_idx = [i for i in range(self.n)]  # novo vetor
        self.gpt_idx = [i for i in range(self.n)]    # novo vetor para g(v)

    def dfs(self, v):
        self.visitado[v] = True
        self.tempo += 1
        self.g[v] = self.tempo
        self.gpt_idx[v] = v  # Inicialmente, g(v) = v
        self.low[v] = self.tempo
        self.lowpt_idx[v] = v
        self.pilha.append(v)

        filhos = 0  # Conta filhos diretos na DFS (importante para raiz)
        for w in range(self.n):
            if self.matriz[v][w]:
                if not self.visitado[w]:
                    self.pai[w] = v
                    filhos += 1
                    self.dfs(w)
                    if self.low[w] < self.low[v]:
                        self.low[v] = self.low[w]
                        self.lowpt_idx[v] = self.lowpt_idx[w]
                    # Verifica condição de articulação (exceto raiz)
                    if self.pai[v] != -1 and self.low[w] >= self.g[v]:
                        self.articulacoes.add(v)
                else:
                    if w in self.pilha and w != self.pai[v]:
                        self.arestas_retorno.append((v, w))
                        # Se encontrar uma aresta de retorno, g(v) deve ser o menor índice alcançável
                        if self.g[w] < self.g[v]:
                            self.g[v] = self.g[w]
                            self.gpt_idx[v] = w
                        if self.g[w] < self.low[v]:
                            self.low[v] = self.g[w]
                            self.lowpt_idx[v] = w

        # Se v é raiz e tem mais de 1 filho, é articulação
        if self.pai[v] == -1 and filhos > 1:
            self.articulacoes.add(v)

        self.pilha.pop()

    def mostrar_articulacoes(self):
        print("\nArticulações e demarcadores (definição da foto):")
        novas_articulacoes = set()
        demarcadores_dict = {}
        for v in range(self.n):
            demarcadores = []
            for w in range(self.n):
                if self.pai[w] == v and (self.lowpt_idx[w] == v or self.lowpt_idx[w] == w):
                    demarcadores.append(w+1)  # +1 para exibir humano
            if demarcadores:
                novas_articulacoes.add(v)
                demarcadores_dict[v] = demarcadores
        if not novas_articulacoes:
            print("Nenhuma articulação encontrada.")
        else:
            for art in sorted(novas_articulacoes):
                print(f"Vértice {art+1}: demarcadores -> {', '.join(map(str, demarcadores_dict[art]))}")

    def busca_profundidade(self, raiz):
        self.dfs(raiz)

    def mostrar_tabela_lowpt(self):
        print("\nVértice | g(v) | vértice g(v) | lowpt(v) | vértice lowpt")
        print("--------------------------------------------------------")
        for v in range(self.n):
            print(f"   {v+1:2}   |  {self.g[v]:2}  |     v{self.gpt_idx[v]+1:2}     |   {self.low[v]:2}    |     v{self.lowpt_idx[v]+1:2}")

    def mostrar_articulacoes_e_demarcadores(self):
        print("\nArticulações e demarcadores (definição da foto):")
        demarcadores_dict = {}
        articulacoes = set()
        for v in range(self.n):
            demarcadores = []
            for w in range(self.n):
                # v é pai de w na árvore DFS e lowpt(w) = v ou w
                if self.pai[w] == v and (self.lowpt_idx[w] == v or self.lowpt_idx[w] == w):
                    demarcadores.append(w+1)  # +1 para exibir humano
            if demarcadores:
                articulacoes.add(v)
                demarcadores_dict[v] = demarcadores
        if not articulacoes:
            print("Nenhuma articulação encontrada.")
        else:
            for art in sorted(articulacoes):
                print(f"Vértice {art+1}: demarcadores -> {', '.join(map(str, demarcadores_dict[art]))}")

    def mostrar_biconexas(self):
        print("\nComponentes Biconexas (definição da foto):")
        biconexas = []
        # Para cada articulação e seus demarcadores, verifica a subárvore de cada demarcador
        for v in range(self.n):
            for w in range(self.n):
                if self.pai[w] == v and (self.lowpt_idx[w] == v or self.lowpt_idx[w] == w):
                    # w é demarcador de v
                    # Verifica se a subárvore de w não contém articulações
                    sub_arvore = self._subarvore(w)
                    contem_articulacao = any(u in self.articulacoes and u != v for u in sub_arvore)
                    if not contem_articulacao:
                        # Os vértices da subárvore de w + v formam uma componente biconexa
                        comp = sorted(list(sub_arvore | {v}))
                        biconexas.append((v, comp))
        if not biconexas:
            print("Nenhuma componente biconexa encontrada.")
        else:
            for v, comp in biconexas:
                comp_humano = ', '.join(f"v{u+1}" for u in comp)
                print(f"Componente biconexa induzida por v{v+1}: {comp_humano}")

    def _subarvore(self, raiz):
        # Retorna o conjunto de vértices da subárvore de DFS enraizada em raiz
        visitados = set()
        def dfs_sub(u):
            visitados.add(u)
            for v in range(self.n):
                if self.pai[v] == u and v not in visitados:
                    dfs_sub(v)
        dfs_sub(raiz)
        return visitados

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
        print("4 - Listar Articulações com seus Respectivos Demarcadores (definição da foto)")
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
            if not any(grafo.g):  # Se g(v) ainda não foi calculado
                print("Executando DFS automaticamente para calcular g(v) e lowpt(v)...")
                grafo.visitado = [False] * grafo.n
                grafo.tempo = 0
                grafo.low = [0] * grafo.n
                grafo.g = [0] * grafo.n
                grafo.pai = [-1] * grafo.n
                grafo.articulacoes = set()
                grafo.biconexas = []
                grafo.pilha = []
                grafo.arestas_retorno = []
                grafo.busca_profundidade(0)
            grafo.mostrar_tabela_lowpt()
        elif opcao == '4':
            grafo.mostrar_articulacoes_e_demarcadores()
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

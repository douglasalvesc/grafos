# Instruções de Uso do Programa de Teoria dos Grafos

Este programa implementa funcionalidades para análise de grafos a partir de matrizes de adjacência, conforme solicitado na disciplina de Teoria dos Grafos.

## Como usar

1. **Arquivo de Entrada**
   - O arquivo `grafo.txt` deve conter uma ou mais matrizes de adjacência, separadas por uma linha em branco.
   - Cada matriz representa um grafo diferente.
   - Exemplo de formato:
     ```
     0 1 1 0
     1 0 0 1
     1 0 0 1
     0 1 1 0
     
     0 1 0 0
     1 0 1 1
     0 1 0 1
     0 1 1 0
     ```

2. **Execução**
   - Execute o arquivo `main.py`.
   - Será exibida a quantidade de matrizes carregadas e você poderá escolher qual deseja analisar.

3. **Menu de Opções**
   - Após escolher a matriz, o seguinte menu será apresentado:
     1. Apresentar Grafo (representação gráfica)
     2. Apresentar Árvore de Busca em Profundidade
     3. Apresentar Tabela Lowpt(v) e g(v)
     4. Listar Articulações com seus Respectivos Demarcadores
     5. Apresentar Componentes Biconexas
     0. Sair

4. **Detalhes das Opções**
   - **1:** Mostra o grafo desenhado.
   - **2:** Solicita o vértice raiz e mostra a árvore DFS.
   - **3:** Exibe a tabela com valores de g(v) e lowpt(v) para cada vértice.
   - **4:** Lista os vértices de articulação e seus demarcadores.
   - **5:** Mostra as componentes biconexas do grafo.

5. **Observações**
   - O programa utiliza apenas bibliotecas padrão e `matplotlib`/`networkx` para visualização.
   - O código é original e não utiliza funções prontas para as operações principais de grafos.

## Requisitos
- Python 3.x
- matplotlib
- networkx

Instale as dependências com:
```
pip install matplotlib networkx
```

---

Dúvidas ou sugestões, entre em contato com o desenvolvedor.

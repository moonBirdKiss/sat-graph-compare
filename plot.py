import networkx as nx
import matplotlib.pyplot as plt


def visulizeGraph(Matrix):
    G = nx.Graph()
    for i in range(len(Matrix)):
        for j in range(len(Matrix)):
            if Matrix[i][j] > 0:
                G.add_edge(i, j)
    nx.draw(G, with_labels=True, font_weight='bold')
    plt.show()

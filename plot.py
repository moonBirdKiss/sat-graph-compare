import networkx as nx
import matplotlib.pyplot as plt


def visulizeGraph(Matrix):
    G = nx.Graph()
    for i in range(len(Matrix)):
        for j in range(len(Matrix)):
            if Matrix[i][j] > 0:
                G.add_edge(i, j)
    nx.draw(G, with_labels=True)
    plt.show()


def visulizeMultiGraph(Matrices):
    G = nx.MultiGraph()
    for index, Matrix in enumerate(Matrices):
        for i in range(len(Matrix)):
            for j in range(len(Matrix)):
                if Matrix[i][j] > 0:
                    G.add_edge(i, j)
        ax = plt.subplot(int("12"+str(index+1)))
        nx.draw(G, with_labels=True, font_weight='bold')
        for spine in ax.spines.values():
            spine.set_edgecolor('black')
    plt.show()


if __name__ == "__main__":
    pass
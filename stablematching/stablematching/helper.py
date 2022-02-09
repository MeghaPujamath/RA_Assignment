import names
import numpy as np
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import io
import matplotlib
matplotlib.use('Agg')

def get_input(size,_gender):
    _list = []
    for i in range(int(size)):
        _list.append(names.get_first_name(gender=_gender))
    
    return _list

def get_random_preferance(to_assign, to_be_assigned):
    preferred_rankings = []

    for x in to_assign : 
        pref = np.random.permutation(to_be_assigned)
        preferred_rankings.append([x,pref.tolist()])

    return dict(preferred_rankings)

def plotgraph(result,preferred_men,preferred_women):
    men = [i[0] for i in result]
    women = [i[1] for i in result]
    edges = [tuple(x) for x in result]

    Bipartite = nx.Graph()

    edges = [tuple(x) for x in result]
    Bipartite.add_nodes_from(men, bipartite=0, label='user')
    Bipartite.add_nodes_from(women, bipartite=1, label='item')

    for row in edges:
        Bipartite.add_edge(row[0], row[1], rating=[preferred_men[row[0]],preferred_women[row[1]]])

    left_or_top = men
    pos = nx.bipartite_layout(Bipartite, left_or_top)

    nx.draw(Bipartite,pos,node_color='#A0CBE2',edge_color='#00bb5e',width=1,
     edge_cmap=plt.cm.Blues,with_labels=True)

    # To add labels to the edges

    #edge_labels = nx.get_edge_attributes(Bipartite,'rating')
    #nx.draw_networkx_edge_labels(Bipartite, pos, edge_labels=edge_labels)

    buf = io.BytesIO()
    plt.savefig(buf, format='svg', bbox_inches='tight')
    image_bytes = buf.getvalue().decode('utf-8')
    buf.close()
    plt.close()
    matplotlib.pyplot.switch_backend('Agg') 

    return image_bytes



def init_free_men(preferred_rankings_men,free_men):
    for man in preferred_rankings_men:
        free_men.append(man)
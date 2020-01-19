import networkx as nx
from collections import namedtuple
import sys
import matplotlib.pyplot as plt

read_line = lambda f: f.readline().replace("\n", "").replace("\r", "").split(" ")

state = namedtuple('state', 'capitan lucky')

# take inputs
def set_inputs(file_path="./input.txt"):
    print('file path is: ' + str(file_path))
    print('opening file')
    # check file is exist
    try:
        f = open(file_path, 'r')
    except OSError:
        # print "Could not open/read file:", file_path
        print("Could not open/read file:", file_path)
        sys.exit()

    G = nx.DiGraph()
    vertex_size, edges_size = map(int, read_line(f))
    print(vertex_size, edges_size)

    # creating nodes
    for i, color in enumerate(read_line(f)):
        G.add_node(i + 1, color=color)
        print(str(i + 1) + ' ' + str(color))
    G.add_node(vertex_size, color='W')  # add final node

    # add edges
    read_line(f)
    for _ in range(edges_size):
	    line = read_line(f)
	    G.add_edge(int(line[0]), int(line[1]), color=str(line[2]))
    return G, vertex_size

def draw_graph(graph, pos):
    # Copied from Git
    colors=('B','R','Y','G','W')	
    plt.style.use(['dark_background'])
    plt.figure(figsize=(8,8),dpi=100)
     # draw nodes
    colored_nodes={}
    for color in colors:
        colored_nodes[color]=[]
    for node in graph.nodes():
        colored_nodes[graph.nodes[node]['color']].append(node)
    for col in colored_nodes:
        nx.draw_networkx_nodes(graph, pos,
                               nodelist=colored_nodes[col],
                               node_color=col, node_size=250, alpha=0.9)

    # draw edges
    colored_edges={}
    for color in colors:
        colored_edges[color]=[]
    for edge in graph.edges:
        colored_edges[graph.edges[edge]['color']].append(edge)
    for col in colored_edges:
        nx.draw_networkx_edges(graph, pos,
                               edgelist=colored_edges[col],
                               width=3, alpha=0.9, edge_color=col)
    # draw network labels
    labels={}
    for node in graph.nodes():
        labels[node]=node  
    # the FINAL NODE is WHITE and labeled as END
    labels[len(graph.nodes())]='end'
    nx.draw_networkx_labels(graph, pos, labels, font_size=8, font_weight='bold')
    
    plt.axis('off')
    plt.show()
    

if len(sys.argv) - 2:
    graph, vertex_size = set_inputs()
else:
    graph, vertex_size = set_inputs(sys.argv[1])

draw_graph(graph,pos=nx.kamada_kawai_layout(graph))

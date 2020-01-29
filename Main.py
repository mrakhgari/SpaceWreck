import networkx as nx
from collections import namedtuple
import sys
import matplotlib.pyplot as plt
import string


def read_line(f): return f.readline().replace(
    "\n", "").replace("\r", "").split()


STATE = namedtuple('STATE', 'R L')


# take inputs
def set_inputs(file_path="./input.txt"):
    print('file path is: ' + str(file_path))
    print('opening file')
    # check file is exist
    try:
        f = open(file_path, 'r')
    except OSError:
        print("Could not open/read file:", file_path)
        sys.exit()

    G = nx.DiGraph()
    vertex_size, edges_size = map(int, read_line(f))
    print(vertex_size, edges_size)

    # creating nodes
    for i, color in enumerate(read_line(f)):
        G.add_node(i, color=color)
    G.add_node(vertex_size - 1, color='W')  # add final node

    r, l = map(int, read_line(f))
    starting_state = STATE(r - 1, l - 1)
    # add edges
    for _ in range(edges_size):
        line = read_line(f)
        print(line)
        G.add_edge(int(line[0]) - 1, int(line[1]) - 1, color=str(line[2]))
    return G, vertex_size, starting_state

# create RUG graph


def create_new_graph(graph, final_node, starting_state):
    G = nx.DiGraph()
    visited = set()

    def move_L(state, next_node):
        if graph.edges()[(state[0], next_node)]['color'] == graph.nodes()[state[1]]['color']:
            next_state = STATE(next_node, state[1])
            G.add_node(next_state)
            if next_state not in visited:
                G.add_edge(state, next_state)
            refurb(next_state)

    def move_R(state, next_node):
        if graph.edges()[(state[1], next_node)]['color'] == graph.nodes()[state[0]]['color']:
            next_state = STATE(state[0], next_node)
            G.add_node(next_state)
            if next_state not in visited:
                G.add_edge(state, next_state)
            refurb(next_state)

    def refurb(state):
        if state in visited:
            return
        visited.add(state)
        for next_left in list(graph.adj.items())[state[0]][1]:
            move_L(state, next_left)
        for next_right in list(graph.adj.items())[state[1]][1]:
            move_R(state, next_right)

    refurb(starting_state)

    return G


def drawRefurbishedGraph(graph, pos):
    # size of plot
    plt.figure(figsize=(10, 10), dpi=100)
    # set up position of graph items

    # draw nodes
    for node in graph.nodes():
        nx.draw_networkx_nodes(graph, pos,
                               nodelist=list(graph.nodes()),
                               node_size=250, node_color='R', alpha=0.9)

    # draw edges
    for edge in graph.edges:
        nx.draw_networkx_edges(graph, pos,
                               edgelist=list(graph.edges()),
                               width=3, alpha=0.9, edge_color='grey')
    # draw network labels
    labels = {}
    for node in graph.nodes():
        # label according to PDF problem statement node labeling standard
        labels[node] = str(node[0]+1)+", "+str(node[1]+1)
    nx.draw_networkx_labels(graph, pos, labels, font_size=5)

    plt.axis('off')
    plt.show()


# drawVanillaGraph:
# draw full graph with colored, numbered nodes and colored, directed edges
def draw_graph(graph, pos):
    # Coppied from Git
    colors = ('B', 'R', 'Y', 'G', 'W')
    plt.style.use(['dark_background'])
    plt.figure(figsize=(8, 8), dpi=100)
    # draw nodes
    colored_nodes = {}
    for color in colors:
        colored_nodes[color] = []
    for node in graph.nodes():
        colored_nodes[graph.nodes[node]['color']].append(node)
    for col in colored_nodes:
        nx.draw_networkx_nodes(graph, pos,
                               nodelist=colored_nodes[col],
                               node_color=col, node_size=250, alpha=0.9)

    # draw edges
    colored_edges = {}
    for color in colors:
        colored_edges[color] = []
    for edge in graph.edges:
        colored_edges[graph.edges[edge]['color']].append(edge)
    for col in colored_edges:
        nx.draw_networkx_edges(graph, pos,
                               edgelist=colored_edges[col],
                               width=3, alpha=0.9, edge_color=col)
    # draw network labels
    labels = {}
    for node in graph.nodes():
        labels[node] = node + 1
    # the FINAL NODE is WHITE and labeled as END
    labels[len(graph.nodes()) - 1] = 'end'
    nx.draw_networkx_labels(
        graph, pos, labels, font_size=8, font_weight='bold')

    plt.axis('off')
    plt.show()

# check that L or R are in final node or not?


def in_des(state, final_state):
    final_state = final_state - 1
    if state[0][0] == final_state or state[0][1] == final_state:
        return True
    return False


# for print result, we need to add the path like the result
def get_path(states, s):
    if states[0][0] == states[1][0]:
        return('L '+str(states[0][1]+1)+'\t// Lucky moves to '+print_node_alpha(states[0][1]+1, s))
    else:
        return('R '+str(states[0][0]+1)+'\t// Rocket moves to '+print_node_alpha(states[0][0]+1, s))


# convert integer to alph
def print_node_alpha(num, s):
    out = ""
    if num == s+1:
        return 'end'
    for _ in range(int((num-1)/26)+1):
        out = out+list(string.ascii_uppercase)[(num-1) % 26]
        num = num-26
    return out


# find a path from bsf's result, we itrate the result for find path
def find_path(tree, final_state):

    finished = False
    out = []
    for i in range(len(tree), 0, -1):
        if finished == False and in_des(tree[i-1], final_state):
            finished = True
            out.append(get_path(tree[i - 1], final_state - 1))
            index = i
        if finished == True and tree[i-1][0] == tree[index - 1][1]:
            index = i
            out.append(get_path(tree[i-1], final_state - 1))
    if finished:
        for i in range(len(out), 0, -1):
            print(out[i-1])
    else:
        print(' NO SOLUTION ')


if len(sys.argv) - 2:
    graph, final_node, starting_state = set_inputs()
else:
    graph, final_node, starting_state = set_inputs(sys.argv[1])

draw_graph(graph, pos=nx.kamada_kawai_layout(graph))
new_graph = create_new_graph(graph, final_node, starting_state)
# uncomment below line for  draw graph
# drawRefurbishedGraph(new_graph, pos=nx.fruchterman_reingold_layout(new_graph))


tree = list(nx.bfs_predecessors(new_graph, starting_state))
print(tree)
find_path(tree, final_node)

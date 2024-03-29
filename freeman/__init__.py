from random import random
from networkx import NetworkXError
from wrapt import ObjectProxy

from .drawing import *
from .exploring import *
from .moving import *
from .analyzing import *
from .simulating import *


def load(path):
    g = nx.read_gml(path, 'id')

    for n in g.nodes:
        if 'pos' in g.nodes[n]:
            raise ValueError('node pos is not allowed in file')
        if 'x' in g.nodes[n]:
            if 'y' in g.nodes[n]:
                x = g.nodes[n]['x']
                y = g.nodes[n]['y']
                g.nodes[n]['pos'] = (x, y)
                del g.nodes[n]['x']
                del g.nodes[n]['y']
            else:
                raise ValueError('node x is not allowed without y')
        else:
            if 'y' in g.nodes[n]:
                raise ValueError('node y is not allowed without x')

    for n, m in g.edges:
        if 'labflip' in g.edges[n, m]:
            value = g.edges[n, m]['labflip']
            if value != 0 and value != 1:
                raise ValueError('edge labflip must be binary')
            g.edges[n, m]['labflip'] = bool(value)

    return Graph(g)


def init(g):
    if isinstance(g, nx.MultiGraph):
        raise NetworkXError('freeman does not support multigraphs')
    for n, m in g.edges:
        if n == m:
            raise NetworkXError('freeman does not support self loops')
    for n in g.nodes:
        if 'pos' not in g.nodes[n]:
            x = random()
            y = random()
            g.nodes[n]['pos'] = (x, y)
    set_nodeframe(g)
    set_edgeframe(g)


def dyads(g, ordered=False):
    if ordered:
        return permutations(g.nodes, 2)
    return combinations(g.nodes, 2)


def triads(g, ordered=False):
    if ordered:
        return permutations(g.nodes, 3)
    return combinations(g.nodes, 3)


def set_each_node(g, key, map):
    values = list(extract_nodes(g, map))
    for n, value in zip(g.nodes, values):
        g.nodes[n][key] = value


def set_each_edge(g, key, map):
    values = list(extract_edges(g, map))
    for (n, m), value in zip(g.edges, values):
        g.edges[n, m][key] = value


def set_all_nodes(g, key, value, filter=None):
    if filter is None:
        nodes = g.nodes
    else:
        nodes = [n for n in g.nodes if filter(n)]
    for n in nodes:
        g.nodes[n][key] = value


def set_all_edges(g, key, value, filter=None):
    if filter is None:
        edges = g.edges
    else:
        edges = [(n, m) for n, m in g.edges if filter(n, m)]
    for n, m in edges:
        g.edges[n, m][key] = value


def unset_nodes(g, key):
    for n in g.nodes:
        if key in g.nodes[n]:
            del g.nodes[n][key]


def unset_edges(g, key):
    for n, m in g.edges:
        if key in g.edges[n, m]:
            del g.edges[n, m][key]


def colorize_communities(g, C):
    map = {}
    for i, c in enumerate(C):
        for n in c:
            map[n] = i

    colorize_nodes(g, map)


def stack_and_track(graphs, targets=None):
    nodes = set.intersection(*(set(g.nodes) for g in graphs))

    if targets is None:
        targets = nodes

    h = nx.DiGraph()

    for j, n in enumerate(nodes):
        prev = None

        for i, g in enumerate(graphs):
            curr = i * len(nodes) + j

            h.add_node(curr)
            h.nodes[curr].update(g.nodes[n])

            if prev is not None and n in targets:
                h.add_edge(prev, curr)

            prev = curr

    return Graph(h)


def skin_seaborn(g):
    g.graph['width'] = 450
    g.graph['height'] = 450
    g.graph['bottom'] = 0
    g.graph['left'] = 0
    g.graph['right'] = 0
    g.graph['top'] = 0

    set_all_nodes(g, 'size', 10)
    set_all_nodes(g, 'style', 'circle')
    set_all_nodes(g, 'bwidth', 0)
    set_all_nodes(g, 'labpos', 'hover')

    set_all_edges(g, 'width', 1)
    set_all_edges(g, 'style', 'solid')
    set_all_edges(g, 'color', (135, 135, 138))
    unset_edges(g, 'label')


def skin_pyvis(g):
    set_all_nodes(g, 'size', 50)
    set_all_nodes(g, 'style', 'circle')
    set_all_nodes(g, 'color', (151, 194, 252))
    set_all_nodes(g, 'bwidth', 1)
    set_all_nodes(g, 'bcolor', (43, 124, 233))

    set_all_edges(g, 'width', 1)
    set_all_edges(g, 'style', 'solid')
    set_all_edges(g, 'color', (43, 124, 233))


class Graph(ObjectProxy):
    def interact(self, path=None, physics=False):
        interact(self, path, physics)
    def draw(self, toolbar=False):
        draw(self, toolbar)

    def extract_nodes(self, map):
        extract_nodes(self, map)
    def extract_edges(self, map):
        extract_edges(self, map)
    def label_nodes(self, map=None, ndigits=2):
        label_nodes(self, map, ndigits)
    def label_edges(self, map=None, ndigits=2):
        label_edges(self, map, ndigits)
    def colorize_nodes(self, map=None):
        colorize_nodes(self, map)
    def colorize_edges(self, map=None):
        colorize_edges(self, map)
    def scale_nodes_size(self, map, lower=None, upper=None):
        scale_nodes_size(self, map, lower, upper)
    def scale_edges_width(self, map, lower=None, upper=None):
        scale_edges_width(self, map, lower, upper)
    def scale_nodes_dark(self, map, lower=None, upper=None, hue=None):
        scale_nodes_dark(self, map, lower, upper, hue)
    def scale_edges_alpha(self, map, lower=None, upper=None, hue=None):
        scale_edges_alpha(self, map, lower, upper, hue)
    def heat_nodes(self, map, lower=None, upper=None, middle=None):
        heat_nodes(self, map, lower, upper, middle)
    def heat_edges(self, map, lower=None, upper=None, middle=None):
        heat_edges(self, map, lower, upper, middle)

    def scatter(self, xmap, ymap):
        scatter(self, xmap, ymap)
    def move(self, key, *args, **kwargs):
        move(self, key, *args, **kwargs)
    def move_inverse(self, key, weight, *args, **kwargs):
        move_inverse(self, key, weight, *args, **kwargs)
    def move_complement(self, key, *args, **kwargs):
        move_complement(self, key, *args, **kwargs)

    def set_nodecol(self, col, map):
        set_nodecol(self, col, map)
    def set_edgecol(self, col, map):
        set_edgecol(self, col, map)
    def distest_nodes(self, x):
        return distest_nodes(self, x)
    def distest_edges(self, x):
        return distest_edges(self, x)
    def cortest_nodes(self, x, y, max_perm=None):
        return cortest_nodes(self, x, y, max_perm)
    def cortest_edges(self, x, y, max_perm=None):
        return cortest_edges(self, x, y, max_perm)
    def chitest_nodes(self, x, y, max_perm=None):
        return chitest_nodes(self, x, y, max_perm)
    def chitest_edges(self, x, y, max_perm=None):
        return chitest_edges(self, x, y, max_perm)
    def reltest_nodes(self, a, b, max_perm=None):
        return reltest_nodes(self, a, b, max_perm)
    def reltest_edges(self, a, b, max_perm=None):
        return reltest_edges(self, a, b, max_perm)
    def mixtest_nodes(self, x, y, max_perm=None):
        return mixtest_nodes(self, x, y, max_perm)
    def mixtest_edges(self, x, y, max_perm=None):
        return mixtest_edges(self, x, y, max_perm)
    def linregress_nodes(self, X, y, *args, **kwargs):
        return linregress_nodes(self, X, y, *args, **kwargs)
    def linregress_edges(self, X, y, *args, **kwargs):
        return linregress_edges(self, X, y, *args, **kwargs)
    def logregress_nodes(self, X, y, *args, **kwargs):
        return logregress_nodes(self, X, y, *args, **kwargs)
    def logregress_edges(self, X, y, *args, **kwargs):
        return logregress_edges(self, X, y, *args, **kwargs)
    def intencode_nodes(self, col, order=None):
        return intencode_nodes(self, col, order)
    def intencode_edges(self, col, order=None):
        return intencode_edges(self, col, order)
    def binencode_nodes(self, col):
        return binencode_nodes(self, col)
    def binencode_edges(self, col):
        return binencode_edges(self, col)
    def displot_nodes(self, x):
        displot_nodes(self, x)
    def displot_edges(self, x):
        displot_edges(self, x)
    def barplot_nodes(self, x, control=None):
        barplot_nodes(self, x, control)
    def barplot_edges(self, x, control=None):
        barplot_edges(self, x, control)
    def linplot_nodes(self, x, y, control=None):
        linplot_nodes(self, x, y, control)
    def linplot_edges(self, x, y, control=None):
        linplot_edges(self, x, y, control)
    def scaplot_nodes(self, x, y, control=None):
        scaplot_nodes(self, x, y, control)
    def scaplot_edges(self, x, y, control=None):
        scaplot_edges(self, x, y, control)
    def matplot_nodes(self, X, control=None):
        matplot_nodes(self, X, control)
    def matplot_edges(self, X, control=None):
        matplot_edges(self, X, control)
    def valcount_nodes(self, x, order=None, transpose=False):
        return valcount_nodes(self, x, order, transpose)
    def valcount_edges(self, x, order=None, transpose=False):
        return valcount_edges(self, x, order, transpose)
    def contable_nodes(self, x, y):
        return contable_nodes(self, x, y)
    def contable_edges(self, x, y):
        return contable_edges(self, x, y)
    def corplot_nodes(self, x, y):
        corplot_nodes(self, x, y)
    def corplot_edges(self, x, y):
        corplot_edges(self, x, y)
    def boxplot_nodes(self, x, y, control=None):
        boxplot_nodes(self, x, y, control)
    def boxplot_edges(self, x, y, control=None):
        boxplot_edges(self, x, y, control)
    def girvan_newman(self):
        girvan_newman(self)
    def corplot_graph(self, nodes, weight='weight', plot=True):
        return corplot_graph(self, nodes, weight, plot)

    def __init__(self, g):
        super().__init__(g)
        init(self)
    def dyads(self, ordered=False):
        return dyads(self, ordered)
    def triads(self, ordered=False):
        return triads(self, ordered)
    def set_each_node(self, key, map):
        set_each_node(self, key, map)
    def set_each_edge(self, key, map):
        set_each_edge(self, key, map)
    def set_all_nodes(self, key, value, filter=None):
        set_all_nodes(self, key, value, filter)
    def set_all_edges(self, key, value, filter=None):
        set_all_edges(self, key, value, filter)
    def unset_nodes(self, key):
        unset_nodes(self, key)
    def unset_edges(self, key):
        unset_edges(self, key)
    def colorize_communities(self, C):
        colorize_communities(self, C)
    def skin_seaborn(self):
        skin_seaborn(self)
    def skin_pyvis(self):
        skin_pyvis(self)

    def copy(self):
        return Graph(self.__wrapped__.copy())
    def to_undirected(self):
        return Graph(self.__wrapped__.to_undirected())
    def to_directed(self):
        return Graph(self.__wrapped__.to_directed())
    def subgraph(self, nodes):
        return Graph(self.__wrapped__.subgraph(nodes))
    def edge_subgraph(self, edges):
        return Graph(self.__wrapped__.edge_subgraph(edges))
    def reverse(self):
        return Graph(self.__wrapped__.reverse())

import networkx as nx
import numpy as np


from pge.init.creator import powerlaw
from pge.model.growth.pa import PADiGrowth
from pge.ranks.rank import estimate_rank


class PACancer3DiGrowth(PADiGrowth):
    def __init__(self, graph, schema, deg, model_param, lims):
        super().__init__(graph, schema, deg, model_param)
        self.frm = "prt"
        self.nws = 0
        self.nws_max = lims

    def new_node_add(self, graph, to, tp, attrs):
        super().new_node_add(graph, to, tp, attrs)

        graph.set_attr(to, self.frm, -1)
        graph.set_attr(to, "nw", 1)
        self.nws += 1

    def new_edge_add(self, gr, attrs):
        if gr.get_nodes_with("nw", 1).size == 0:
            return

        node1 = self.choice(gr, 1, tp="out")[0]
        if gr.get_attr(node1, "nw") == 1:
            node2 = self.choice(gr, 1, tp="in")[0]
        else:
            ids = gr.get_nodes_with("nw", 1)
            probs = np.array([gr.count_in_degree(node) for node in ids]) + self.param[0]
            probs = probs / np.sum(probs)
            probs, ids = probs[probs > 0], ids[probs > 0]
            node2 = np.random.choice(ids, 1, replace=False, p=probs)[0]

        gr.add_edge(node1, node2)
        gr.set_edge_data(node1, node2, attrs[0], attrs[1] + 1)

    def prep(self, graph):
        return graph

    def save(self, gr, to):
        for node in gr.get_ids():
            gr.set_attr(node, "nw-"+self.frm, -1)

        while gr.get_nodes_with("nw-"+self.frm, -1).size != 0:
            for node in gr.get_ids():
                if gr.get_attr(node, "nw-"+self.frm) == -1:
                    if gr.get_attr(node, "nw") == 1:
                        nbrs = gr.get_in_degrees(node)
                        nodes = np.unique(gr.get_attributes(self.frm, nbrs))
                        if np.sum(np.isin([0], nodes)) > 0:
                            gr.set_attr(node, "nw-" + self.frm, 0)
                        elif np.sum(np.isin([1], nodes)) > 0:
                            gr.set_attr(node, "nw-" + self.frm, 1)
                        elif np.sum(np.isin([2], nodes)) > 0:
                            gr.set_attr(node, "nw-" + self.frm, 2)
                        else:
                            gr.set_attr(node, "nw-" + self.frm, 3)
                    else:
                        gr.set_attr(node, "nw-" + self.frm, -2)

        estimate_rank(gr, "one", pers=None)
        nx.write_graphml(gr.get_nx_graph(), to + ".graphml")

    def new_load(self, gr):
        self.nws = 0
        for node in gr.get_ids():
            gr.set_attr(node, self.frm, self.gr.get_attr(node, "prt"))
            gr.set_attr(node, "nw", 0)
        return gr

    def stop(self):
        return self.nws == self.nws_max


class PACancerDiGrowth(PACancer3DiGrowth):
    def __init__(self, graph, schema, deg, model_param, lims):
        super(PACancer3DiGrowth, self).__init__(graph, schema, deg, model_param)
        self.nws_max = lims[0]
        self.outs = powerlaw(self.nws_max, lims[1], ac=0.1)

    def new_node_add(self, graph, to, tp, attrs):
        self.deg[0] = ("const", min(graph.size(), int(self.outs[self.nws])))
        super().new_node_add(graph, to, tp, attrs)
        super().new_node_add(graph, to, 0, attrs)

        graph.set_attr(to, self.frm, -1)
        graph.set_attr(to, "nw", 1)
        self.nws += 1

    def choice(self, graph, sz, tp="in"):
        ids = graph.get_ids(stable=True)[graph.get_attributes(self.frm) != -1]

        if tp == "in":
            probs = np.array([graph.count_in_degree(node) for node in ids]) + self.param[0]
        else:
            probs = np.array([graph.count_out_degree(node) for node in ids]) + self.param[1]
        probs = probs / np.sum(probs)
        probs, ids = probs[probs > 0], ids[probs > 0]
        return np.random.choice(ids, min(sz, ids.size), replace=False, p=probs)


class PACancer2DiGrowth(PACancerDiGrowth):
    def choice(self, graph, sz, tp="in"):
        ids = graph.get_ids(stable=True)

        probs = np.array([graph.count_in_degree(node) + graph.count_out_degree(node) for node in ids]) + self.param
        probs = probs / np.sum(probs)
        return np.random.choice(ids, sz, replace=False, p=probs)

    def new_node_add(self, graph, to, tp, attrs):
        if self.schema[0] == 1:
            self.deg[0] = ("const", min(graph.size(), int(self.outs[self.nws])))
        else:
            self.deg[1] = ("const", min(graph.size(), int(self.outs[self.nws])))
        super(PADiGrowth, self).new_node_add(graph, to, tp, attrs)
        graph.set_attr(to, self.frm, -1)
        graph.set_attr(to, "nw", 1)

        self.nws += 1

def gen_adj_matrix(n, edges):
    adj_matrix_out = [[] for i in range(n+1)]
    adj_matrix_in = [[] for i in range(n+1)]
    for x,y in edges:
        (adj_matrix_out[x]).append(y)
        (adj_matrix_in[y]).append(x)
    return (adj_matrix_out, adj_matrix_in)


def is_dag(n, edges):
    adj_matrix_out, adj_matrix_in = gen_adj_matrix(n, edges)
    active = [True] * (n+1)
    #no. of incoming edges to a node from other active edges
    num_in_edges = [len(adj_matrix_in[i]) for i in range(n+1)]
    #list of nodes with no incoming edge from an active node
    no_dep_nodes_list = [i for i in range(1, n+1) if (not(num_in_edges[i]))]
    ordering = []
    while (no_dep_nodes_list):
        #pick an active node that has no incoming edge from other active nodes
        no_dep_node = no_dep_nodes_list.pop(0)
        ordering.append(no_dep_node)
        #delete this node from the graph
        active[no_dep_node] = False
        for out_node in adj_matrix_out[no_dep_node]:
            #assert: active[out_node] = True
            num_in_edges[out_node] -= 1
            if (not(num_in_edges[out_node])):
                no_dep_nodes_list.append(out_node)
    if (True in active[1:]):
        #assert: a part of the graph could not be put into a topological ordering (the graph has a cycle)
        return False, ordering
    else:
        #assert: the entire graph has been put into a topological ordering
        return True, ordering

g1 = [[1,4],[1,5],[1,7],[2,3],[2,5],[2,6],[3,4],[3,5],[4,5],[5,6],[5,7],[6,7]] #a general DAG
g2 = [[1,4],[1,5],[1,7],[2,3],[2,6],[3,4],[3,5],[4,5],[5,2],[5,6],[5,7],[6,7]] #[2,3,5,2] is a cycle
g3 = [[1,2],[1,3],[2,5],[3,4],[4,5]] #another DAG
g4 = []    #a single node graph
g5 = [[1,2]]    #a single edge graph
g6 = g3 + [[6,7],[6,8],[7,8]] #a graph with two distinct components
g7 = [[1,2],[2,3],[3,4],[4,1]] #a cycle


def test():
    print(is_dag(4, g7))

test()


def gen_adj_matrix(n, edges):
    adj_matrix = [[] for i in range(n+1)]
    for x,y in edges:
        (adj_matrix[x]).append(y)
        (adj_matrix[y]).append(x)
    return adj_matrix

#--------------------------------------------------------------------

#BFS

def bfs(n, edges, start_node=1):
    adj_matrix = gen_adj_matrix(n, edges)
    discovered = [False] * (n+1)
    trav = []
    dist = [-1] * (n+1)
    parent = [-1] * (n+1)
    bfs_tree = []
    nodes_queue = []
    update_structs_on_discovery(start_node, start_node, discovered, trav, dist, parent, bfs_tree, nodes_queue)
    while (nodes_queue):
        node = dequeue(nodes_queue)
        for adj_node in adj_matrix[node]:
            if (not(discovered[adj_node])):
                update_structs_on_discovery(adj_node, node, discovered, trav, dist, parent, bfs_tree, nodes_queue)
    return discovered, trav, dist, parent, bfs_tree


def enqueue(queue, elt):
    queue.append(elt)

def dequeue(queue):
    return queue.pop(0)

def update_structs_on_discovery(node, parent_node, discovered, trav, dist, parent, bfs_tree, nodes_queue):
    discovered[node] = True
    trav.append(node)
    dist[node] = dist[parent_node] + 1
    if (node != parent_node):
        parent[node] = parent_node
        bfs_tree.append((parent_node, node))
    else:
        parent[node] = 0
    enqueue(nodes_queue, node)

#----------------------------------------------------------------------

#DFS

def dfs_recur(n, edges, start_node=1):
    adj_matrix = gen_adj_matrix(n, edges)
    explored = [False] * (n+1)
    trav = []
    parent = [-1] * (n+1)
    dfs_tree = []
    dfs_explore_node(adj_matrix, start_node, start_node, explored, trav, parent, dfs_tree)
    return explored, trav, parent, dfs_tree


def dfs_explore_node(adj_matrix, node, parent_node, explored, trav, parent, dfs_tree):
    explored[node] = True
    trav.append(node)
    if (node != parent_node):
        parent[node] = parent_node
        dfs_tree.append((parent_node, node))
    else:
        parent[node] = 0
    for adj_node in adj_matrix[node]:
        if (not(explored[adj_node])):
            dfs_explore_node(adj_matrix, adj_node, node, explored, trav, parent, dfs_tree)


def dfs(n, edges, start_node=1):
    adj_matrix = gen_adj_matrix(n, edges)
    explored = [False] * (n+1)
    trav = []
    parent = [-1] * (n+1)
    dfs_tree = []
    nodes_stack = []
    parent[start_node] = 0
    push(nodes_stack, start_node)
    #each while loop iteration corresponds to a recursive DFS call
    #explored[i] denotes if recursive DFS has been called on node i or not
    while (nodes_stack):
        node = pop(nodes_stack)
        if (not(explored[node])):
            #recursive DFS call on node
            explored[node] = True
            trav.append(node)
            if (parent[node]): dfs_tree.append((parent[node], node))
            for adj_node in reversed(adj_matrix[node]):
                if (not(explored[adj_node])):    #this condition can be removed
                    parent[adj_node] = node
                    push(nodes_stack, adj_node)
        #backtracking
    return explored, trav, parent, dfs_tree


def push(stack, elt):
    stack.append(elt)

def pop(stack):
    return stack.pop()

#-----------------------------------------------------------------------

#CHECKING BIPARTITENESS

def is_bipartite(n, edges):
    adj_matrix = gen_adj_matrix(n, edges)
    start_node = 1
    color = [0] * (n+1)
    parent = [-1] * (n+1)
    nodes_queue = []
    color_node_on_discovery(start_node, start_node, color, parent, nodes_queue)
    while (nodes_queue):
        node = dequeue(nodes_queue)
        #explore the neighbours of this node
        for adj_node in adj_matrix[node]:
            adj_node_color = color[adj_node]
            if (adj_node_color):
                if (color[node] == adj_node_color):
                    #assert: bipartite coloring of the entire graph not possible (found an odd cycle in the graph)
                    return False, build_odd_cycle(node, adj_node, parent)
            else:
                color_node_on_discovery(adj_node, node, color, parent, nodes_queue)
    #assert: successfully performed the bipartite coloring of entire graph
    return True, color


def color_node_on_discovery(node, parent_node, color, parent, nodes_queue):
    color[node] = decide_color(color[parent_node])
    parent[node] = parent_node if (node != parent_node) else 0
    enqueue(nodes_queue, node)


def decide_color(parent_color):
    if ((not(parent_color)) or (parent_color == 2)):
        return 1
    elif (parent_color == 1):
        return 2


def build_odd_cycle(node, adj_node, parent):
    ancestor = lowest_common_ancestor(node, adj_node, parent)
    path1 = build_path(ancestor, node, parent)
    path2 = build_path(ancestor, adj_node, parent)
    path2.reverse()
    return (path1 + path2)


def lowest_common_ancestor(node, adj_node, parent):
    branch1 = node
    branch2 = adj_node
    while (branch1 != branch2):
        branch1 = parent[branch1]
        branch2 = parent[branch2]
    return branch1


def build_path(ancestor, descendant, parent):
    path = []
    curr_node = descendant
    # starting from the descendant build the path in the reverse direction
    while (curr_node != ancestor):
        path.append(curr_node)
        curr_node = parent[curr_node]
    path.append(curr_node)    # add ancestor to the path
    path.reverse()
    return path

#--------------------------------------------------------------------------

#CHECKING PRESENCE OF CYCLES

def is_cyclic_bfs(n, edges):
    adj_matrix = gen_adj_matrix(n, edges)
    discovered = [False] * (n+1)
    parent = [None] * (n+1)    # to store the BFS tree
    dist = [None] * (n+1)    # needed to find the lowest common ancestor efficiently
    nodes_queue = []
    start_node = 1
    mark_discovered(start_node, None, discovered, parent, dist, nodes_queue)
    while (nodes_queue):
        node = dequeue(nodes_queue)
        for adj_node in adj_matrix[node]:
            if (discovered[adj_node]):
                if (parent[node] != adj_node):
                    #assert: a cycle has been detected
                    return True, build_cycle(node, adj_node, parent, dist)
            else:
                mark_discovered(adj_node, node, discovered, parent, dist, nodes_queue)
    #assert: the graph has no cycle
    return False, []


def mark_discovered(node, parent_node, discovered, parent, dist, nodes_queue):
    discovered[node] = True
    parent[node] = parent_node
    dist[node] = (dist[parent_node] + 1) if (parent_node) else 0
    enqueue(nodes_queue, node)


def build_cycle(node1, node2, parent, dist):
    ancestor = lowest_common_ancestor_gen(node1, node2, parent, dist)
    path1 = build_path(ancestor, node1, parent)
    path2 = build_path(ancestor, node2, parent)
    path2.reverse()
    return (path1 + path2)


def lowest_common_ancestor_gen(node1, node2, parent, dist):
    curr_node1 = node1
    curr_node2 = node2
    if (dist[node1] == (dist[node2] - 1)):
        curr_node2 = parent[node2]
    elif (dist[node1] ==  (dist[node2] + 1)):
        curr_node1 = parent[node1]
    # assert: curr_node1 and curr_node2 are at the same level in the tree
    while (curr_node1 != curr_node2):
        curr_node1 = parent[curr_node1]
        curr_node2 = parent[curr_node2]
    # assert: both curr_node1 and curr_node2 are at the lowest common ancestor of node1, node2
    return curr_node1


def is_cyclic_dfs(n, edges):
    adj_matrix = gen_adj_matrix(n, edges)
    explored = [False] * (n+1)
    parent = [None] * (n+1)    # to store the DFS tree
    start_node = 1
    nodes_stack = []
    record_parent_and_push(start_node, None, parent, nodes_stack)
    while (nodes_stack):
        node = pop(nodes_stack)
        if (not(explored[node])):    # this condition will always be satisfied
            explored[node] = True
            for adj_node in adj_matrix[node]:
                if (explored[adj_node]):
                    if (adj_node != parent[node]):
                        # assert: a cycle has been detected
                        return True, build_cycle_dfs(adj_node, node, parent)
                else:
                    record_parent_and_push(adj_node, node, parent, nodes_stack)
    # assert: there is no cycle in the graph
    return False, []


def record_parent_and_push(node, parent_node, parent, nodes_stack):
    parent[node] = parent_node
    push(nodes_stack, node)


def build_cycle_dfs(ancestor, descendant, parent):
    path = build_path(ancestor, descendant, parent)
    path.append(ancestor)
    return path



#--------------------------------------------------------------------------


def test():
    g1 = [[1,2],[1,3],[2,3],[2,4],[2,5],[3,5],[3,7],[3,8],[4,5],[5,6],[7,8]]    # a general graph with cycles
    g2 = [[1,2],[1,3],[1,4],[3,5],[3,6],[4,7],[7,8],[7,9],[7,10],[9,11]]    # a tree
    g3 = []    # a single node graph
    g4 = [[1,2]]    # a single edge tree
    # Petersen Graph
    g5 = [[1,2],[1,5],[1,6],[2,3],[2,7],[3,4],[3,8],[4,5],[4,9],[5,10],[6,8],[6,9],[7,9],[7,10],[8,10]]
    g6 = [[1,2],[2,3],[3,4],[4,5]]    # a single line with 5 nodes 
    g7 = [[1,2],[1,3],[1,4],[1,5]]    # a hub with 4 spokes
    g8 = [[1,2],[2,3],[3,4],[4,1],[2,5],[2,6],[5,6],[3,7],[3,8],[4,9],[9,10],[4,8],[9,7],[11,1]] # a general graph
    g9 = [[1,2],[2,3],[2,4],[3,4]]    # a simple graph containing a triangle
    g10 = [[1,2],[2,3],[3,4],[4,5],[5,6],[6,1]]    # a hexagon
    g11 = [[1,2],[1,3],[1,4],[2,5],[2,6],[3,7],[3,8],[4,8],[4,9]] # a tree with a 4-cycle
    # a tree with a 7-cycle
    g12 = [[1,2],[1,3],[1,4],[3,5],[3,6],[5,7],[5,8],[6,9],[6,10],[8,11],[8,12],[10,13],[10,14],[11,14]]

    print(is_cyclic_dfs(8, g1))
    print(is_cyclic_dfs(11, g2))
    print(is_cyclic_dfs(1, g3))
    print(is_cyclic_dfs(2, g4))
    print(is_cyclic_dfs(10, g5))
    print(is_cyclic_dfs(5, g6))
    print(is_cyclic_dfs(5, g7))
    print(is_cyclic_dfs(11, g8))
    print(is_cyclic_dfs(4, g9))
    print(is_cyclic_dfs(6, g10))
    print(is_cyclic_dfs(9, g11))
    print(is_cyclic_dfs(14, g12))

test()


import heapq

class UnionFind:
    """
    The Disjoint Set data structure, used in the Kruskal algorithm to detect cycles.
    Includes Path Compression and Union by Rank optimizations.
    """
    def __init__(self, vertices):
        self.parent = {v: v for v in vertices}
        self.rank = {v: 0 for v in vertices}

    def find(self, item):
        if self.parent[item] != item:
            # path compression
            self.parent[item] = self.find(self.parent[item])
        return self.parent[item]

    def union(self, x, y):
        xroot = self.find(x)
        yroot = self.find(y)
        
        if xroot == yroot:
            return False # cycle detected, union not performed

        # union by rank
        if self.rank[xroot] < self.rank[yroot]:
            self.parent[xroot] = yroot
        elif self.rank[xroot] > self.rank[yroot]:
            self.parent[yroot] = xroot
        else:
            self.parent[yroot] = xroot
            self.rank[xroot] += 1
        return True

def kruskal(vertices, edges):
    """
    Kruskal implementation
    :param vertices: ['A', 'B', 'C']
    :param edges: (weight, u, v)
    :return: the edges in the minimum spanning tree and the total weight
    """
    mst = []
    total_weight = 0
    uf = UnionFind(vertices)
    
    # sort edges by weight
    sorted_edges = sorted(edges, key=lambda item: item[0])

    for edge in sorted_edges:
        weight, u, v = edge
        # If u and v are not in the same set, adding this edge will not form a cycle.
        if uf.union(u, v):
            mst.append(edge)
            total_weight += weight

    return mst, total_weight


def kruskal_matrix(vertices, adj_matrix):
    """
    Kruskal's algorithm (adjacency matrix version).
    :param vertices: A list of vertices; their order must match the rows and columns of adj_matrix
    :param adj_matrix: An adjacency matrix in the format matrix[i][j] = weight; use float(‘inf’) for no edges
    :return: A list of edges and the total weight of the minimum spanning tree (or forest)
    """
    edges = []
    n = len(vertices)
    for i in range(n):
        u = vertices[i]
        for j in range(i + 1, n):
            weight = adj_matrix[i][j]
            if weight != float('inf'):
                edges.append((weight, u, vertices[j]))

    return kruskal(vertices, edges)


def prim(graph, start_vertex):
    """
    Implementation of the Prim algorithm.
    :param graph: A dictionary of adjacency lists, in the format {u: [(weight, v), ...]}
    :param start_vertex: The starting vertex
    :return: A list of edges in the minimum spanning tree and the total weight
    """
    mst = []
    visited = set([start_vertex])
    total_weight = 0
    
    # (Min-Heap)，storage format(weight, from_vertex, to_vertex)
    edges = [
        (weight, start_vertex, to_vertex) 
        for weight, to_vertex in graph[start_vertex]
    ]
    heapq.heapify(edges)

    while edges:
        weight, frm, to = heapq.heappop(edges)
        
        if to not in visited:
            visited.add(to)
            mst.append((weight, frm, to))
            total_weight += weight
            
            # Add the edges adjacent to the new vertex to the priority queue
            for next_weight, next_to in graph[to]:
                if next_to not in visited:
                    heapq.heappush(edges, (next_weight, to, next_to))

    return mst, total_weight


def prim_matrix(vertices, adj_matrix, start_vertex):
    """
    Prim's Algorithm (Adjacency Matrix Version).
    :param vertices: A list of vertices; their order must match the rows and columns of adj_matrix
    :param adj_matrix: An adjacency matrix in the format matrix[i][j] = weight; use float(‘inf’) for no edges
    :param start_vertex: The starting vertex
    :return: A list of edges and the total weight of the minimum spanning tree
    """
    if not vertices:
        return [], 0

    vertex_to_index = {vertex: idx for idx, vertex in enumerate(vertices)}
    if start_vertex not in vertex_to_index:
        raise ValueError(f"start_vertex {start_vertex} 不在 vertices 中")

    n = len(vertices)
    in_mst = [False] * n
    min_weight = [float('inf')] * n
    parent = [-1] * n
    total_weight = 0
    mst = []

    start_idx = vertex_to_index[start_vertex]
    min_weight[start_idx] = 0

    for _ in range(n):
        u = -1
        u_weight = float('inf')
        for idx in range(n):
            if not in_mst[idx] and min_weight[idx] < u_weight:
                u_weight = min_weight[idx]
                u = idx

        # 图不连通时，Prim 只覆盖起始点可达分量
        if u == -1 or u_weight == float('inf'):
            break

        in_mst[u] = True

        if parent[u] != -1:
            frm = vertices[parent[u]]
            to = vertices[u]
            weight = adj_matrix[parent[u]][u]
            mst.append((weight, frm, to))
            total_weight += weight

        for v in range(n):
            weight = adj_matrix[u][v]
            if not in_mst[v] and weight < min_weight[v]:
                min_weight[v] = weight
                parent[v] = u

    return mst, total_weight

# ==========================================
# (Logical Checks & Edge Cases)
# ==========================================
if __name__ == "__main__":
    def build_adj_matrix(vertices, edges):
        idx = {v: i for i, v in enumerate(vertices)}
        matrix = [[float('inf')] * len(vertices) for _ in vertices]
        for i in range(len(vertices)):
            matrix[i][i] = 0
        for weight, u, v in edges:
            ui, vi = idx[u], idx[v]
            if weight < matrix[ui][vi]:
                matrix[ui][vi] = weight
                matrix[vi][ui] = weight
        return matrix

    print("--- logic checks and edge cases ---")

    # 1. basic connected graph (Normal Case)
    vertices_1 = ['A', 'B', 'C', 'D']
    edges_1 = [(1, 'A', 'B'), (4, 'A', 'C'), (2, 'B', 'C'), (5, 'B', 'D'), (3, 'C', 'D')]
    graph_1 = {
        'A': [(1, 'B'), (4, 'C')],
        'B': [(1, 'A'), (2, 'C'), (5, 'D')],
        'C': [(4, 'A'), (2, 'B'), (3, 'D')],
        'D': [(5, 'B'), (3, 'C')]
    }
    
    print("\n[test 1: basic connected graph]")
    k_mst, k_weight = kruskal(vertices_1, edges_1)
    p_mst, p_weight = prim(graph_1, 'A')
    p_mst_matrix, p_weight_matrix = prim_matrix(vertices_1, build_adj_matrix(vertices_1, edges_1), 'A')
    print(f"Kruskal weight: {k_weight}, edges: {k_mst}")
    print(f"Prim weight: {p_weight}, edges: {p_mst}")
    print(f"Prim(adjacency matrix) weight: {p_weight_matrix}, edges: {p_mst_matrix}")
    assert k_weight == p_weight == p_weight_matrix == 6, "test for basic connected graph failed"

    # 2. edge case (Disconnected Graph)
    # 预期表现：Kruskal 生成最小生成森林(MSF)，Prim 只能遍历包含起始点的连通分量
    vertices_2 = ['A', 'B', 'C', 'D']
    edges_2 = [(1, 'A', 'B'), (2, 'C', 'D')] # AB 连通，CD 连通，但互相不连通
    graph_2 = {
        'A': [(1, 'B')], 'B': [(1, 'A')],
        'C': [(2, 'D')], 'D': [(2, 'C')]
    }
    
    print("\n[test 2: disconnected graph (edge case)]")
    k_mst_2, k_weight_2 = kruskal(vertices_2, edges_2)
    p_mst_2, p_weight_2 = prim(graph_2, 'A')
    p_mst_matrix_2, p_weight_matrix_2 = prim_matrix(vertices_2, build_adj_matrix(vertices_2, edges_2), 'A')
    print(f"Kruskal's algorithm for generating MSF from a disconnected graph: weight {k_weight_2}, edges {k_mst_2}")
    print(f"Prim's algorithm covers only one side of a disconnected graph: weight {p_weight_2}, edges {p_mst_2}")
    print(f"Prim (Adjacency Matrix) for Handling Disconnected Graphs: weight {p_weight_matrix_2}, edges {p_mst_matrix_2}")

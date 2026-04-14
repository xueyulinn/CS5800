import time
from mst_algorithms import kruskal, prim


def load_roadnet_ca_sample(path, max_lines=50000):
    vertices = set()
    undirected_edges = set()
    count = 0

    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            u, v = line.split()
            vertices.add(u)
            vertices.add(v)
            undirected_edges.add(tuple(sorted((u, v))))

            count += 1
            if count >= max_lines:
                break

    vertices = list(vertices)
    edges = []
    adj_list = {v: [] for v in vertices}

    for u, v in undirected_edges:
        w = 1
        edges.append((w, u, v))
        adj_list[u].append((w, v))
        adj_list[v].append((w, u))

    return vertices, edges, adj_list


def extract_connected_component(edges, graph, start_vertex):
    """
    提取包含 start_vertex 的连通分量，保证 Prim 与 Kruskal 比较的是同一张连通子图。
    """
    visited = set()
    stack = [start_vertex]

    while stack:
        vertex = stack.pop()
        if vertex in visited:
            continue

        visited.add(vertex)
        for _, neighbor in graph[vertex]:
            if neighbor not in visited:
                stack.append(neighbor)

    component_vertices = list(visited)
    component_vertex_set = set(component_vertices)
    component_edges = [
        (weight, u, v)
        for weight, u, v in edges
        if u in component_vertex_set and v in component_vertex_set
    ]
    component_graph = {
        vertex: [
            (weight, neighbor)
            for weight, neighbor in graph[vertex]
            if neighbor in component_vertex_set
        ]
        for vertex in component_vertices
    }

    return component_vertices, component_edges, component_graph


def test():
    v, e, graph = load_roadnet_ca_sample(
        path='dataset/roadNet-CA.txt', max_lines=2000000)
    start_vertex = v[0]
    component_v, component_e, component_graph = extract_connected_component(
        e, graph, start_vertex)

    print(
        f"{'Case':<16} | {'Nodes':<8} | {'Edges':<8} | {'Kruskal Weight':<15} | {'Prim Weight':<15} | "
        f"{'Kruskal Time(s)':<16} | {'Prim Time(s)':<13} | {'Result':<10}"
    )
    print("-" * 130)

    # 测试 Kruskal
    start_k = time.perf_counter()
    _, k_weight = kruskal(component_v, component_e)
    end_k = time.perf_counter()
    kruskal_time = end_k - start_k

    # 测试 Prim
    start_p = time.perf_counter()
    _, p_weight = prim(component_graph, start_vertex)
    end_p = time.perf_counter()
    prim_time = end_p - start_p

    result = "PASS" if k_weight == p_weight else "FAIL"

    print(
        f"{'roadNet-CA':<16} | {len(component_v):<8} | {len(component_e):<8} | {k_weight:<15} | {p_weight:<15} | "
        f"{kruskal_time:<16.6f} | {prim_time:<13.6f} | {result:<10}"
    )


if __name__ == "__main__":
    test()

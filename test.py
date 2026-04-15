import time
import random
from mst_algorithms import kruskal, prim


def generate_connected_random_graph(n, edge_multiplier=2):
    """
    生成一个保证连通的随机图。
    n: 顶点数量
    edge_multiplier: 边的密集程度（n * multiplier）
    """
    vertices = [str(i) for i in range(n)]
    edges = []
    edge_set = set()
    adj_list = {v: [] for v in vertices}

    # 步骤1: 先生成一棵树确保图是连通的
    nodes = list(vertices)
    random.shuffle(nodes)
    for i in range(len(nodes) - 1):
        u, v = nodes[i], nodes[i+1]
        w = random.randint(1, 100)
        edges.append((w, u, v))
        edge_set.add(tuple(sorted((u, v))))
        adj_list[u].append((w, v))
        adj_list[v].append((w, u))

    # 步骤2: 添加额外的边增加复杂度
    current_edge_count = len(edges)
    max_edge_count = n * (n - 1) // 2
    target_edge_count = min(n * edge_multiplier, max_edge_count)
    while current_edge_count < target_edge_count:
        u, v = random.sample(vertices, 2)
        edge_key = tuple(sorted((u, v)))
        if edge_key in edge_set:
            continue

        w = random.randint(1, 100)
        edges.append((w, u, v))
        edge_set.add(edge_key)
        adj_list[u].append((w, v))
        adj_list[v].append((w, u))
        current_edge_count += 1

    return vertices, edges, adj_list


def build_graph(vertices, edge_tuples):
    """
    根据边列表构建 Kruskal/Prim 共用的输入格式。
    edge_tuples: [(weight, u, v), ...]
    """
    adj_list = {v: [] for v in vertices}
    for weight, u, v in edge_tuples:
        adj_list[u].append((weight, v))
        adj_list[v].append((weight, u))
    return vertices, edge_tuples, adj_list


def generate_complete_graph(n):
    """
    生成完全无向图，边数为 n * (n - 1) / 2，用于真正的稠密图测试。
    """
    vertices = [str(i) for i in range(n)]
    edges = []

    for i in range(n):
        for j in range(i + 1, n):
            w = random.randint(1, 100)
            edges.append((w, vertices[i], vertices[j]))

    return build_graph(vertices, edges)


def generate_extreme_test_cases():
    """
    构造一些结构上的极端测试用例，而不只是随机规模变化。
    """
    return [
        ("single-node", *build_graph(['0'], [])),
        (
            "minimal-tree",
            *build_graph(
                ['0', '1'],
                [(7, '0', '1')]
            ),
        ),
        (
            "tree-only",
            *build_graph(
                ['0', '1', '2', '3', '4'],
                [(3, '0', '1'), (2, '1', '2'), (5, '1', '3'), (4, '3', '4')]
            ),
        ),
        (
            "duplicate-edges",
            *build_graph(
                ['0', '1', '2', '3'],
                [
                    (10, '0', '1'),
                    (1, '0', '1'),
                    (5, '1', '2'),
                    (2, '2', '3'),
                    (8, '0', '3'),
                    (3, '1', '3'),
                ],
            ),
        ),
        (
            "equal-weights",
            *build_graph(
                ['0', '1', '2', '3'],
                [
                    (1, '0', '1'),
                    (1, '1', '2'),
                    (1, '2', '3'),
                    (1, '3', '0'),
                    (1, '0', '2'),
                    (1, '1', '3'),
                ],
            ),
        ),
        ("dense-complete", *generate_complete_graph(500)),
    ]


def run_extensive_test():
    # 随机图测试：(顶点数, 边数约为 顶点数 * multiplier)
    # 前三组观察规模增长，后三组在 500 个顶点下观察密度增长。
    random_test_cases = [
        ("sparse-50", 50, 2),
        ("sparse-200", 200, 2),
        ("sparse-500", 500, 2),
        ("medium-500", 500, 20),
        ("dense-500", 500, 80),
    ]
    extreme_test_cases = generate_extreme_test_cases()

    print(
        f"{'Case':<16} | {'Nodes':<8} | {'Edges':<8} | {'Kruskal Weight':<15} | {'Prim Weight':<15} | "
        f"{'Kruskal Time(s)':<16} | {'Prim Time(s)':<13} | {'Result':<10}"
    )
    print("-" * 130)

    for case_name, n, mult in random_test_cases:
        v, e, adj = generate_connected_random_graph(n, mult)
        start_vertex = '0'

        # 测试 Kruskal
        start_k = time.perf_counter()
        _, k_weight = kruskal(v, e)
        end_k = time.perf_counter()
        kruskal_time = end_k - start_k

        # 测试 Prim
        start_p = time.perf_counter()
        _, p_weight = prim(adj, start_vertex)
        end_p = time.perf_counter()
        prim_time = end_p - start_p

        result = "PASS" if k_weight == p_weight else "FAIL"

        print(
            f"{case_name:<16} | {n:<8} | {len(e):<8} | {k_weight:<15} | {p_weight:<15} | "
            f"{kruskal_time:<16.6f} | {prim_time:<13.6f} | {result:<10}"
        )

    for case_name, v, e, adj in extreme_test_cases:
        start_vertex = v[0]
        # 测试 Kruskal
        start_k = time.perf_counter()
        _, k_weight = kruskal(v, e)
        end_k = time.perf_counter()
        kruskal_time = end_k - start_k

        # 测试 Prim
        start_p = time.perf_counter()
        _, p_weight = prim(adj, '0')
        end_p = time.perf_counter()
        prim_time = end_p - start_p

        result = "PASS" if k_weight == p_weight else "FAIL"

        print(
            f"{case_name:<16} | {len(v):<8} | {len(e):<8} | {k_weight:<15} | {p_weight:<15} | "
            f"{kruskal_time:<16.6f} | {prim_time:<13.6f} | {result:<10}"
        )


if __name__ == "__main__":
    run_extensive_test()

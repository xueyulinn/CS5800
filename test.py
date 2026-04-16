import time
import random
from mst_algorithms import kruskal_matrix, prim_matrix


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

    # Step 1: First, generate a tree to ensure the graph is connected.
    nodes = list(vertices)
    random.shuffle(nodes)
    for i in range(len(nodes) - 1):
        u, v = nodes[i], nodes[i+1]
        w = random.randint(1, 100)
        edges.append((w, u, v))
        edge_set.add(tuple(sorted((u, v))))
        adj_list[u].append((w, v))
        adj_list[v].append((w, u))

    # Step 2: Add additional edges to increase the complexity
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


def generate_connected_random_graph_by_density(n, density):
    """
    生成指定密度的连通无向图。
    density: (0, 1]，目标边密度，相对于完全图边数 n*(n-1)/2。
    """
    if not (0 < density <= 1):
        raise ValueError("density 必须在 (0, 1] 范围内")

    vertices = [str(i) for i in range(n)]
    edges = []
    edge_set = set()
    adj_list = {v: [] for v in vertices}

    # 先生成一棵随机树，保证连通
    nodes = list(vertices)
    random.shuffle(nodes)
    for i in range(len(nodes) - 1):
        u, v = nodes[i], nodes[i + 1]
        w = random.randint(1, 100)
        edges.append((w, u, v))
        edge_set.add(tuple(sorted((u, v))))
        adj_list[u].append((w, v))
        adj_list[v].append((w, u))

    max_edge_count = n * (n - 1) // 2
    target_edge_count = int(max_edge_count * density)
    target_edge_count = max(n - 1, min(target_edge_count, max_edge_count))

    while len(edges) < target_edge_count:
        u, v = random.sample(vertices, 2)
        edge_key = tuple(sorted((u, v)))
        if edge_key in edge_set:
            continue

        w = random.randint(1, 100)
        edges.append((w, u, v))
        edge_set.add(edge_key)
        adj_list[u].append((w, v))
        adj_list[v].append((w, u))

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


def build_adj_matrix(vertices, edge_tuples):
    """
    根据边列表构建 Prim(邻接矩阵版本) 的输入。
    """
    index = {v: i for i, v in enumerate(vertices)}
    n = len(vertices)
    matrix = [[float('inf')] * n for _ in range(n)]

    for i in range(n):
        matrix[i][i] = 0

    for weight, u, v in edge_tuples:
        ui, vi = index[u], index[v]
        if weight < matrix[ui][vi]:
            matrix[ui][vi] = weight
            matrix[vi][ui] = weight

    return matrix


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


def generate_structured_test_cases():
    """
    构造特殊结构测试用例。
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
        (
            "negative-weights",
            *build_graph(
                ['0', '1', '2', '3'],
                [
                    (-2, '0', '1'),
                    (3, '0', '2'),
                    (-1, '1', '2'),
                    (4, '1', '3'),
                    (2, '2', '3'),
                ],
            ),
        ),
        (
            "self-loop",
            *build_graph(
                ['0', '1', '2'],
                [
                    (1, '0', '0'),
                    (2, '0', '1'),
                    (3, '1', '2'),
                    (10, '0', '2'),
                ],
            ),
        ),
    ]


def generate_dense_complete_test_cases():
    """
    构造 dense-complete 测试用例。
    """
    cases = []
    dense_complete_sizes = [80, 120, 160, 220,
                            300, 400, 500, 650, 800, 1000, 1200]
    for n in dense_complete_sizes:
        cases.append((f"dense-complete-{n}", *generate_complete_graph(n)))
    return cases


def generate_grouped_random_test_cases():
    """
    让 sparse 和 dense 分组排列（不交错）。
    """
    sizes = [200, 500, 1500, 3000, 8000, 15000]
    sparse_multiplier = 3
    dense_multiplier = 120

    cases = []
    for n in sizes:
        cases.append((f"sparse-{n}", n, sparse_multiplier))

    for n in sizes:
        cases.append((f"dense-{n}", n, dense_multiplier))
    return cases


def run_matrix_benchmark():
    """
    直接比较 matrix 实现：Kruskal(matrix) vs Prim(matrix)。
    每个用例仅执行一次计时，不取平均。
    """
    random.seed(42)
    # 仅保留 dense / complete，用高密度与更大规模提升 Prim(matrix) 的优势概率
    dense_cases = [
        ("dense-500-20", 500, 0.20),
        ("dense-700-30", 700, 0.30),
        ("dense-900-40", 900, 0.40),
        ("dense-1100-50", 1100, 0.50),
        ("dense-1300-60", 1300, 0.60),
    ]
    complete_cases = [300, 400, 500, 600, 700, 800, 900, 1000]

    print("\n[Matrix Benchmark] Kruskal(matrix) vs Prim(matrix)")
    print(
        f"{'Case':<13} | {'Nodes':<7} | {'Edges':<9} | {'Density':<8} | "
        f"{'KruskalM Time(s)':<17} | {'PrimM Time(s)':<14} | {'Winner':<8} | {'Result':<6}"
    )
    print("-" * 118)

    all_cases = []
    for case_name, n, density in dense_cases:
        all_cases.append((case_name, n, density, False))
    for n in complete_cases:
        all_cases.append((f"complete-{n}", n, 1.0, True))

    for case_name, n, density, is_complete in all_cases:
        if is_complete:
            vertices, edges, _ = generate_complete_graph(n)
        else:
            vertices, edges, _ = generate_connected_random_graph_by_density(n, density)

        adj_matrix = build_adj_matrix(vertices, edges)
        start_vertex = vertices[0]

        start_k = time.perf_counter()
        _, k_weight = kruskal_matrix(vertices, adj_matrix)
        end_k = time.perf_counter()
        kruskal_time = end_k - start_k

        start_p = time.perf_counter()
        _, p_weight = prim_matrix(vertices, adj_matrix, start_vertex)
        end_p = time.perf_counter()
        prim_time = end_p - start_p

        winner = "Kruskal" if kruskal_time < prim_time else "Prim"
        result = "PASS" if k_weight == p_weight else "FAIL"
        actual_density = len(edges) / (n * (n - 1) / 2)

        print(
            f"{case_name:<13} | {n:<7} | {len(edges):<9} | {actual_density:<8.2%} | "
            f"{kruskal_time:<17.6f} | {prim_time:<14.6f} | {winner:<8} | {result:<6}"
        )


if __name__ == "__main__":
    run_matrix_benchmark()

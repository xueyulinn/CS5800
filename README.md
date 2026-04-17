# CS 5800 Algorithm Project: Kruskal's vs. Prim's

This project implements and compares two greedy algorithms for finding a Minimum Spanning Tree (MST):

- `Kruskal`
- `Prim`

## Team Members
- Lexin Yi - Implementation & Correctness
- Yulin Xue - Test Case Design & Performance Analysis
- Hanfei Yang - Overall Check & Presentation

## Project Structure
- `mst_algorithms.py`: Core implementations of Kruskal and Prim.
- `test.py`: Random tests plus several extreme edge cases.
- `test_roadNet-CA.py`: Real-world dataset test using a sample from `dataset/roadNet-CA.txt`.
- `dataset/roadNet-CA.txt`: California road network dataset.
- `README.md`: Project overview and run instructions.

## Requirements
- Python `3.8+`

## How to Run

### 1. Basic Correctness Check
Runs the small built-in examples in `mst_algorithms.py`.

```bash
python mst_algorithms.py
```

### 2. Random and Extreme Test Cases
Runs generated graph tests, including:

- small / medium / large random connected graphs
- single-node graph
- minimal tree
- tree-only graph
- duplicate-edge graph
- equal-weight graph
- dense complete graph

```bash
python test.py
```

The output includes:

- number of nodes
- number of edges
- Kruskal MST weight
- Prim MST weight
- runtime of each algorithm
- pass/fail consistency check

### 3. Real Dataset Test
Runs the MST comparison on a sampled subgraph from `dataset/roadNet-CA.txt`.

```bash
python test_roadNet-CA.py
```

## Dataset Notes

### roadNet-CA format
`roadNet-CA.txt` is an edge list file:

- lines starting with `#` are comments
- each data line contains `FromNodeId ToNodeId`

Example:

```txt
0 1
0 2
1 0
```

In `test_roadNet-CA.py`, the file is converted into:

- `vertices`: list of node ids
- `edges`: list of `(weight, u, v)` for Kruskal
- `adj_list`: adjacency list for Prim

The current script assigns weight `1` to every road edge so the dataset can be used with the existing MST implementations.

## Why Kruskal and Prim May Differ on a Sampled Dataset

If the sampled graph is not connected:

- `Kruskal` returns a minimum spanning forest over all connected components
- `Prim(start_vertex)` only explores the connected component containing `start_vertex`

So directly comparing their total weights on a disconnected graph is not valid.

To make the comparison fair, `test_roadNet-CA.py` first extracts the connected component containing the chosen start vertex, then runs both algorithms on that same connected subgraph.

## Current Limitation

The full `roadNet-CA` dataset is very large:

- about `1,965,206` nodes
- about `5,533,214` edges

Running the current pure-Python implementation on the full dataset is likely to be slow and memory-intensive. The provided script therefore samples only part of the file.

## Possible Next Steps

1. Extract the largest connected component instead of the first reachable component.
2. Use real edge weights if a weighted road dataset is available.
3. Benchmark runtime across multiple sample sizes.
4. Plot Kruskal vs. Prim runtime as graph size increases.

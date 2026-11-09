# Nodex — Network Connectivity Simulator

Nodex is a Python 3 console-based, graph-driven simulation of a small computer-lab network. A manually implemented **undirected adjacency matrix** tracks up to 10 devices. Its BFS uses an indexed queue, and DFS uses recursion and a visited array.

## Quick start

Open the repository root in VS Code. In the integrated terminal:

```powershell
py --version
py main.py
py -m unittest discover -s tests -p "test_*.py" -v
```

On installations where `python` is on PATH, substitute `python` for `py`. Requires Python 3 and **no third-party packages**. On Windows, if `python` opens a Microsoft Store prompt, use the `py` launcher or fix the Python PATH/app execution aliases.

**Important:** The real entry point is the repository's root-level `main.py`, not `src/main.py`.

## Console operation

The app initializes **five** device records (IDs 101–105) and three valid connections on startup. Device 105 is intentionally disconnected, so BFS/DFS can demonstrate the option to include all components. Data is in memory for each run; changes do not persist after exit.

The numbered menu repeats until **0 — Exit**:

1. Add device
2. Remove device
3. Connect devices
4. Disconnect devices
5. Search device
6. Display network topology (devices, matrix, adjacency list)
7. Breadth-first search (BFS)
8. Depth-first search (DFS)
9. Count devices
10. Check direct link

The console validates numeric input, blank fields, negative IDs/port counts, duplicate IDs, missing devices, self-links, over-capacity insertions, and invalid menu choices. Graph methods handle link duplication and port exhaustion. Each attempted graph operation displays time and auxiliary-space complexity. Set `GROUP_NAME` in `main.py` to the official section and group number before producing final submission screenshots.

## Structure

```text
main.py                     # Input/output and menu, one NetworkGraph instance
models/device.py            # Device ID, hostname, type, port capacity
structures/graph.py         # Custom adjacency-matrix NetworkGraph
algorithms/bfs.py           # Manual queue BFS
algorithms/dfs.py           # Recursive DFS
tests/test_console.py       # Menu and integration tests
tests/test_graph.py         # Graph correctness tests
tests/test_device.py        # Device tests
tests/bfs_check.py          # Traversal checks
tests/dfs_check.py          # Traversal checks
DEFENSE_NOTES.md            # Graph and traversal explanations
```

## Integration contract

```python
from models.device import Device
from structures.graph import NetworkGraph

graph = NetworkGraph(enforce_port_capacity=True)
graph.add_device(Device(10, "Router-A", "Router", 4))
graph.add_device(Device(20, "Switch-B", "Switch", 8))
graph.connect_devices(10, 20)
print(graph.search_device(10).hostname)
print(graph.get_device_count())
print(graph.is_directly_connected(10, 20))
graph.display_graph()
print(graph.bfs(10))
print(graph.dfs(10, include_disconnected=True))
```

Mutation methods return `True` or `False` and print diagnostics. `search_device` returns a `Device` or `None`. `get_device_count` returns an integer. Traversals return device **IDs**, not list positions, and throw `ValueError` for unknown starting IDs on nonempty graphs; they return `[]` on empty graphs. Neighbor exploration follows ascending array index order.

## Operation complexity

Let **V** be the active device count (at most 10), **C = 10** the fixed capacity, and auxiliary space exclude persistent graph storage and terminal output.

| Operation | Time | Auxiliary space |
| --- | --- | --- |
| Create graph | O(C²) | O(1) beyond the stored O(C²) matrix |
| Search / find index | O(V) | O(1) |
| Add device | O(V) | O(1) |
| Remove device (matrix reindex) | O(V²) | O(1) |
| Connect / disconnect | O(V) | O(1) |
| Count used ports | O(V) | O(1) |
| Check direct link | O(V) | O(1) |
| Count devices | O(1) | O(1) |
| Display topology | O(V²) | O(1) |
| BFS | O(V²) | O(V) |
| DFS | O(V²) | O(V) |

An adjacency-matrix traversal scans up to V columns per visited device; its time bound is O(V²), not O(V+E). Traversal result lists use O(V) additional output space. IDs stay stable even when internal indexes shift during deletion.

## Submission tasks still required

The console code and tests do **not** replace the remaining course deliverables: a reviewed/approved PR, official team name, real console screenshots (at least six), the 5–8-page PDF report, a 10-minute defense and the final `Section_GroupNo_Nodex` package. Run and review tests locally before accepting this work.

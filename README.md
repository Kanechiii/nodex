# Nodex — Graph and Traversal Issue

Console-only Python. Data storage uses a fixed 10-device list and a manually constructed **undirected 10×10 adjacency matrix**. No `dict`, `set`, `deque`, or graph libraries are used for the data structure or traversals. `unittest` is used only for tests.

## Files

```text
nodex_issue/
├── main.py                  # Standalone integration demo; do not overwrite teammate's main.py
├── models/
│   ├── __init__.py
│   └── device.py
├── structures/
│   ├── __init__.py
│   └── graph.py
├── algorithms/
│   ├── __init__.py
│   ├── bfs.py
│   └── dfs.py
└── tests/
    ├── __init__.py
    ├── test_device.py
    ├── test_graph.py
    ├── bfs_check.py
    └── dfs_check.py
```

## Run in VS Code terminal

Open the `nodex_issue` folder as the workspace, then:

```bash
python main.py
python -m unittest discover -s tests -p '*.py' -v
```

## Integration contract

```python
from models.device import Device
from structures.graph import NetworkGraph

graph = NetworkGraph(enforce_port_capacity=True)
graph.add_device(Device(10, "Router-A", "Router", 4))
graph.add_device(Device(20, "Switch-B", "Switch", 8))
graph.connect_devices(10, 20)

# Values returned are DEVICE IDS, not current array indexes:
print(graph.bfs(10))   # [10, 20]
print(graph.dfs(10))   # [10, 20]
print(graph.bfs(10, include_disconnected=True))
print(graph.dfs(10, include_disconnected=True))
```

If the graph is empty, either traversal returns `[]`. On a nonempty graph, an unknown starting device ID raises `ValueError` (catch this in the console menu and show its message). By default only the reachable component is traversed. Set `include_disconnected=True` to start additional traversals from the lowest unvisited **array index** after completing the initial component. Neighbors are scanned in ascending array-index order. Traversal never mutates graph state.

All add/remove/connect/disconnect operations print a diagnostic and return a success Boolean. Searching returns the `Device` instance or `None`; `find_device_index` returns a zero-based array index or `-1`. `get_device_count()` returns an integer. `display_graph()` prints index-to-ID mapping, matrix, and adjacency list.

## Purpose and complexity

Let **V** be the current number of devices (0–10), and **C=10** be the fixed capacity. Auxiliary space excludes persistent stored records/matrix and excludes the returned traversal order unless stated otherwise.

| Operation | Purpose | Time | Auxiliary space |
|---|---|---|---|
| `Device(...)` | Construct a device record | O(1) | O(1) |
| `Device.display_info` | Print one device | O(1) | O(1) |
| `NetworkGraph(...)` | Allocate 10 slots and 10×10 matrix | O(C²) | O(1) beyond O(C²) stored graph |
| `find_device_index(id)` | Find unique ID's current array index | O(V) | O(1) |
| `search_device(id)` | Get a record by ID | O(V) | O(1) |
| `get_device_count()` | Get active count | O(1) | O(1) |
| `add_device(device)` | Validate and add record | O(V) | O(1) |
| `remove_device(id)` | Remove record, incident links, compact matrix | O(V²) | O(1) |
| `count_used_ports(index)` | Count links from an active array index | O(V) | O(1) |
| `connect_devices(a, b)` | Add symmetric edge; enforce ports optionally | O(V) | O(1) |
| `disconnect_devices(a, b)` | Clear both symmetric edge entries | O(V) | O(1) |
| `is_directly_connected(a, b)` | Test immediate connection | O(V) | O(1) |
| `display_graph()` | Print indexed devices, matrix, derived list | O(V²) | O(1) excluding terminal output |
| `bfs(id, include_disconnected=False)` | Visit in breadth-first order | O(V²) | O(V) queue + visited; output O(V) |
| `dfs(id, include_disconnected=False)` | Visit in depth-first recursive preorder | O(V²) | O(V) visited + recursion; output O(V) |

Operation	              Purpose	                                  Time	Auxiliary space
find_device_index()	      Find a device's array position	          O(V)	O(1)
add_device()	          Add unique device	                          O(V)	O(1)
remove_device()	          Remove device and reindex matrix	          O(V²)	O(1)
search_device()	          Retrieve device record	                  O(V)	O(1)
connect_devices()	      Connect two devices	                      O(V)	O(1)
disconnect_devices()      Remove a connection	                      O(V)	O(1)
count_used_ports()	      Count a device's links	                  O(V)	O(1)
is_directly_connected()	  Check direct connectivity	                  O(V)	O(1)
get_device_count()	      Return total devices	                      O(1)	O(1)
display_graph()	          Print devices and matrix	                  O(V²)	O(1)
bfs()	                  Level-by-level traversal	                  O(V²)	O(V)
dfs()	                  Recursive depth-first traversal	          O(V²)	O(V)


Because capacity is fixed at 10, operations are bounded in actual use. Their O(V) / O(V²) forms express how their work depends on the active number of devices, which is useful for project defense. With an adjacency matrix, scanning one vertex's neighbors checks V columns, so a traversal visiting V vertices takes O(V²), not O(V+E).

## Console integration review checklist (teammate's code not supplied)

- **One shared graph instance.** Do not create a fresh `NetworkGraph` on every menu action.
- **Input ID versus index.** All menu-facing methods accept `device_id` except the internal helper `count_used_ports(index)`; never pass display indexes as IDs.
- **Import names.** Use `from structures.graph import NetworkGraph` and `from models.device import Device` with the repo root as the working directory.
- **Return values.** Display traversal results returned as lists; use Boolean results of mutations to report success/failure without inventing success.
- **Exceptions.** Catch `ValueError` from `graph.bfs` and `graph.dfs` when the chosen starting device ID does not exist; validate user-entered numeric input where appropriate.
- **Disconnected choice.** Specify whether the user wants reachable-only or all components (`include_disconnected=True`). The starting device's component always comes first.
- **Removal.** Graph compacting changes current array indexes; continue identifying devices by stable IDs.
- **Validation.** Check full capacity, duplicates, missing IDs, self-links, existing links, port limits and isolated nodes via the menu.
- **No forbidden helpers.** Do not replace the queue with `collections.deque`, and do not replace the graph with dictionaries or sets if course rules prohibit those.


See `DEFENSE_NOTES.md` for how to explain BFS/DFS at the final defense.

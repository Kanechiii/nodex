# Nodex — Final Defense Notes

## Short explanation to present

> "Our Nodex network is an undirected graph: each device is a vertex, and each direct physical connection is an edge. We store at most ten devices in a fixed array, and our 10-by-10 adjacency matrix uses 1 for a connection and 0 otherwise. The matrix is symmetric because links work in both directions. Each device has a unique ID, which we map to its current array index before accessing the matrix."
>
> "BFS explores a starting device's neighbors first, then the next level. We implemented our own queue using a Python list with front and rear integer indexes. DFS explores each neighbor recursively before it backtracks. Both use a visited Boolean array to prevent revisiting devices in cycles. We scan neighbor indexes in ascending order, so our tests have reproducible output."
>
> "A disconnected graph has multiple groups. Our default traversals return the group reachable from the requested start ID; the optional all-components mode continues from other unvisited indexes. An isolated device appears by itself. An empty graph returns an empty list; an invalid start ID in a nonempty graph raises a ValueError for the console menu to display."

## Trace this simple example

```text
        ID 20
        /   \
     ID 10  ID 40
        \   /
        ID 30

Array index order: [10, 20, 30, 40]
Edges: (10,20), (10,30), (20,40), (30,40)
```

- `graph.bfs(10)` returns `[10, 20, 30, 40]`: 10; then its neighbors 20 and 30; then 40.
- `graph.dfs(10)` returns `[10, 20, 40, 30]`: take the lowest-index unvisited neighbor at each step, then backtrack.
- Both scans skip already visited devices, preventing infinite cycles.

## Likely questions and short answers

**Why a 10×10 matrix?** The project caps active devices at ten. A matrix directly represents every possible pair and makes direct edge lookup O(1) *once the indexes are known*. Finding IDs first costs O(V).

**How does removing a device work?** Shift its device record left, move rows above the deleted row, move columns left over the deleted column, zero the unused row and column, and decrement count. All surviving IDs and edges remain correct.

**Why isn't BFS O(V+E)?** That bound assumes an adjacency list. Here the algorithms check every matrix column for each visited row, giving O(V²) time, even if there are few edges.

**Does traversal use built-in queues or visited sets?** No. BFS uses a basic list of length V plus manual front/rear indexes; DFS uses recursive calls; both use `[False] * V` for visited.

**Does the result include every device?** Only reachable devices by default. The `include_disconnected=True` option handles all components, starting with the selected start device.

**What happens with invalid input?** On an empty graph, return `[]`. For a missing starting ID in a nonempty graph, raise `ValueError`; the console layer catches and prints the message.

**Can DFS overflow?** Recursive DFS can overflow on very large graphs, but Nodex is explicitly limited to 10 devices, so this implementation's maximum depth is 10.


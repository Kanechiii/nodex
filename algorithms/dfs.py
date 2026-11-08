"""Depth-first search using recursion and a visited array."""


def dfs_traversal(graph, start_device_id, include_disconnected=False):
    """Return device IDs in deterministic recursive DFS preorder.

    By default, visit only the component containing start_device_id.
    If include_disconnected=True, visit other components afterward,
    choosing each next root by ascending array index.

    An empty graph returns []. An unknown starting ID on a nonempty
    graph raises ValueError. Does not modify the graph.

    For V active devices in an adjacency matrix:
      Time: O(V^2), scanning neighbors in ascending index order.
      Auxiliary space: O(V) for visited plus up to V recursive frames.
      Returned result: an additional O(V) list of device IDs.

    Recursion is safe here because the graph has at most 10 devices.
    """
    count = graph.get_device_count()
    if count == 0:
        return []

    start_index = graph.find_device_index(start_device_id)
    if start_index == -1:
        raise ValueError(f"Start device ID {start_device_id!r} does not exist.")

    visited = [False] * count
    order = []

    def visit(index):
        visited[index] = True  # Mark BEFORE exploring edges to avoid cycles.
        order.append(graph.devices[index].device_id)

        for neighbor in range(count):
            if graph.adjacency_matrix[index][neighbor] == 1 and not visited[neighbor]:
                visit(neighbor)

    visit(start_index)

    if include_disconnected:
        for index in range(count):
            if not visited[index]:
                visit(index)

    return order

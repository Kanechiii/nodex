"""Depth-first search using recursion and a visited array."""


def dfs_traversal(graph, start_device_id, include_disconnected=False):
    """Traverse a graph recursively in ascending neighbor-index order.

    Returns device IDs; can include all disconnected components.
    Empty graph returns []; invalid start ID raises ValueError.
    Time O(V²); auxiliary space O(V), plus O(V) output.
    """
    size = graph.get_device_count()
    if size == 0:
        return []

    start_idx = graph.find_device_index(start_device_id)
    if start_idx == -1:
        raise ValueError(f"Start device ID {start_device_id!r} does not exist.")

    visited = [False] * size
    order = []

    def visit(index):
        visited[index] = True
        order.append(graph.devices[index].device_id)

        for neighbor in range(size):
            if graph.adjacency_matrix[index][neighbor] == 1 and not visited[neighbor]:
                visit(neighbor)

    visit(start_idx)

    if include_disconnected:
        for index in range(size):
            if not visited[index]:
                visit(index)

    return order

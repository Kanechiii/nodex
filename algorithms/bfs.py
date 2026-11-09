"""Breadth-first search using a manually indexed fixed-size queue."""


def bfs_traversal(graph, start_device_id, include_disconnected=False):
    """Traverse a graph with a manually indexed queue.

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
    queue = [0] * size
    front = 0
    rear = 0
    order = []

    def visit_component(root_idx):
        nonlocal front, rear
        visited[root_idx] = True
        queue[rear] = root_idx
        rear += 1

        while front < rear:
            current = queue[front]
            front += 1
            order.append(graph.devices[current].device_id)

            for neighbor in range(size):
                if graph.adjacency_matrix[current][neighbor] == 1 and not visited[neighbor]:
                    visited[neighbor] = True
                    queue[rear] = neighbor
                    rear += 1

    visit_component(start_idx)

    if include_disconnected:
        for index in range(size):
            if not visited[index]:
                visit_component(index)

    return order

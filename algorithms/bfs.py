"""Breadth-first search using a manually indexed fixed-size queue."""


def bfs_traversal(graph, start_device_id, include_disconnected=False):
    """Return device IDs in deterministic BFS order.

    By default, visit only the component containing start_device_id.
    If include_disconnected=True, visit other components afterward,
    choosing each next root by ascending array index.

    An empty graph returns []. An unknown starting ID on a nonempty
    graph raises ValueError. Does not modify the graph.

    For V active devices in an adjacency matrix:
      Time: O(V^2), including scanning neighbors in ascending index order.
      Auxiliary space: O(V) for the queue and visited array.
      Returned result: an additional O(V) list of device IDs.
    """
    count = graph.get_device_count()
    if count == 0:
        return []

    start_index = graph.find_device_index(start_device_id)
    if start_index == -1:
        raise ValueError(f"Start device ID {start_device_id!r} does not exist.")

    visited = [False] * count
    queue = [0] * count       # Manual queue, never uses pop(0) or deque.
    front = 0                 # Next item to remove.
    rear = 0                  # Next free position (each vertex queued once).
    order = []

    def visit_component(root_index):
        nonlocal front, rear
        visited[root_index] = True
        queue[rear] = root_index
        rear += 1

        while front < rear:
            current = queue[front]
            front += 1
            order.append(graph.devices[current].device_id)

            for neighbor in range(count):
                if graph.adjacency_matrix[current][neighbor] == 1 and not visited[neighbor]:
                    visited[neighbor] = True  # Mark WHEN enqueued to avoid duplicates.
                    queue[rear] = neighbor
                    rear += 1

    visit_component(start_index)

    if include_disconnected:
        for index in range(count):
            if not visited[index]:
                visit_component(index)

    return order

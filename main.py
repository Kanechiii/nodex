"""Example integration only. The teammate can call these same graph methods."""

from models.device import Device
from structures.graph import NetworkGraph


def demo():
    graph = NetworkGraph(enforce_port_capacity=True)
    graph.add_device(Device(101, "Router-A", "Router", 3))
    graph.add_device(Device(102, "Switch-B", "Switch", 3))
    graph.add_device(Device(103, "PC-C", "Computer", 2))
    graph.add_device(Device(104, "Server-D", "Server", 1))
    graph.add_device(Device(105, "Printer-E", "Printer", 1))

    graph.connect_devices(101, 103)
    graph.connect_devices(101, 102)
    graph.connect_devices(102, 104)
    graph.connect_devices(103, 104)  # Rejected: Server-D's single port is used.

    graph.display_graph()

    # Calls made by a console menu: use IDs, not current array indexes.
    try:
        print("BFS (reachable):", graph.bfs(101))
        print("DFS (reachable):", graph.dfs(101))
        print("BFS (all components):", graph.bfs(101, include_disconnected=True))
        print("DFS (all components):", graph.dfs(101, include_disconnected=True))
    except ValueError as error:
        print("Traversal error:", error)


if __name__ == "__main__":
    demo()

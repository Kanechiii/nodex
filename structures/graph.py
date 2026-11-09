from models.device import Device
from algorithms.bfs import bfs_traversal
from algorithms.dfs import dfs_traversal


class NetworkGraph:
    """Undirected graph with a fixed 10-device adjacency matrix."""

    def __init__(self, enforce_port_capacity=True):
        """Create device slots and matrix. Time O(C²); stored space O(C²)."""
        self.max_devices = 10
        self.device_count = 0
        self.enforce_port_capacity = enforce_port_capacity
        self.devices = [None] * self.max_devices
        self.adjacency_matrix = []

        for _ in range(self.max_devices):
            self.adjacency_matrix.append([0] * self.max_devices)

    def find_device_index(self, device_id):
        """Find index by ID or return -1. Time O(V); space O(1)."""
        for i in range(self.device_count):
            if self.devices[i].device_id == device_id:
                return i
        return -1

    def search_device(self, device_id):
        """Find a device by ID. Time O(V); space O(1)."""
        index = self.find_device_index(device_id)
        return None if index == -1 else self.devices[index]

    def get_device_count(self):
        """Return active-device count. Time O(1); auxiliary space O(1)."""
        return self.device_count

    def add_device(self, device):
        """Insert a valid, unique device. Time O(V); space O(1)."""
        if not isinstance(device, Device):
            print("Error: Expected a Device record.")
            return False
        if self.find_device_index(device.device_id) != -1:
            print("Error: Duplicate device ID.")
            return False
        if self.device_count >= self.max_devices:
            print("Error: Network is full. Maximum 10 devices.")
            return False
        if type(device.port_capacity) is not int or device.port_capacity < 0:
            print("Error: Port capacity must be a non-negative integer.")
            return False

        self.devices[self.device_count] = device
        self.device_count += 1
        print(f"Device {device.hostname} added successfully.")
        return True

    def remove_device(self, device_id):
        """Remove a device and its links; compact the matrix. Time O(V²); space O(1)."""
        index = self.find_device_index(device_id)
        if index == -1:
            print("Error: Device not found.")
            return False

        last = self.device_count - 1
        for i in range(index, last):
            self.devices[i] = self.devices[i + 1]
        self.devices[last] = None
        for i in range(index, last):
            for j in range(self.device_count):
                self.adjacency_matrix[i][j] = self.adjacency_matrix[i + 1][j]
        for j in range(index, last):
            for i in range(last):
                self.adjacency_matrix[i][j] = self.adjacency_matrix[i][j + 1]
        for i in range(self.max_devices):
            self.adjacency_matrix[last][i] = 0
            self.adjacency_matrix[i][last] = 0

        self.device_count -= 1
        print(f"Device {device_id} removed successfully.")
        return True

    def count_used_ports(self, index):
        """Count links by array index, not ID. Time O(V); space O(1)."""
        used_ports = 0
        for j in range(self.device_count):
            used_ports += self.adjacency_matrix[index][j]
        return used_ports

    def connect_devices(self, device_id1, device_id2):
        """Connect two device IDs. Time O(V); space O(1)."""
        index1 = self.find_device_index(device_id1)
        index2 = self.find_device_index(device_id2)
        if index1 == -1 or index2 == -1:
            print("Error: One or both devices not found.")
            return False
        if index1 == index2:
            print("Error: A device cannot connect to itself.")
            return False
        if self.adjacency_matrix[index1][index2] == 1:
            print("Error: Devices are already connected.")
            return False

        if self.enforce_port_capacity:
            if self.count_used_ports(index1) >= self.devices[index1].port_capacity:
                print("Error: First device has no available ports.")
                return False
            if self.count_used_ports(index2) >= self.devices[index2].port_capacity:
                print("Error: Second device has no available ports.")
                return False

        self.adjacency_matrix[index1][index2] = 1
        self.adjacency_matrix[index2][index1] = 1
        print(f"Devices {device_id1} and {device_id2} connected.")
        return True

    def disconnect_devices(self, device_id1, device_id2):
        """Disconnect two device IDs. Time O(V); space O(1)."""
        index1 = self.find_device_index(device_id1)
        index2 = self.find_device_index(device_id2)
        if index1 == -1 or index2 == -1:
            print("Error: One or both devices not found.")
            return False
        if index1 == index2:
            print("Error: Self-links are not allowed.")
            return False
        if self.adjacency_matrix[index1][index2] == 0:
            print("Error: Devices are not connected.")
            return False

        self.adjacency_matrix[index1][index2] = 0
        self.adjacency_matrix[index2][index1] = 0
        print(f"Devices {device_id1} and {device_id2} disconnected.")
        return True

    def is_directly_connected(self, device_id1, device_id2):
        """Check if two IDs share a link. Time O(V); space O(1)."""
        index1 = self.find_device_index(device_id1)
        index2 = self.find_device_index(device_id2)
        if index1 == -1 or index2 == -1:
            return False
        return self.adjacency_matrix[index1][index2] == 1

    def display_graph(self):
        """Print devices and links. Time O(V²); space O(1)."""
        print("\n========== NETWORK GRAPH ==========")
        print("\nDevices:")
        for i in range(self.device_count):
            device = self.devices[i]
            print(
                f"[{i}] ID: {device.device_id} | Hostname: {device.hostname} | "
                f"Type: {device.device_type} | Ports: {device.port_capacity}"
            )
        if self.device_count == 0:
            print("No devices in the network.")
            return

        print("\nAdjacency Matrix (indexes):")
        print("     ", end="")
        for i in range(self.device_count):
            print(f"{i:3}", end="")
        print()
        for i in range(self.device_count):
            print(f"{i:3} |", end="")
            for j in range(self.device_count):
                print(f"{self.adjacency_matrix[i][j]:3}", end="")
            print()

        print("\nAdjacency List (device IDs):")
        for i in range(self.device_count):
            print(f"{self.devices[i].device_id}: ", end="")
            has_neighbor = False
            for j in range(self.device_count):
                if self.adjacency_matrix[i][j] == 1:
                    print(self.devices[j].device_id, end=" ")
                    has_neighbor = True
            if not has_neighbor:
                print("(none)", end="")
            print()
        print("===================================")

    def bfs(self, start_device_id, include_disconnected=False):
        """Return BFS order. Time O(V²); auxiliary space O(V)."""
        return bfs_traversal(self, start_device_id, include_disconnected)

    def dfs(self, start_device_id, include_disconnected=False):
        """Return DFS order. Time O(V²); auxiliary space O(V)."""
        return dfs_traversal(self, start_device_id, include_disconnected)

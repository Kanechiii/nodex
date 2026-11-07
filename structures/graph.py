
class NetworkGraph:
    def __init__(self, enforce_port_capacity=True):
        self.max_devices = 10
        self.device_count = 0
        self.enforce_port_capacity = enforce_port_capacity

        # Fixed-size device array
        self.devices = [None] * self.max_devices

        # Manually created 10x10 adjacency matrix
        self.adjacency_matrix = []

        for i in range(self.max_devices):
            row = [0] * self.max_devices
            self.adjacency_matrix.append(row)

  
    # SEARCH DEVICE INDEX BY ID
    def find_device_index(self, device_id):
        for i in range(self.device_count):
            if self.devices[i].device_id == device_id:
                return i

        return -1

  
    # SEARCH DEVICE BY ID 
    def search_device(self, device_id):
        index = self.find_device_index(device_id)

        if index == -1:
            return None

        return self.devices[index]

    # GET DEVICE COUNT 
    def get_device_count(self):
        return self.device_count

    # ADD DEVICE
    def add_device(self, device):
        if self.find_device_index(device.device_id) != -1:
            print("Error: Duplicate device ID.")
            return False

        if self.device_count >= self.max_devices:
            print("Error: Network is full. Maximum 10 devices.")
            return False

        if not isinstance(device.port_capacity, int) or device.port_capacity < 0:
            print("Error: Port capacity must be a non-negative integer.")
            return False

        self.devices[self.device_count] = device
        self.device_count += 1

        print(f"Device {device.hostname} added successfully.")
        return True


    # REMOVE DEVICE
    def remove_device(self, device_id):
        index = self.find_device_index(device_id)

        if index == -1:
            print("Error: Device not found.")
            return False

        last = self.device_count - 1

        # Shift device array to the left
        for i in range(index, last):
            self.devices[i] = self.devices[i + 1]

        self.devices[last] = None

        # Shift adjacency matrix rows upward
        for i in range(index, last):
            for j in range(self.device_count):
                self.adjacency_matrix[i][j] = (
                    self.adjacency_matrix[i + 1][j]
                )

        # Shift adjacency matrix columns left
        for j in range(index, last):
            for i in range(last):
                self.adjacency_matrix[i][j] = (
                    self.adjacency_matrix[i][j + 1]
                )

        # Clear the unused last row and column
        for i in range(self.max_devices):
            self.adjacency_matrix[last][i] = 0
            self.adjacency_matrix[i][last] = 0

        self.device_count -= 1

        print(f"Device {device_id} removed successfully.")
        return True

  
    # COUNT USED PORTS
    def count_used_ports(self, index):
        used_ports = 0

        for j in range(self.device_count):
            used_ports += self.adjacency_matrix[index][j]

        return used_ports
    
    # CONNECT DEVICEs
    def connect_devices(self, device_id1, device_id2):
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
            device1 = self.devices[index1]
            device2 = self.devices[index2]

            if self.count_used_ports(index1) >= device1.port_capacity:
                print("Error: First device has no available ports.")
                return False

            if self.count_used_ports(index2) >= device2.port_capacity:
                print("Error: Second device has no available ports.")
                return False

        # Undirected graph: both directions
        self.adjacency_matrix[index1][index2] = 1
        self.adjacency_matrix[index2][index1] = 1

        print(f"Devices {device_id1} and {device_id2} connected.")
        return True


    # DISCONNECT DEVICES
    def disconnect_devices(self, device_id1, device_id2):
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

    # CHECK DIRECT CONNECTION
    def is_directly_connected(self, device_id1, device_id2):
        index1 = self.find_device_index(device_id1)
        index2 = self.find_device_index(device_id2)

        if index1 == -1 or index2 == -1:
            return False

        return self.adjacency_matrix[index1][index2] == 1


    # DISPLAY GRAPH
    def display_graph(self):
        print("\n========== NETWORK GRAPH ==========")

        print("\nDevices:")
        for i in range(self.device_count):
            device = self.devices[i]

            print(
                f"[{i}] ID: {device.device_id} | "
                f"Hostname: {device.hostname} | "
                f"Type: {device.device_type} | "
                f"Ports: {device.port_capacity}"
            )

        if self.device_count == 0:
            print("No devices in the network.")
            return

        print("\nAdjacency Matrix:")
        print("     ", end="")

        for i in range(self.device_count):
            print(f"{i:3}", end="")
        print()

        for i in range(self.device_count):
            print(f"{i:3} |", end="")

            for j in range(self.device_count):
                print(f"{self.adjacency_matrix[i][j]:3}", end="")

            print()

        print("\nAdjacency List (Device IDs):")

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


class Device:
    def __init__(self, device_id, hostname, device_type, port_capacity):
        self.device_id = device_id
        self.hostname = hostname
        self.device_type = device_type
        self.port_capacity = port_capacity

    def display_info(self):
        print(f"Device ID: {self.device_id}")
        print(f"Hostname: {self.hostname}")
        print(f"Device Type: {self.device_type}")
        print(f"Port Capacity: {self.port_capacity}")

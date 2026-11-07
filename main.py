
from models.device import Device
from structures.graph import NetworkGraph

network = NetworkGraph()

# Create devices
router = Device(1, "Router-1", "Router", 4)
switch = Device(2, "Switch-1", "Switch", 8)
pc = Device(3, "PC-1", "Computer", 2)
server = Device(4, "Server-1", "Server", 4)

# Add devices
network.add_device(router)
network.add_device(switch)
network.add_device(pc)
network.add_device(server)

# Test duplicate ID
network.add_device(Device(1, "Router-2", "Router", 4))

# Connect devices
network.connect_devices(1, 2)
network.connect_devices(2, 3)
network.connect_devices(3, 4)

# Test duplicate connection and self-link
network.connect_devices(1, 2)
network.connect_devices(1, 1)

# Display graph before removal
network.display_graph()

# Search for a device
found = network.search_device(3)

if found is not None:
    found.display_info()
else:
    print("Device not found.")

# Check device count
print("Device count:", network.get_device_count())

# Check direct connection
print("PC to Server:", network.is_directly_connected(3, 4))

# Remove middle device
network.remove_device(2)

# Display updated graph
network.display_graph()

# Disconnect remaining connection
network.disconnect_devices(3, 4)

network.display_graph()

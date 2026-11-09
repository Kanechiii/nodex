from models.device import Device
from structures.graph import NetworkGraph

GROUP_NAME = "Nodex Project Team"
OPERATIONS = (
    ("Add device", "O(V)", "O(1)"),
    ("Remove device", "O(V²)", "O(1)"),
    ("Connect devices", "O(V)", "O(1)"),
    ("Disconnect devices", "O(V)", "O(1)"),
    ("Search device", "O(V)", "O(1)"),
    ("Display network topology", "O(V²)", "O(1)"),
    ("Breadth-first search (BFS)", "O(V²)", "O(V)"),
    ("Depth-first search (DFS)", "O(V²)", "O(V)"),
    ("Count devices", "O(1)", "O(1)"),
    ("Check direct link", "O(V)", "O(1)"),
)


def seed_network(graph):
    records = (
        (101, "Router-A", "Router", 3),
        (102, "Switch-B", "Switch", 3),
        (103, "PC-C", "Computer", 2),
        (104, "Server-D", "Server", 1),
        (105, "Printer-E", "Printer", 1),
    )
    for dev_id, name, kind, ports in records:
        graph.add_device(Device(dev_id, name, kind, ports))
    for first, second in ((101, 102), (101, 103), (102, 104)):
        graph.connect_devices(first, second)


def read_integer(prompt, minimum=0):
    while True:
        raw = input(prompt).strip()
        try:
            number = int(raw)
        except ValueError:
            print("Invalid input: enter a whole number.")
            continue
        if number < minimum:
            print(f"Invalid input: enter an integer of at least {minimum}.")
            continue
        return number


def read_text(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Invalid input: this field cannot be blank.")


def read_yes_no(prompt):
    while True:
        answer = input(prompt).strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("Invalid input: enter Y or N.")


def show_menu(graph):
    print("\n" + "=" * 49)
    print(" NODEX | NETWORK CONNECTIVITY SIMULATOR")
    print(f" Group: {GROUP_NAME}")
    print(f" Devices: {graph.get_device_count()}/{graph.max_devices}")
    print("=" * 49)
    for index, (label, _, _) in enumerate(OPERATIONS, start=1):
        print(f" {index:2}. {label}")
    print("  0. Exit")
    print("=" * 49)


def show_complexity(choice):
    _, time_cost, space_cost = OPERATIONS[choice - 1]
    print(f"Complexity: time {time_cost} | auxiliary space {space_cost}")


def do_operation(graph, choice):
    if choice == 1:
        if graph.get_device_count() == graph.max_devices:
            print("Network is full: remove a device before adding another.")
            return
        dev_id = read_integer("Device ID (0 or greater): ")
        if graph.search_device(dev_id) is not None:
            print("Error: Duplicate device ID.")
            return
        name = read_text("Hostname: ")
        kind = read_text("Device type: ")
        ports = read_integer("Port capacity (0 or greater): ")
        graph.add_device(Device(dev_id, name, kind, ports))
    elif choice == 2:
        graph.remove_device(read_integer("Device ID to remove: "))
    elif choice in (3, 4, 10):
        first = read_integer("First device ID: ")
        second = read_integer("Second device ID: ")
        if choice == 3:
            graph.connect_devices(first, second)
        elif choice == 4:
            graph.disconnect_devices(first, second)
        elif graph.search_device(first) is None or graph.search_device(second) is None:
            print("Error: One or both devices not found.")
        elif first == second:
            print("No direct link: a device cannot link to itself.")
        elif graph.is_directly_connected(first, second):
            print(f"Direct link exists between {first} and {second}.")
        else:
            print(f"No direct link between {first} and {second}.")
    elif choice == 5:
        dev_id = read_integer("Device ID to search: ")
        device = graph.search_device(dev_id)
        if device is None:
            print(f"Device {dev_id} not found.")
        else:
            print("Device found:")
            device.display_info()
    elif choice == 6:
        graph.display_graph()
    elif choice in (7, 8):
        if graph.get_device_count() == 0:
            print("Network is empty: no devices to traverse.")
            return
        start = read_integer("Starting device ID: ")
        include_all = read_yes_no("Include disconnected components? [Y/N]: ")
        try:
            order = graph.bfs(start, include_all) if choice == 7 else graph.dfs(start, include_all)
        except ValueError as error:
            print(f"Traversal error: {error}")
            return
        method = "BFS" if choice == 7 else "DFS"
        print(f"{method} visit order (device IDs): " + " -> ".join(str(item) for item in order))
    elif choice == 9:
        print(f"Active devices: {graph.get_device_count()} / {graph.max_devices}")


def main():
    graph = NetworkGraph(enforce_port_capacity=True)
    print("Starting Nodex with five sample network devices...")
    seed_network(graph)
    try:
        while True:
            show_menu(graph)
            raw = input("Choose an option (0-10): ").strip()
            try:
                choice = int(raw)
            except ValueError:
                print("Invalid menu selection: enter a number from 0 to 10.")
                continue
            if choice == 0:
                print("Exiting Nodex. Goodbye!")
                break
            if choice < 0 or choice > len(OPERATIONS):
                print("Invalid menu selection: enter a number from 0 to 10.")
                continue
            try:
                do_operation(graph, choice)
            finally:
                show_complexity(choice)
    except (EOFError, KeyboardInterrupt):
        print("\nExiting Nodex. Goodbye!")


if __name__ == "__main__":
    main()

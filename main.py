from models.device import Device
from structures.graph import NetworkGraph
import console_ui

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


class BackToMenu(Exception):
    """User canceled the current operation before it could finish."""


def check_back(value):
    if value.lower() in ("b", "back"):
        raise BackToMenu


def read_integer(prompt, minimum=0):
    while True:
        raw = input(prompt).strip()
        check_back(raw)
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
        check_back(value)
        if value:
            return value
        print("Invalid input: this field cannot be blank.")


def read_yes_no(prompt):
    while True:
        answer = input(prompt).strip().lower()
        check_back(answer)
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no"):
            return False
        print("Invalid input: enter Y or N.")


def read_existing_device_id(graph, prompt):
    """Retry a mistyped device ID without restarting the current operation."""
    while True:
        dev_id = read_integer(prompt)
        if graph.search_device(dev_id) is not None:
            return dev_id
        print("Error: Device not found. Try again or enter B to go back.")


def show_menu(graph):
    console_ui.show_menu(graph, OPERATIONS, GROUP_NAME)


def show_complexity(choice):
    _, time_cost, space_cost = OPERATIONS[choice - 1]
    print(f"Complexity: time {time_cost} | auxiliary space {space_cost}")


def do_operation(graph, choice):
    """Run an operation; return False if the user backs out."""
    console_ui.show_operation(choice, OPERATIONS)
    try:
        _perform_operation(graph, choice)
    except BackToMenu:
        print("Operation canceled. Returning to the main menu.")
        return False
    return True


def _perform_operation(graph, choice):
    if choice == 1:
        if graph.get_device_count() == graph.max_devices:
            print("Network is full: remove a device before adding another.")
            return
        while True:
            dev_id = read_integer("Device ID (0 or greater): ")
            if graph.search_device(dev_id) is None:
                break
            print("Error: Duplicate device ID. Try another ID or enter B to go back.")
        name = read_text("Hostname: ")
        kind = read_text("Device type: ")
        ports = read_integer("Port capacity (0 or greater): ")
        graph.add_device(Device(dev_id, name, kind, ports))
    elif choice == 2:
        graph.remove_device(read_existing_device_id(graph, "Device ID to remove: "))
    elif choice in (3, 4, 10):
        first = read_existing_device_id(graph, "First device ID: ")
        second = read_existing_device_id(graph, "Second device ID: ")
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
        start = read_existing_device_id(graph, "Starting device ID: ")
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
    console_ui.show_splash()
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
                completed = do_operation(graph, choice)
            except (EOFError, KeyboardInterrupt):
                raise
            else:
                if completed:
                    show_complexity(choice)
    except (EOFError, KeyboardInterrupt):
        print("\nExiting Nodex. Goodbye!")


if __name__ == "__main__":
    main()

"""Presentation-only terminal interface for Nodex.

No graph mutations or input validation occur in this module.
Animation and ANSI colors are disabled automatically for redirected output.
"""
import os
import sys
import time

WIDTH = 66
RESET = "\x1b[0m"
CYAN = "\x1b[36m"
BLUE = "\x1b[94m"
DIM = "\x1b[2m"
BOLD = "\x1b[1m"

def _interactive():
    return bool(getattr(sys.stdout, "isatty", lambda: False)()) and not os.environ.get("NO_COLOR") and os.environ.get("TERM", "") != "dumb"

def _paint(value, style):
    return style + value + RESET if _interactive() else value

def _line():
    print(_paint("  " + "-" * WIDTH, DIM))

def show_splash():
    """Display a short moving network motif once; never animate redirected output."""
    logo = "NODEX"
    if _interactive() and not os.environ.get("NODEX_NO_ANIMATION"):
        frames = ("o-----o  o", "o--o--o  o", "o--o--o--o", "o--o==o--o")
        for frame in frames:
            sys.stdout.write("\r  " + _paint(frame + "  " + logo, CYAN + BOLD) + "  ")
            sys.stdout.flush()
            time.sleep(0.09)
        sys.stdout.write("\r" + " " * (len(frames[-1]) + len(logo) + 6) + "\r")
        sys.stdout.flush()
    print()
    print(_paint("  o----o----o   NODEX", CYAN + BOLD))
    print(_paint("       |        Network Connectivity Simulator", DIM))
    print(_paint("       o", CYAN))

def show_menu(graph, operations, group_name):
    """Render all original menu numbers with compact, grouped navigation."""
    count = graph.get_device_count()
    print()
    _line()
    print("  " + _paint("NODEX", CYAN + BOLD) + "  /  NETWORK CONNECTIVITY SIMULATOR")
    print("  " + _paint(group_name, DIM))
    print("  " + _paint("DEVICES", BLUE + BOLD) + f"  {count}/{graph.max_devices}  " + _paint("[" + "#" * count + "." * (graph.max_devices - count) + "]", CYAN))
    _line()
    groups = (("DEVICE MANAGEMENT", 1, 2), ("NETWORK CONNECTIONS", 3, 4), ("INSPECT NETWORK", 5, 6), ("GRAPH TRAVERSAL", 7, 8), ("NETWORK UTILITIES", 9, 10))
    for heading, first, last in groups:
        print("  " + _paint(heading, BLUE + BOLD))
        for index in range(first, last + 1):
            print(f"  {index:2}. {operations[index - 1][0]}")
        print()
    print("   0. Exit")
    _line()
    print("  " + _paint("TIP", CYAN + BOLD) + "  Enter B (Back) at any operation prompt to return to this menu.")
    _line()

def show_operation(choice, operations):
    """Operation context; not a second input step."""
    print()
    _line()
    print("  " + _paint(f"{choice:02d} / {operations[choice - 1][0].upper()}", CYAN + BOLD))
    print("  " + _paint("Enter B to return to the main menu.", DIM))
    _line()

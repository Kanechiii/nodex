"""Presentation-only terminal UI for Nodex.

The logo recreates the four SVG nodes and six edges from assets/nodex-banner.svg.
Only terminal output is affected; there are no graph or input-handling changes.
"""
import math
import os
import sys
import time

WIDTH = 66
RESET = "\x1b[0m"
CYAN = "\x1b[36m"
BLUE = "\x1b[94m"
DIM = "\x1b[2m"
BOLD = "\x1b[1m"

# Exact center coordinates and connections from assets/nodex-banner.svg.
_LOGO_POINTS = ((858, 140), (953, 81), (1053, 137), (955, 204))
_LOGO_EDGES = ((0, 1), (1, 2), (2, 3), (3, 0), (1, 3), (0, 2))
_BRAILLE_DOTS = ((0x01, 0x02, 0x04, 0x40), (0x08, 0x10, 0x20, 0x80))
_SPIN_ANGLES = tuple(range(0, 360, 24)) + (360,)


def _interactive():
    return (
        bool(getattr(sys.stdout, "isatty", lambda: False)())
        and not os.environ.get("NO_COLOR")
        and os.environ.get("TERM", "") != "dumb"
    )


def _supports_braille():
    try:
        "⣿".encode(getattr(sys.stdout, "encoding", None) or "utf-8")
    except (UnicodeError, LookupError):
        return False
    return True


def _paint(value, style):
    return style + value + RESET if _interactive() else value


def _line():
    print(_paint("  " + "-" * WIDTH, DIM))


def _distance_to_line(x, y, first, second):
    ax, ay = first
    bx, by = second
    dx, dy = bx - ax, by - ay
    extent = dx * dx + dy * dy
    step = max(0.0, min(1.0, ((x - ax) * dx + (y - ay) * dy) / extent))
    return math.hypot(x - (ax + step * dx), y - (ay + step * dy))


def _logo_frame(degrees=0, columns=18, rows=9):
    """Rasterize the original SVG geometry into a terminal Braille dot grid."""
    width, height = columns * 2, rows * 4
    center_x, center_y = (width - 1) / 2, (height - 1) / 2
    scale = (min(width, height) - 5) / 230.0
    turn = math.radians(degrees)
    sine, cosine = math.sin(turn), math.cos(turn)
    nodes = []
    for x, y in _LOGO_POINTS:
        dx, dy = (x - 955) * scale, (y - 142) * scale
        nodes.append((center_x + dx * cosine - dy * sine,
                      center_y + dx * sine + dy * cosine))
    edges = tuple((nodes[first], nodes[second]) for first, second in _LOGO_EDGES)
    radius = 17 * scale  # Same circle radius as the README SVG.
    pixels = [[False] * width for _ in range(height)]
    for y in range(height):
        for x in range(width):
            sx, sy = x + 0.5, y + 0.5
            marked = any(_distance_to_line(sx, sy, a, b) <= 0.58 for a, b in edges)
            for nx, ny in nodes:
                distance = math.hypot(sx - nx, sy - ny)
                if distance < radius - 0.72:
                    marked = False  # The SVG node's dark center hides edge lines.
                if abs(distance - radius) <= 0.72:
                    marked = True
            pixels[y][x] = marked
    result = []
    for row in range(rows):
        text = []
        for col in range(columns):
            bits = 0
            for dx in range(2):
                for dy in range(4):
                    if pixels[row * 4 + dy][col * 2 + dx]:
                        bits |= _BRAILLE_DOTS[dx][dy]
            text.append(chr(0x2800 + bits))
        result.append("".join(text))
    return tuple(result)


def _display_logo(angle=0, columns=18, rows=9):
    if _supports_braille():
        return _logo_frame(angle, columns, rows)
    # ASCII-only fallback for terminals with no Unicode encoding.
    if rows == 5:
        return ("    O    ", "  / | \\  ", " O--+--O ", "  \\ | /  ", "    O    ")
    return (
        "        O         ",
        "       /|\\        ",
        "      / | \\       ",
        "     /  |  \\      ",
        "    O---+---O     ",
        "     \\  |  /      ",
        "      \\ | /       ",
        "       \\|/        ",
        "        O         ",
    )


def _banner_lines(angle=0):
    logo = _display_logo(angle)
    heading = ("", "", "Nodex", "", "NETWORK CONNECTIVITY SIMULATOR", "", "", "", "")
    lines = []
    for idx, mark in enumerate(logo):
        text = heading[idx].ljust(35)
        if idx == 2:
            text = _paint(text, BOLD)
        lines.append("  " + text + "  " + mark)
    return tuple(lines)


def show_splash():
    """Rotate the README's connected-node mark once; keep wordmark fixed."""
    if not (_interactive() and _supports_braille() and not os.environ.get("NODEX_NO_ANIMATION")):
        print("\n".join(_banner_lines()))
        return
    sys.stdout.write("\x1b[?25l")  # Hide the cursor only while animating.
    try:
        for frame_index, angle in enumerate(_SPIN_ANGLES):
            sys.stdout.write("\r" + "\n".join(_banner_lines(angle)) + "\n")
            sys.stdout.flush()
            if frame_index < len(_SPIN_ANGLES) - 1:
                time.sleep(0.055)
                sys.stdout.write(f"\x1b[{9}A")  # Redraw the same nine lines.
    finally:
        sys.stdout.write("\x1b[?25h")
        sys.stdout.flush()


def show_menu(graph, operations, group_name):
    """Keep all original menu numbers with a small static README logo."""
    count = graph.get_device_count()
    print()
    _line()
    mini = _display_logo(columns=9, rows=5)
    header = (
        "NODEX  /  NETWORK CONNECTIVITY SIMULATOR",
        group_name,
        f"DEVICES  {count}/{graph.max_devices}  [" + "#" * count + "." * (graph.max_devices - count) + "]",
        "",
        "",
    )
    for index, (text, symbol) in enumerate(zip(header, mini)):
        style = CYAN + BOLD if index == 0 else BLUE if index == 2 else DIM
        print("  " + _paint(text.ljust(47), style) + " " + symbol)
    _line()
    groups = (("DEVICE MANAGEMENT", 1, 2), ("NETWORK CONNECTIONS", 3, 4),
              ("INSPECT NETWORK", 5, 6), ("GRAPH TRAVERSAL", 7, 8),
              ("NETWORK UTILITIES", 9, 10))
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

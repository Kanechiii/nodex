<div align="center">
  <img src="assets/nodex-banner.svg" width="100%" alt="Nodex: a visual network of connected devices with BFS and DFS graph traversal" />

  <h1>Nodex</h1>
  <p>An offline Python console simulator for device connectivity, breadth-first search (BFS), and depth-first search (DFS).</p>

  <p>
    <a href="https://github.com/Kanechiii/nodex/actions/workflows/security.yml"><img alt="Python tests and security checks" src="https://github.com/Kanechiii/nodex/actions/workflows/security.yml/badge.svg" /></a>
    <a href="https://github.com/Kanechiii/nodex/releases"><img alt="Latest release" src="https://img.shields.io/github/v/release/Kanechiii/nodex?label=release" /></a>
    <a href="LICENSE"><img alt="MIT License" src="https://img.shields.io/badge/license-MIT-blue.svg" /></a>
    <img alt="Python 3.11 or newer" src="https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&amp;logoColor=white" />
  </p>
</div>

## Quick start

**Requirements:** Python 3.11 or newer. No third-party dependencies.

**Windows (VS Code / PowerShell)**

```powershell
git clone https://github.com/Kanechiii/nodex.git
cd nodex
py main.py
```

<details>
<summary><strong>macOS / Linux commands</strong></summary>

```bash
git clone https://github.com/Kanechiii/nodex.git
cd nodex
python3 main.py
```

</details>

The console starts with **five sample devices** and three links. Select a number from **1–10** to perform an operation; enter **0** to exit. All changes are in memory and reset on restart.

## Application workflow

Nodex repeats the same cycle until you select **0 — Exit**. The console handles input and messages, while `NetworkGraph` manages devices and the adjacency matrix. Every valid menu operation finishes by displaying its time and auxiliary-space complexity.

```mermaid
flowchart TD
    Start["Launch Nodex"] --> Seed["Create graph and seed 5 sample devices"]
    Seed --> Menu["Display menu (0–10)"]
    Menu --> Choice{"Select an option"}
    Choice -->|0| Exit["Exit"]
    Choice -->|1–6, 9–10| Graph["Validate input and run graph operation"]
    Choice -->|7–8| Traverse["Validate start and run BFS or DFS"]
    Choice -->|Invalid| Retry["Show input error"]
    Graph --> Result["Show result and complexity"]
    Traverse --> Result
    Result --> Menu
    Retry --> Menu
```

For detailed decision points and diagrams, see **[workflows for all 10 menu operations](docs/WORKFLOWS.md)**.

## How it works

<details open>
<summary><strong>Architecture and sample network</strong> — click to collapse</summary>

### Architecture

```mermaid
flowchart TD
    A["Console user"] --> B["main.py · Menu and validation"]
    B --> C["NetworkGraph · Graph operations"]
    C --> D["Device records"]
    C --> E["10 × 10 adjacency matrix"]
    C --> F["BFS · Manual indexed queue"]
    C --> G["DFS · Recursive traversal"]
```

Every device is a **vertex**; each bidirectional link is an **edge**. The matrix stores **1** for a direct connection and **0** otherwise. No graph library, built-in queue class, or visited set is used.

### Default network

```mermaid
flowchart LR
    A["101 · Router-A"] --- B["102 · Switch-B"]
    A --- C["103 · PC-C"]
    B --- D["104 · Server-D"]
    E["105 · Printer-E<br/>(disconnected)"]
```

Starting at **101** without disconnected components:

| Traversal | Visit order |
| --- | --- |
| **BFS** | `101 → 102 → 103 → 104` |
| **DFS** | `101 → 102 → 104 → 103` |

Enable **Include disconnected components** to visit the isolated printer, too.

</details>

## Menu operation workflows

<details>
<summary><strong>Expand all menu actions (1–10)</strong></summary>

Each item describes the live console behavior. Errors are reported without changing the graph, and the menu returns after the attempt.

**1. Add device** — Check the 10-device limit → read a unique non-negative ID, hostname, type, and non-negative port capacity → create and insert the device. Reject duplicates or a full graph. [View flowchart](docs/WORKFLOWS.md#1-add-device).

**2. Remove device** — Read a non-negative ID → locate the device → remove its record and links → compact matrix rows/columns → clear unused slots. Report if missing. [View flowchart](docs/WORKFLOWS.md#2-remove-device).

**3. Connect devices** — Read two IDs → verify both exist, are distinct and not already linked → check both port capacities → set symmetric matrix entries to 1. [View flowchart](docs/WORKFLOWS.md#3-connect-devices).

**4. Disconnect devices** — Read two IDs → verify both exist and are distinct → check the link is present → clear both matrix entries to 0. [View flowchart](docs/WORKFLOWS.md#4-disconnect-devices).

**5. Search device** — Read an ID → find its current array index → display the ID, hostname, type and port capacity, or report not found. [View flowchart](docs/WORKFLOWS.md#5-search-device).

**6. Display network topology** — List active device records → print the indexed adjacency matrix → list each device's neighboring IDs. Show an empty-network message if needed. [View flowchart](docs/WORKFLOWS.md#6-display-network-topology).

**7. Breadth-first search (BFS)** — Check for an empty graph → read a start ID and disconnected-components choice → validate start → visit level by level with an indexed queue and visited array → print IDs. [View flowchart](docs/WORKFLOWS.md#7-breadth-first-search-bfs).

**8. Depth-first search (DFS)** — Check for an empty graph → read a start ID and disconnected-components choice → validate start → recursively visit neighbors with a visited array → print IDs. [View flowchart](docs/WORKFLOWS.md#8-depth-first-search-dfs).

**9. Count devices** — Read the graph's active device counter → display the number in use out of 10. [View flowchart](docs/WORKFLOWS.md#9-count-devices).

**10. Check direct link** — Read two IDs → reject missing devices and self-links → inspect the corresponding matrix entry → report whether a direct link exists. [View flowchart](docs/WORKFLOWS.md#10-check-direct-link).

</details>

## Console features

<details>
<summary><strong>View all 10 operations</strong></summary>

| # | Operation | # | Operation |
| --- | --- | --- | --- |
| 1 | Add device | 6 | Display network topology |
| 2 | Remove device | 7 | Breadth-first search (BFS) |
| 3 | Connect devices | 8 | Depth-first search (DFS) |
| 4 | Disconnect devices | 9 | Count devices |
| 5 | Search device | 10 | Check direct link |

Nodex validates input, rejects duplicate device IDs and self-links, checks available ports, and displays time and auxiliary-space complexity after each operation.

</details>

<details>
<summary><strong>Algorithms and complexity</strong></summary>

For **V** active devices (up to 10):

| Operation | Time | Auxiliary space |
| --- | --- | --- |
| Count devices | O(1) | O(1) |
| Add, search, connect, disconnect, direct-link check | O(V) | O(1) |
| Remove device, display topology | O(V²) | O(1) |
| BFS, DFS | O(V²) | O(V) |

BFS uses an indexed array queue; DFS uses recursion. Both use visited arrays and traverse neighbors by ascending index. The graph's fixed 10 × 10 matrix requires O(10²) storage.

</details>

<details>
<summary><strong>Source-code layout</strong></summary>

```text
nodex/
├── main.py                    Console menu and input validation
├── models/device.py           Device record
├── structures/graph.py        Undirected adjacency matrix
├── algorithms/bfs.py          BFS with manually indexed queue
├── algorithms/dfs.py          Recursive DFS
├── tests/                     Console, graph, traversal, security tests
├── scripts/                   Security and history audit tools
├── SECURITY.md                Responsible disclosure policy
└── DEFENSE_NOTES.md           Algorithm explanations
```

</details>

## Tests and security

<details>
<summary><strong>Run tests and security checks</strong></summary>

From the repository root, on Windows:

```powershell
py -m unittest discover -s tests -p "test_*.py" -v
py -m unittest discover -s tests -p "*_check.py" -v
```

For the security and Git history audits, use a **full Git clone**:

```powershell
py scripts/security_audit.py
py scripts/history_privacy_audit.py
```

On macOS/Linux, replace `py` with `python3`. GitHub Actions checks Python 3.11 and 3.13, unit tests, source code, and reachable Git history. See the [security policy](SECURITY.md) for responsible reporting.

</details>

## Contributing

Contributions are welcome—especially improvements to graph operations, learning features, accessibility, and automated testing. Please open an issue to discuss larger changes before implementing them, then submit a focused pull request.

Start with the **[contribution guide](CONTRIBUTING.md)** for the development workflow, test commands, and suggested enhancements. Preserve the educational purpose: keep the console usable offline and explain any new data structures or algorithms.

## License and contributors

Released under the **[MIT License](LICENSE)**. Copyright © 2026 **[Kenneth Gabriel Alido](https://github.com/Kanechiii)** and **[Mark Ryan Songalia](https://github.com/gyryan)**.

## Disclaimer

Nodex is an **educational graph-based network simulator**, not a real network management, monitoring, security scanning, or device configuration tool. Its connections and device records are simulated in memory, and all changes reset when the program closes. It does not emulate packet forwarding, routing protocols, VLANs, STP, or physical network behavior, and it is **not a replacement for Cisco Packet Tracer**. Use it to learn fundamental graph concepts, not to make decisions about operational networks.


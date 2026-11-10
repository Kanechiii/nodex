# Nodex — Menu Workflows

This guide follows the **actual Python console implementation** in [`main.py`](../main.py) and [`NetworkGraph`](../structures/graph.py). Nodex uses a **fixed-capacity, undirected 10-device adjacency matrix**, a manually indexed BFS queue and recursive DFS.

## Overall flow

```mermaid
flowchart TD
    A["Start main.py"] --> B["Initialize NetworkGraph"]
    B --> C["Seed 5 example devices and 3 connections"]
    C --> D["Display 0–10 menu"]
    D --> E{"Menu input"}
    E -->|"0"| X["Exit"]
    E -->|"Invalid"| W["Explain error and ask again"]
    E -->|"1–10"| F["Validate required input"]
    F --> G["Run selected operation"]
    G --> H["Display outcome and complexity"]
    H --> D
    W --> D
```

**Input rules:** The console retries invalid numbers and blank text fields. Device IDs and port counts must be non-negative integers. Unless an operation is skipped at the menu (e.g., invalid menu choice), it displays its time and auxiliary-space complexity after the attempt.

Each expandable section contains the operation's inputs, implementation flow, expected outcome, and validation paths.

### 1. Add device

<details>
<summary><strong>View decision-flow diagram</strong></summary>

**Inputs:** Device ID, hostname, device type, port capacity.

```mermaid
flowchart TD
    A["Choose 1"] --> B{"10 devices already present?"}
    B -->|"Yes"| X["Show network-full error"]
    B -->|"No"| C["Read non-negative device ID"]
    C --> D{"ID already exists?"}
    D -->|"Yes"| Y["Show duplicate-ID error"]
    D -->|"No"| E["Read nonblank hostname and type"]
    E --> F["Read non-negative port capacity"]
    F --> G["Create Device record"]
    G --> H["Append device to graph's next free slot"]
    H --> I["Show success"]
```

The graph stores the device in an active slot, preserving its unique ID. **Time O(V), auxiliary space O(1)**.

</details>

### 2. Remove device

<details>
<summary><strong>View decision-flow diagram</strong></summary>

**Input:** Device ID to remove.

```mermaid
flowchart TD
    A["Choose 2"] --> B["Read non-negative device ID"]
    B --> C["Find device index"]
    C --> D{"Device found?"}
    D -->|"No"| X["Show not-found error"]
    D -->|"Yes"| E["Shift remaining device records left"]
    E --> F["Compact adjacency-matrix rows"]
    F --> G["Compact adjacency-matrix columns"]
    G --> H["Clear unused final row and column"]
    H --> I["Decrease count and show success"]
```

Removal also removes all links to the deleted device while preserving the other devices' IDs and connections. **Time O(V²), auxiliary space O(1)**.

</details>

### 3. Connect devices

<details>
<summary><strong>View decision-flow diagram</strong></summary>

**Inputs:** Two device IDs.

```mermaid
flowchart TD
    A["Choose 3"] --> B["Read two non-negative IDs"]
    B --> C{"Both IDs exist?"}
    C -->|"No"| X["Show missing-device error"]
    C -->|"Yes"| D{"Two different devices?"}
    D -->|"No"| Y["Reject self-link"]
    D -->|"Yes"| E{"Connection already exists?"}
    E -->|"Yes"| Z["Reject duplicate link"]
    E -->|"No"| F{"Both have free ports?"}
    F -->|"No"| W["Show port-capacity error"]
    F -->|"Yes"| G["Set matrix i,j and j,i to 1"]
    G --> H["Confirm connection"]
```

Each connection uses one port on each endpoint; connections are bidirectional. **Time O(V), auxiliary space O(1)**.

</details>

### 4. Disconnect devices

<details>
<summary><strong>View decision-flow diagram</strong></summary>

**Inputs:** Two device IDs.

```mermaid
flowchart TD
    A["Choose 4"] --> B["Read two non-negative IDs"]
    B --> C{"Both IDs exist?"}
    C -->|"No"| X["Show missing-device error"]
    C -->|"Yes"| D{"IDs different?"}
    D -->|"No"| Y["Reject self-link"]
    D -->|"Yes"| E{"Link present?"}
    E -->|"No"| Z["Report not connected"]
    E -->|"Yes"| F["Set matrix i,j and j,i to 0"]
    F --> G["Confirm disconnection"]
```

The devices remain in the graph; only their direct edge is removed. **Time O(V), auxiliary space O(1)**.

</details>

### 5. Search device

<details>
<summary><strong>View decision-flow diagram</strong></summary>

**Input:** Device ID.

```mermaid
flowchart TD
    A["Choose 5"] --> B["Read non-negative device ID"]
    B --> C["Scan active records for matching ID"]
    C --> D{"Found?"}
    D -->|"No"| E["Show not-found message"]
    D -->|"Yes"| F["Display ID, hostname, type and port capacity"]
```

Search uses the device's **ID**, not its changing array index. **Time O(V), auxiliary space O(1)**.

</details>

### 6. Display network topology

<details>
<summary><strong>View decision-flow diagram</strong></summary>

**Input:** None.

```mermaid
flowchart TD
    A["Choose 6"] --> B["Print active device records"]
    B --> C{"Graph empty?"}
    C -->|"Yes"| D["Show empty-network message"]
    C -->|"No"| E["Print adjacency matrix by array index"]
    E --> F["Print adjacency list using device IDs"]
    F --> G["Finish topology display"]
```

A **1** at position `[i][j]` means the indexed devices share a direct link; a **0** means they do not. The adjacency list shows neighboring **device IDs**, which are easier for learners to follow. **Time O(V²), auxiliary space O(1)**.

</details>

### 7. Breadth-first search (BFS)

<details>
<summary><strong>View decision-flow diagram</strong></summary>

**Inputs:** Start device ID and whether to include disconnected components.

```mermaid
flowchart TD
    A["Choose 7"] --> B{"Graph empty?"}
    B -->|"Yes"| X["Explain no devices to traverse"]
    B -->|"No"| C["Read start ID and Y/N choice"]
    C --> D{"Start ID exists?"}
    D -->|"No"| Y["Display traversal error"]
    D -->|"Yes"| E["Create visited array and indexed queue"]
    E --> F["Enqueue start, mark visited"]
    F --> G["Dequeue next device and record its ID"]
    G --> H["Enqueue unvisited neighbors in ascending index order"]
    H --> I{"Any queue items left?"}
    I -->|"Yes"| G
    I -->|"No"| J{"Include disconnected components?"}
    J -->|"Yes"| K{"Unvisited device exists?"}
    K -->|"Yes"| L["Start BFS from next unvisited index"]
    L --> G
    K -->|"No"| M["Print traversal order"]
    J -->|"No"| M
```

BFS explores nearer neighbors before deeper levels. The queue is a fixed-size Python list managed using explicit front/rear indexes. **Time O(V²), auxiliary space O(V)**.

</details>

### 8. Depth-first search (DFS)

<details>
<summary><strong>View decision-flow diagram</strong></summary>

**Inputs:** Start device ID and whether to include disconnected components.

```mermaid
flowchart TD
    A["Choose 8"] --> B{"Graph empty?"}
    B -->|"Yes"| X["Explain no devices to traverse"]
    B -->|"No"| C["Read start ID and Y/N choice"]
    C --> D{"Start ID exists?"}
    D -->|"No"| Y["Display traversal error"]
    D -->|"Yes"| E["Create visited array"]
    E --> F["Visit start recursively"]
    F --> G["Mark visited and record device ID"]
    G --> H["Recursively explore each unvisited neighbor in ascending index order"]
    H --> I["Backtrack when no unvisited neighbors remain"]
    I --> J{"Include disconnected components?"}
    J -->|"Yes"| K{"Unvisited device exists?"}
    K -->|"Yes"| L["Run DFS from next unvisited index"]
    L --> G
    K -->|"No"| M["Print traversal order"]
    J -->|"No"| M
```

DFS follows each branch as far as possible before backtracking. It uses recursion and a visited array, not a built-in stack or visited set. **Time O(V²), auxiliary space O(V)**.

</details>

### 9. Count devices

<details>
<summary><strong>View decision-flow diagram</strong></summary>

**Input:** None.

```mermaid
flowchart LR
    A["Choose 9"] --> B["Read active device_count"]
    B --> C["Print active devices out of maximum 10"]
```

Nodex maintains this count as devices are added and removed, so no scan is needed. **Time O(1), auxiliary space O(1)**.

</details>

### 10. Check direct link

<details>
<summary><strong>View decision-flow diagram</strong></summary>

**Inputs:** Two device IDs.

```mermaid
flowchart TD
    A["Choose 10"] --> B["Read two non-negative IDs"]
    B --> C{"Both devices exist?"}
    C -->|"No"| X["Show missing-device error"]
    C -->|"Yes"| D{"Same ID?"}
    D -->|"Yes"| Y["Explain self-links are not allowed"]
    D -->|"No"| E["Find current indexes of both IDs"]
    E --> F{"Matrix entry equals 1?"}
    F -->|"Yes"| G["Report direct link exists"]
    F -->|"No"| H["Report no direct link"]
```

This checks a **single direct connection**, not whether two devices can reach one another through intermediate devices. Looking up IDs costs O(V), so **time O(V), auxiliary space O(1)**.

</details>

## Traversal example

The sample graph has links `101–102`, `101–103` and `102–104`; device `105` is isolated. With start ID `101`, both algorithms visit the connected component; enabling disconnected components also visits `105`. The exact order is deterministic because neighbors are examined by increasing array index.

[Back to the README](../README.md) · [Contributing](../CONTRIBUTING.md) · [Algorithm defense notes](../DEFENSE_NOTES.md)

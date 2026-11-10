# Nodex workflows

These diagrams document the **current console behavior** in [`main.py`](../main.py), [`graph.py`](../structures/graph.py), [`bfs.py`](../algorithms/bfs.py) and [`dfs.py`](../algorithms/dfs.py). Each menu operation is shown separately rather than combining steps.

**Shared input handling:** Numeric prompts repeat until a whole number at least 0 is entered. Text prompts repeat until nonblank. BFS/DFS's Y/N prompt repeats until a valid answer. For any selected operation 1–10, the console prints the operation's **time and auxiliary-space complexity** after completion or an application-level error. Only invalid menu selections and option 0 skip that line.

## Main loop

```mermaid
flowchart TD
    A["Start"] --> B["Create graph"]
    B --> C["Add 5 devices"]
    C --> D["Add 3 links"]
    D --> E["Show menu"]
    E --> F["Read choice"]
    F --> G{"0–10?"}
    G -->|"No"| H["Input error"]
    H --> E
    G -->|"Yes"| I{"Choice = 0?"}
    I -->|"Yes"| J["Exit"]
    I -->|"No"| K["Run option"]
    K --> L["Print result"]
    L --> M["Print cost"]
    M --> E
```

## 1. Add device

**Input:** ID, hostname, type, port capacity.

```mermaid
flowchart TD
    A["Choose 1"] --> B{"Count = 10?"}
    B -->|"Yes"| X["Full error"]
    B -->|"No"| C["Read ID"]
    C --> D{"ID valid?"}
    D -->|"No"| C
    D -->|"Yes"| E{"ID exists?"}
    E -->|"Yes"| Y["Duplicate error"]
    E -->|"No"| F["Read name"]
    F --> G{"Name blank?"}
    G -->|"Yes"| F
    G -->|"No"| H["Read type"]
    H --> I{"Type blank?"}
    I -->|"Yes"| H
    I -->|"No"| J["Read ports"]
    J --> K{"Ports valid?"}
    K -->|"No"| J
    K -->|"Yes"| L["Create record"]
    L --> M["Insert next slot"]
    M --> N["Count +1"]
    N --> O["Confirm"]
    X --> Z["Print cost"]
    Y --> Z
    O --> Z
```

The graph checks capacity and uniqueness before insertion. No adjacency-matrix edge is created automatically. **Time O(V), space O(1)**.

## 2. Remove device

**Input:** ID.

```mermaid
flowchart TD
    A["Choose 2"] --> B["Read ID"]
    B --> C{"ID valid?"}
    C -->|"No"| B
    C -->|"Yes"| D["Find index"]
    D --> E{"Found?"}
    E -->|"No"| X["Not found"]
    E -->|"Yes"| F["Shift records"]
    F --> G["Shift rows"]
    G --> H["Shift columns"]
    H --> I["Clear last row"]
    I --> J["Clear last col"]
    J --> K["Count -1"]
    K --> L["Confirm"]
    X --> Z["Print cost"]
    L --> Z
```

Removing a device deletes all of its links. Remaining records shift left; their IDs stay unchanged while their matrix indexes may change. **Time O(V²), space O(1)**.

## 3. Connect devices

**Input:** Two IDs.

```mermaid
flowchart TD
    A["Choose 3"] --> B["Read first ID"]
    B --> C{"Valid?"}
    C -->|"No"| B
    C -->|"Yes"| D["Read second ID"]
    D --> E{"Valid?"}
    E -->|"No"| D
    E -->|"Yes"| F["Find both"]
    F --> G{"Both found?"}
    G -->|"No"| X["Missing ID"]
    G -->|"Yes"| H{"Same device?"}
    H -->|"Yes"| Y["Self-link error"]
    H -->|"No"| I{"Already linked?"}
    I -->|"Yes"| J["Duplicate link"]
    I -->|"No"| K{"First port free?"}
    K -->|"No"| L["No free port"]
    K -->|"Yes"| M{"Second port free?"}
    M -->|"No"| L
    M -->|"Yes"| N["Set [i][j] = 1"]
    N --> O["Set [j][i] = 1"]
    O --> P["Confirm"]
    X --> Z["Print cost"]
    Y --> Z
    J --> Z
    L --> Z
    P --> Z
```

Each undirected link uses one port on each endpoint. The matrix is updated **symmetrically** only when all checks pass. **Time O(V), space O(1)**.

## 4. Disconnect devices

**Input:** Two IDs.

```mermaid
flowchart TD
    A["Choose 4"] --> B["Read first ID"]
    B --> C{"Valid?"}
    C -->|"No"| B
    C -->|"Yes"| D["Read second ID"]
    D --> E{"Valid?"}
    E -->|"No"| D
    E -->|"Yes"| F["Find both"]
    F --> G{"Both found?"}
    G -->|"No"| X["Missing ID"]
    G -->|"Yes"| H{"Same device?"}
    H -->|"Yes"| Y["Self-link error"]
    H -->|"No"| I{"Link exists?"}
    I -->|"No"| J["No link error"]
    I -->|"Yes"| K["Set [i][j] = 0"]
    K --> L["Set [j][i] = 0"]
    L --> M["Confirm"]
    X --> Z["Print cost"]
    Y --> Z
    J --> Z
    M --> Z
```

Only the edge is removed; both device records remain. **Time O(V), space O(1)**.

## 5. Search device

**Input:** ID.

```mermaid
flowchart TD
    A["Choose 5"] --> B["Read ID"]
    B --> C{"ID valid?"}
    C -->|"No"| B
    C -->|"Yes"| D["Scan records"]
    D --> E{"Found?"}
    E -->|"No"| X["Not found"]
    E -->|"Yes"| F["Print ID"]
    F --> G["Print name"]
    G --> H["Print type"]
    H --> I["Print ports"]
    X --> Z["Print cost"]
    I --> Z
```

Search uses the unique **device ID**, not an array index. **Time O(V), space O(1)**.

## 6. Display network topology

**Input:** None.

```mermaid
flowchart TD
    A["Choose 6"] --> B["Print header"]
    B --> C["List devices"]
    C --> D{"Count = 0?"}
    D -->|"Yes"| X["Empty notice"]
    D -->|"No"| E["Print indexes"]
    E --> F["Print matrix rows"]
    F --> G["For each device"]
    G --> H["Scan links"]
    H --> I{"Any neighbor?"}
    I -->|"Yes"| J["Print neighbor IDs"]
    I -->|"No"| K["Print none"]
    J --> L{"More devices?"}
    K --> L
    L -->|"Yes"| G
    L -->|"No"| M["Print footer"]
    X --> Z["Print cost"]
    M --> Z
```

The displayed matrix uses **array indexes**; the adjacency list uses **device IDs**. An isolated device shows no neighbors. **Time O(V²), space O(1)**.

## 7. Breadth-first search (BFS)

**Input:** Starting ID, then whether to include disconnected components.

```mermaid
flowchart TD
    A["Choose 7"] --> B{"Count = 0?"}
    B -->|"Yes"| X["Empty error"]
    B -->|"No"| C["Read start ID"]
    C --> D{"ID valid?"}
    D -->|"No"| C
    D -->|"Yes"| E["Read Y/N"]
    E --> F{"Valid Y/N?"}
    F -->|"No"| E
    F -->|"Yes"| G["Find start"]
    G --> H{"Found?"}
    H -->|"No"| Y["Start error"]
    H -->|"Yes"| I["Init visited"]
    I --> J["Init queue"]
    J --> K["Mark start"]
    K --> L["Enqueue start"]
    L --> M{"Queue left?"}
    M -->|"Yes"| N["Dequeue index"]
    N --> O["Append ID"]
    O --> P["Set j = 0"]
    P --> Q{"j < V?"}
    Q -->|"Yes"| R{"Link and unseen?"}
    R -->|"Yes"| S["Mark j"]
    S --> T["Enqueue j"]
    T --> U["j +1"]
    R -->|"No"| U
    U --> Q
    Q -->|"No"| M
    M -->|"No"| W{"Include all?"}
    W -->|"No"| AA["Print order"]
    W -->|"Yes"| AB{"Unvisited left?"}
    AB -->|"No"| AA
    AB -->|"Yes"| AC["Choose next index"]
    AC --> AD["Mark + enqueue"]
    AD --> M
    X --> Z["Print cost"]
    Y --> Z
    AA --> Z
```

BFS visits a device, then its unvisited neighbors, using a **manually indexed queue** and a Boolean visited array. The queue stores indexes; the printed order uses IDs. With the **Y** option, remaining components are visited in ascending index order. **Time O(V²), space O(V)**.

## 8. Depth-first search (DFS)

**Input:** Starting ID, then whether to include disconnected components.

```mermaid
flowchart TD
    A["Choose 8"] --> B{"Count = 0?"}
    B -->|"Yes"| X["Empty error"]
    B -->|"No"| C["Read start ID"]
    C --> D{"ID valid?"}
    D -->|"No"| C
    D -->|"Yes"| E["Read Y/N"]
    E --> F{"Valid Y/N?"}
    F -->|"No"| E
    F -->|"Yes"| G["Find start"]
    G --> H{"Found?"}
    H -->|"No"| Y["Start error"]
    H -->|"Yes"| I["Init visited"]
    I --> J["Call visit(start)"]
    J --> K["Mark visited"]
    K --> L["Append ID"]
    L --> M["Scan j ascending"]
    M --> N{"Link and unseen?"}
    N -->|"Yes"| O["Call visit(j)"]
    O --> P["Return to caller"]
    P --> Q{"More j?"}
    N -->|"No"| Q
    Q -->|"Yes"| M
    Q -->|"No"| R["Return from visit"]
    R --> S{"All comps Y?"}
    S -->|"No"| AA["Print order"]
    S -->|"Yes"| T{"Unvisited left?"}
    T -->|"No"| AA
    T -->|"Yes"| U["Choose next index"]
    U --> V["Call visit(next)"]
    V --> S
    X --> Z["Print cost"]
    Y --> Z
    AA --> Z
```

**Recursive detail:** Every `visit(i)` call marks `i` and appends its ID, scans neighbors in ascending index order, calls `visit(j)` for each linked/unvisited neighbor, and **resumes the caller's scan after that call returns**. When all neighbors are checked, the call returns. The diagram abbreviates the repeated recursive calls, but these steps run at every depth. If **Y** was selected, DFS starts again at each remaining unvisited index. **Time O(V²), space O(V)** including recursion.

## 9. Count devices

**Input:** None.

```mermaid
flowchart TD
    A["Choose 9"] --> B["Read count"]
    B --> C["Read capacity 10"]
    C --> D["Print count / 10"]
    D --> Z["Print cost"]
```

The graph maintains the counter when devices are added or removed, so counting is constant-time. **Time O(1), space O(1)**.

## 10. Check direct link

**Input:** Two IDs.

```mermaid
flowchart TD
    A["Choose 10"] --> B["Read first ID"]
    B --> C{"Valid?"}
    C -->|"No"| B
    C -->|"Yes"| D["Read second ID"]
    D --> E{"Valid?"}
    E -->|"No"| D
    E -->|"Yes"| F["Search both IDs"]
    F --> G{"Both found?"}
    G -->|"No"| X["Missing ID"]
    G -->|"Yes"| H{"Same ID?"}
    H -->|"Yes"| Y["Self-link notice"]
    H -->|"No"| I["Find indexes"]
    I --> J["Read matrix [i][j]"]
    J --> K{"Value = 1?"}
    K -->|"Yes"| L["Link exists"]
    K -->|"No"| M["No direct link"]
    X --> Z["Print cost"]
    Y --> Z
    L --> Z
    M --> Z
```

The check looks for **one edge**, not a multihop route. Searching the two IDs costs O(V); reading a matrix cell after the indexes are known is O(1). **Time O(V), space O(1)**.

---

[README](../README.md) · [Contributing](../CONTRIBUTING.md)

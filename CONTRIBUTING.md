# Contributing to Nodex

Nodex is a final project for **Data Structures and Algorithms**. Its main purpose is to demonstrate graph representation and traversal in a small, offline Python network-connectivity scenario. Contributions should respect that scope and keep the code readable for students.

## How to contribute

1. Review [open issues](https://github.com/Kanechiii/nodex/issues) or open one describing a bug, documentation issue, or proposed change. For larger functional changes, discuss the approach before writing code.
2. Fork the repository or create a feature branch. Keep each change focused.
3. Update code and tests together when behavior changes. Document how you verified the result.
4. Run the checks below, then open a pull request against `main`. Explain the problem, your solution, and which tests you ran.
5. Respond to review feedback. Maintainers review the change and its CI results before merging.

## Run locally

Python 3.11 or newer is recommended; no third-party packages are needed.

```powershell
py main.py
py -m unittest discover -s tests -p "test_*.py" -v
py -m unittest discover -s tests -p "*_check.py" -v
```

On macOS/Linux, use `python3` instead of `py`. The [security and history checks](SECURITY.md) are available for a full Git clone.

## Working with the graph

- Keep the maximum of **10 devices** unless a scope change has been discussed.
- Preserve unique device IDs, the **symmetric adjacency matrix**, and port-capacity validation.
- BFS uses an indexed queue and a visited array; DFS uses recursion and a visited array. Neighbors are examined in ascending index order.
- Cover invalid input, missing or disconnected devices, duplicate links, and matrix changes after removing a device.
- Include time and auxiliary-space complexity notes when an algorithm changes.

See the [menu workflow guide](docs/WORKFLOWS.md) before modifying console behavior. For security-related concerns, follow [SECURITY.md](SECURITY.md) instead of posting sensitive details publicly.

Contributions are distributed under the repository's [MIT License](LICENSE). Please submit only work you have the right to share.

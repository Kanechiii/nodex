"""BFS tests; filenames do not have to begin with test_."""

import unittest
from contextlib import redirect_stdout
from io import StringIO

from models.device import Device
from structures.graph import NetworkGraph


class BFSTests(unittest.TestCase):
    def setUp(self):
        self.graph = NetworkGraph()

    def add_ids(self, *ids):
        with redirect_stdout(StringIO()):
            for device_id in ids:
                self.assertTrue(self.graph.add_device(Device(device_id, str(device_id), "PC", 9)))

    def link(self, first, second):
        with redirect_stdout(StringIO()):
            self.assertTrue(self.graph.connect_devices(first, second))

    def test_empty_graph(self):
        self.assertEqual(self.graph.bfs(99), [])
        self.assertEqual(self.graph.bfs(99, include_disconnected=True), [])

    def test_invalid_start(self):
        self.add_ids(10)
        with self.assertRaises(ValueError):
            self.graph.bfs(999)

    def test_cycle_and_ascending_index_order(self):
        self.add_ids(10, 20, 30, 40)
        self.link(10, 30)
        self.link(10, 20)
        self.link(30, 40)
        self.link(20, 40)
        self.assertEqual(self.graph.bfs(10), [10, 20, 30, 40])
        self.assertEqual(self.graph.bfs(10), [10, 20, 30, 40])

    def test_isolated_and_disconnected(self):
        self.add_ids(1, 2, 3, 4, 5)
        self.link(1, 2)
        self.link(4, 5)
        self.assertEqual(self.graph.bfs(1), [1, 2])
        self.assertEqual(self.graph.bfs(3), [3])
        self.assertEqual(self.graph.bfs(1, include_disconnected=True), [1, 2, 3, 4, 5])
        self.assertEqual(self.graph.bfs(3, include_disconnected=True), [3, 1, 2, 4, 5])

    def test_reindex_after_removing_middle_device(self):
        self.add_ids(10, 20, 30, 40)
        self.link(10, 20)
        self.link(20, 30)
        self.link(30, 40)
        with redirect_stdout(StringIO()):
            self.assertTrue(self.graph.remove_device(20))
        self.assertEqual(self.graph.bfs(30), [30, 40])
        self.assertEqual(self.graph.bfs(10, include_disconnected=True), [10, 30, 40])


if __name__ == "__main__":
    unittest.main()

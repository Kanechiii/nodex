"""CRUD, matrix-consistency, capacity and display tests."""

import unittest
from contextlib import redirect_stdout
from io import StringIO

from models.device import Device
from structures.graph import NetworkGraph


class GraphTests(unittest.TestCase):
    def setUp(self):
        self.g = NetworkGraph()

    def quiet(self, action, *args):
        with redirect_stdout(StringIO()):
            return action(*args)

    def add(self, device_id, ports=9):
        return self.quiet(self.g.add_device, Device(device_id, f"D{device_id}", "PC", ports))

    def assert_symmetric_and_unused_zero(self):
        n = self.g.device_count
        for i in range(self.g.max_devices):
            for j in range(self.g.max_devices):
                self.assertEqual(self.g.adjacency_matrix[i][j], self.g.adjacency_matrix[j][i])
                if i >= n or j >= n:
                    self.assertEqual(self.g.adjacency_matrix[i][j], 0)

    def test_unique_ids_capacity_and_record_validation(self):
        self.assertEqual(self.g.get_device_count(), 0)
        for i in range(10):
            self.assertTrue(self.add(i))
        self.assertFalse(self.add(0))
        self.assertFalse(self.add(10))
        self.assertEqual(self.g.get_device_count(), 10)
        self.assertEqual(self.g.find_device_index(7), 7)
        self.assertIsNone(self.g.search_device(99))
        self.assertEqual(self.g.search_device(7).hostname, "D7")

    def test_port_capacity_and_link_validation(self):
        self.assertTrue(self.add(1, 1))
        self.assertTrue(self.add(2, 1))
        self.assertTrue(self.add(3, 1))
        self.assertFalse(self.quiet(self.g.connect_devices, 1, 1))
        self.assertFalse(self.quiet(self.g.connect_devices, 1, 9))
        self.assertTrue(self.quiet(self.g.connect_devices, 1, 2))
        self.assertFalse(self.quiet(self.g.connect_devices, 1, 2))
        self.assertFalse(self.quiet(self.g.connect_devices, 1, 3))
        self.assertTrue(self.g.is_directly_connected(2, 1))
        self.assertFalse(self.quiet(self.g.disconnect_devices, 1, 3))
        self.assertFalse(self.quiet(self.g.disconnect_devices, 1, 1))
        self.assertFalse(self.quiet(self.g.disconnect_devices, 1, 99))
        self.assertTrue(self.quiet(self.g.disconnect_devices, 1, 2))
        self.assertTrue(self.quiet(self.g.connect_devices, 1, 3))
        self.assert_symmetric_and_unused_zero()

    def test_optional_port_enforcement(self):
        g = NetworkGraph(enforce_port_capacity=False)
        with redirect_stdout(StringIO()):
            for i in range(3):
                self.assertTrue(g.add_device(Device(i, str(i), "PC", 0)))
            self.assertTrue(g.connect_devices(0, 1))
            self.assertTrue(g.connect_devices(0, 2))
        self.assertTrue(g.is_directly_connected(0, 1))

    def test_matrix_compaction_remove_first_middle_last_and_readd(self):
        for i in [10, 20, 30, 40, 50]:
            self.assertTrue(self.add(i))
        for a, b in [(10, 20), (20, 30), (30, 40), (40, 50), (10, 50)]:
            self.assertTrue(self.quiet(self.g.connect_devices, a, b))
        self.assertTrue(self.quiet(self.g.remove_device, 20))
        self.assertFalse(self.g.is_directly_connected(10, 30))
        self.assertTrue(self.g.is_directly_connected(30, 40))
        self.assertTrue(self.g.is_directly_connected(10, 50))
        self.assertEqual([self.g.devices[i].device_id for i in range(4)], [10, 30, 40, 50])
        self.assert_symmetric_and_unused_zero()
        self.assertTrue(self.quiet(self.g.remove_device, 10))
        self.assertTrue(self.quiet(self.g.remove_device, 50))
        self.assertEqual([self.g.devices[i].device_id for i in range(2)], [30, 40])
        self.assertTrue(self.g.is_directly_connected(30, 40))
        self.assertFalse(self.quiet(self.g.remove_device, 999))
        self.assertTrue(self.add(60))
        self.assertFalse(self.g.is_directly_connected(30, 60))
        self.assert_symmetric_and_unused_zero()

    def test_display_indexes_matrix_and_adjacency(self):
        self.add(11)
        self.add(22)
        self.quiet(self.g.connect_devices, 11, 22)
        out = StringIO()
        with redirect_stdout(out):
            self.g.display_graph()
        text = out.getvalue()
        self.assertIn("[0] ID: 11", text)
        self.assertIn("[1] ID: 22", text)
        self.assertIn("Adjacency Matrix", text)
        self.assertIn("Adjacency List", text)
        self.assertIn("11: 22", text)


if __name__ == "__main__":
    unittest.main()

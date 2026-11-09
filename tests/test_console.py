"""Tests for the Nodex console and graph integration."""

import unittest
from contextlib import redirect_stdout
from io import StringIO
from unittest.mock import patch

import main as console
from structures.graph import NetworkGraph


class ConsoleTests(unittest.TestCase):
    def setUp(self):
        self.graph = NetworkGraph()
        with redirect_stdout(StringIO()):
            console.seed_network(self.graph)

    def run_operation(self, choice, answers=()):
        out = StringIO()
        with patch("builtins.input", side_effect=list(answers)), redirect_stdout(out):
            console.do_operation(self.graph, choice)
            console.show_complexity(choice)
        return out.getvalue()

    def test_seed_and_isolated_device(self):
        self.assertEqual(self.graph.get_device_count(), 5)
        for first, second in ((101, 102), (101, 103), (102, 104)):
            self.assertTrue(self.graph.is_directly_connected(first, second))
        self.assertFalse(self.graph.is_directly_connected(101, 105))

    def test_menu_lists_actions_group_and_exit(self):
        out = StringIO()
        with redirect_stdout(out):
            console.show_menu(self.graph)
        text = out.getvalue()
        self.assertIn(console.GROUP_NAME, text)
        for index in range(11):
            self.assertIn(f"{index:2}.", text)

    def test_add_search_remove_and_count(self):
        self.assertIn("added successfully", self.run_operation(1, ("106", "Laptop-F", "Computer", "2")))
        self.assertIn("Laptop-F", self.run_operation(5, ("106",)))
        self.assertIn("Active devices: 6", self.run_operation(9))
        self.assertIn("removed successfully", self.run_operation(2, ("106",)))
        self.assertIn("not found", self.run_operation(5, ("106",)))

    def test_connect_disconnect_and_direct_link(self):
        self.assertIn("connected.", self.run_operation(3, ("103", "105")))
        self.assertIn("Direct link exists", self.run_operation(10, ("103", "105")))
        self.assertIn("disconnected.", self.run_operation(4, ("103", "105")))
        self.assertIn("No direct link", self.run_operation(10, ("103", "105")))
        self.assertIn("not found", self.run_operation(2, ("999",)))

    def test_bfs_dfs_disconnected_and_topology(self):
        self.assertIn("101 -> 102 -> 103 -> 104", self.run_operation(7, ("101", "n")))
        self.assertIn("101 -> 102 -> 104 -> 103 -> 105", self.run_operation(8, ("101", "y")))
        self.assertIn("Traversal error", self.run_operation(7, ("999", "n")))
        self.assertIn("Adjacency Matrix", self.run_operation(6))

    def test_bad_input_duplicate_and_self_link(self):
        output = self.run_operation(1, ("abc", "-1", "106", "", "Laptop", "", "PC", "-2", "2"))
        self.assertIn("Invalid input", output)
        self.assertIn("Duplicate device ID", self.run_operation(1, ("101",)))
        self.assertIn("cannot connect to itself", self.run_operation(3, ("101", "101")))

    def test_full_and_empty_graph(self):
        for new_id in range(106, 111):
            self.run_operation(1, (str(new_id), f"Device-{new_id}", "PC", "1"))
        self.assertEqual(self.graph.get_device_count(), 10)
        self.assertIn("Network is full", self.run_operation(1))
        empty = NetworkGraph()
        out = StringIO()
        with redirect_stdout(out):
            console.do_operation(empty, 7)
        self.assertIn("Network is empty", out.getvalue())

    def test_invalid_menu_and_exit(self):
        out = StringIO()
        with patch("builtins.input", side_effect=("oops", "11", "9", "0")), redirect_stdout(out):
            console.main()
        text = out.getvalue()
        self.assertEqual(text.count("Invalid menu selection"), 2)
        self.assertIn("Active devices: 5", text)
        self.assertIn("Exiting Nodex", text)


if __name__ == "__main__":
    unittest.main()

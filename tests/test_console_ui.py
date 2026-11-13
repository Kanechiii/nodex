"""Regression tests for Nodex's display-only console presentation."""
import io
import unittest
from contextlib import redirect_stdout
from unittest.mock import patch

import console_ui
import main
from structures.graph import NetworkGraph


class ConsolePresentationTests(unittest.TestCase):
    def setUp(self):
        self.graph = NetworkGraph()
        with redirect_stdout(io.StringIO()):
            main.seed_network(self.graph)

    def test_all_choices_remain_visible(self):
        out = io.StringIO()
        with redirect_stdout(out):
            main.show_menu(self.graph)
        screen = out.getvalue()
        for number, (label, _, _) in enumerate(main.OPERATIONS, 1):
            self.assertIn(f"{number:2}. {label}", screen)
        self.assertIn(" 0. Exit", screen)
        self.assertIn("Enter B (Back)", screen)
        self.assertIn("5/10", screen)

    def test_redirected_output_has_no_ansi_or_animation(self):
        out = io.StringIO()
        with patch.object(console_ui.time, "sleep", side_effect=AssertionError("animation should be skipped")):
            with redirect_stdout(out):
                console_ui.show_splash()
                main.show_menu(self.graph)
        self.assertNotIn("\\x1b[", out.getvalue())
        self.assertIn("NODEX", out.getvalue())

    def test_operation_header_does_not_change_graph(self):
        before = [row[:] for row in self.graph.adjacency_matrix]
        out = io.StringIO()
        with redirect_stdout(out):
            console_ui.show_operation(7, main.OPERATIONS)
        self.assertIn("BREADTH-FIRST SEARCH", out.getvalue())
        self.assertEqual(before, self.graph.adjacency_matrix)


if __name__ == "__main__":
    unittest.main()

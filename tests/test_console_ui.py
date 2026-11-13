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
        self.assertNotIn(chr(27) + "[", out.getvalue())
        self.assertIn("NODEX", out.getvalue())

    def test_operation_header_does_not_change_graph(self):
        before = [row[:] for row in self.graph.adjacency_matrix]
        out = io.StringIO()
        with redirect_stdout(out):
            console_ui.show_operation(7, main.OPERATIONS)
        self.assertIn("BREADTH-FIRST SEARCH", out.getvalue())
        self.assertEqual(before, self.graph.adjacency_matrix)


    def test_readme_logo_has_same_nodes_and_edges(self):
        self.assertEqual(
            console_ui._LOGO_POINTS,
            ((858, 140), (953, 81), (1053, 137), (955, 204)),
        )
        self.assertEqual(
            console_ui._LOGO_EDGES,
            ((0, 1), (1, 2), (2, 3), (3, 0), (1, 3), (0, 2)),
        )

    def test_logo_rotates_and_stays_within_fixed_dimensions(self):
        starting_frame = console_ui._logo_frame(0)
        turned_frame = console_ui._logo_frame(45)
        self.assertNotEqual(starting_frame, turned_frame)
        self.assertEqual(len(starting_frame), 9)
        self.assertTrue(all(len(line) == 18 for line in starting_frame))
        self.assertEqual(starting_frame, console_ui._logo_frame(360))

    def test_disable_animation_renders_static_readme_logo(self):
        out = io.StringIO()
        with patch.dict("os.environ", {"NODEX_NO_ANIMATION": "1"}), (
            patch.object(console_ui, "_interactive", return_value=True)
        ), patch.object(console_ui.time, "sleep", side_effect=AssertionError("should not animate")):
            with redirect_stdout(out):
                console_ui.show_splash()
        self.assertIn("Nodex", out.getvalue())
        self.assertIn("NETWORK CONNECTIVITY SIMULATOR", out.getvalue())
        self.assertNotIn("\x1b[9A", out.getvalue())

    def test_interactive_animation_restores_cursor(self):
        out = io.StringIO()
        with patch.object(console_ui, "_interactive", return_value=True), (
            patch.object(console_ui, "_supports_braille", return_value=True)
        ), patch.object(console_ui.time, "sleep", return_value=None) as sleep:
            with redirect_stdout(out):
                console_ui.show_splash()
        result = out.getvalue()
        self.assertIn("\x1b[?25l", result)
        self.assertTrue(result.endswith("\x1b[?25h"))
        self.assertEqual(result.count("\x1b[9A"), len(console_ui._SPIN_ANGLES) - 1)
        self.assertEqual(sleep.call_count, len(console_ui._SPIN_ANGLES) - 1)



if __name__ == "__main__":
    unittest.main()

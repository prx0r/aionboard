"""Tests for the onboard buddy: per-business graph and scoped answers."""

import unittest

from aionboard import connect, init_business_tables
from aionboard.buddy import buddy_answer, buddy_ask, build_business_graph
from aionboard.businesses import create_business


def business_db():
    connection = connect()
    init_business_tables(connection)
    return connection


class BusinessGraphTests(unittest.TestCase):
    def test_graph_contains_vertical_knowledge(self):
        connection = business_db()
        business_id = create_business(
            connection, display_name="Fictional Nails", kind="sole_trader", vertical="nails"
        )
        graph = build_business_graph(connection, business_id, "nails")
        self.assertEqual(graph["business_id"], business_id)
        self.assertEqual(graph["vertical"], "nails")
        self.assertTrue(graph["profile"]["pain_mappings"])
        self.assertTrue(graph["profile"]["current_stack"])

    def test_graph_without_business_row_still_builds(self):
        connection = business_db()
        graph = build_business_graph(connection, "biz-ghost-001", "nails")
        self.assertEqual(graph["business"]["display_name"], "biz-ghost-001")

    def test_blank_business_rejected(self):
        connection = business_db()
        with self.assertRaises(ValueError):
            build_business_graph(connection, "   ", "nails")


class BuddyAskTests(unittest.TestCase):
    def setUp(self):
        connection = business_db()
        self.business_id = create_business(
            connection, display_name="Fictional Nails", kind="sole_trader", vertical="nails"
        )
        self.graph = build_business_graph(connection, self.business_id, "nails")

    def test_answers_from_business_graph(self):
        results = buddy_ask(self.graph, "nail deposits no-shows")
        self.assertTrue(results)
        for result in results:
            self.assertIn("source", result)

    def test_empty_question_returns_nothing(self):
        self.assertEqual(buddy_ask(self.graph, "   "), [])

    def test_answer_admits_ignorance(self):
        text = buddy_answer([], "Fictional Nails")
        self.assertIn("don't have verified information", text)

    def test_answer_names_business_and_limits(self):
        results = buddy_ask(self.graph, "deposits reminders")
        text = buddy_answer(results, "Fictional Nails")
        self.assertIn("Fictional Nails", text)
        self.assertIn("can't send messages", text)

    def test_no_cross_business_leakage(self):
        other = build_business_graph(self.graph_connection(), "biz-other-001", "electrician")
        mine = [r["id"] for r in buddy_ask(self.graph, "quote price book")]
        theirs = [r["id"] for r in buddy_ask(other, "quote price book")]
        # Electrician graph knows quoting; nails graph must not.
        self.assertTrue(theirs)
        self.assertNotIn("quote-follower", mine)

    def graph_connection(self):
        connection = business_db()
        create_business(
            connection, display_name="Fictional Sparks", kind="sole_trader", vertical="electrician"
        )
        return connection


if __name__ == "__main__":
    unittest.main(verbosity=2)

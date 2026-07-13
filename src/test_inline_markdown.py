'''
Unit test for inline_markdown.py that check different types of delimiters
'''
import unittest
from inline_markdown import split_nodes_delimiter
from textnode import *

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_no_delimiter(self):
        # string with no delimter. Should retunr just text
        node = TextNode("This is text with a no block word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes,
            [
                TextNode("This is text with a no block word", TextType.TEXT),
            ]
        )

    def test_double_delimiter(self):
        # A string with the delimiter used twice, producing two separate bolded/coded sections
        node = TextNode("This is text with a **bold block once** and a **bold block twice**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bold block once", TextType.BOLD),
                TextNode(" and a ", TextType.TEXT),
                TextNode("bold block twice", TextType.BOLD),
            ]
        )

    def test_empty_string(self):
        # An empty string edge case
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [])

    def test_delimiter_at_start(self):
        # delimiter at the very start of the text
        node = TextNode("**This is text with a bold block** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes,
            [
                TextNode("This is text with a bold block", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ]
        )

    def test_nontext_node(self):
        # node whose text_type is not TEXT
        node = TextNode("This is code block", TextType.CODE)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes,
            [
                TextNode("This is code block", TextType.CODE),
            ]
        )

    def test_multiple_nodes(self):
        # multiple nodes passed into new_nodes
        node = TextNode("This is code block", TextType.CODE)
        node1 = TextNode("This is text with a **bold block** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node, node1], "**", TextType.BOLD)
        self.assertEqual(new_nodes,
            [
                TextNode("This is code block", TextType.CODE),
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bold block", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ]
        )

    def test_bold(self):
        node = TextNode("This is text with a **bold block** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bold block", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ]
        )

    def test_italic(self):
        node = TextNode("This is text with a _italic block_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("italic block", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ]
        )

    def test_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ]
        )


if __name__ == "__main__":
    unittest.main()

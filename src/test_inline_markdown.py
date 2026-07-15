'''
Unit test for inline_markdown.py that check different types of delimiters and regex statements
'''
import unittest
from inline_markdown import *
from textnode import *

class TestSplitNodesDelimiter(unittest.TestCase):
    def test_no_delimiter(self):
        node = TextNode("This is text with a no block word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes,
            [
                TextNode("This is text with a no block word", TextType.TEXT),
            ]
        )

    def test_double_delimiter(self):
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
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [])

    def test_delimiter_at_start(self):
        node = TextNode("**This is text with a bold block** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes,
            [
                TextNode("This is text with a bold block", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ]
        )

    def test_nontext_node(self):
        node = TextNode("This is code block", TextType.CODE)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes,
            [
                TextNode("This is code block", TextType.CODE),
            ]
        )

    def test_multiple_nodes(self):
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

    # testing regex statements
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)


    def test_multiple_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )
        self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)


    def test_multiple_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)


    def test_nonlink_brackets(self):
        matches = extract_markdown_images(
            "Check the [docs] (not a link) and also ![alt](url.com)"
        )
        self.assertListEqual([("alt", "url.com")], matches)


    def test_nonlink_parens(self):
        matches = extract_markdown_images(
            "(just a note) and ![alt](url.com)"
        )
        self.assertListEqual([("alt", "url.com")], matches)


    def test_image_and_link(self):
        matches = extract_markdown_images(
            "[boot](boot.dev) and ![alt](url.com)"
        )
        self.assertListEqual([("alt", "url.com")], matches)

    def test_image_no_link(self):
        matches = extract_markdown_images(
            "testing ![image no link]()"
        )
        self.assertListEqual([("image no link", "")], matches)

if __name__ == "__main__":
    unittest.main()

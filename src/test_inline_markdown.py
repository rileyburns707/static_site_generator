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

    # test split_nodes_link and split_nodes_image
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    
    def test_no_images_or_links(self):
        #Text with no images/links at all (should return the node unchanged)
        node = TextNode(
            "This is text with nothing",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("This is text with nothing", TextType.TEXT)], new_nodes)
    
    def test_start_with_image(self):
        #Text that starts immediately with an image/link (no leading text before it)
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) at the start",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" at the start", TextType.TEXT),
            ],
            new_nodes,
        )
    
    def test_end_with_link(self):
        #Text that ends immediately after an image/link (no trailing text after it)
        node = TextNode(
            "link at end [link](url.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link at end ", TextType.TEXT),
                TextNode("link", TextType.LINK, "url.com"),
            ],
            new_nodes,
        )

    def test_back_to_back_images(self):
        # Text with multiple images/links back-to-back
        node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png)![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_non_text_node(self):
        #A TextNode that isn't TextType.TEXT to begin with (should pass through untouched)
        node = TextNode("`This is code`", TextType.CODE)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([TextNode("`This is code`", TextType.CODE)], new_nodes)

    def test_link_and_look_a_like(self):
        #Text with both a link and something that looks like an image (to make sure your link regex doesn't accidentally grab image syntax, and vice versa)
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a fake [second image test] but it shouldn't (work)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a fake [second image test] but it shouldn't (work)", TextType.TEXT),
            ],
            new_nodes,
        )


    # test text_to_textnodes function that combines all the split node functions together
    def test_if_eq(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_text = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            new_text
        )

    def test_different_order(self):
        text = "This is _italic_ with an **text** word and a `code block` and an [link](https://boot.dev) and a ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)"
        new_text = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" with an ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
            new_text
        )

    def test_not_all_function_used(self):
        text = "[a link](url) and **bold**"
        new_text = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("a link", TextType.LINK, "url"),
                TextNode(" and ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
            ],
            new_text
        )

    def test_no_markdwown(self):
        text = "No markdown used"
        new_text = text_to_textnodes(text)
        self.assertListEqual([TextNode("No markdown used", TextType.TEXT)], new_text)

    def test_double_markdown(self):
        text = "**og bold** and **bold**"
        new_text = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("og bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
            ],
            new_text
        )


if __name__ == "__main__":
    unittest.main()

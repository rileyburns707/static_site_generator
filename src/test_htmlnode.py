import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("p", "this is a paragraph")
        node2 = HTMLNode("p", "this is a paragraph")
        self.assertEqual(node, node2)

    def test_props_to_html(self):
        node = HTMLNode("a", "this is an attribute", [], {"href": "https://www.google.com"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com"')

    def test_noteq(self):
        node = HTMLNode("p", "this is an attribute", [], {"href": "https://www.google.com"})
        node2 = HTMLNode("p", "this is a paragraph")
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()

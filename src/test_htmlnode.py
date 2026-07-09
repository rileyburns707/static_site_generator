import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

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

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
    
    def test_leaf_to_html_h(self):
        node = LeafNode("h", "Header test")
        self.assertEqual(node.to_html(), "<h>Header test</h>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')
    
    # testing ParentNode
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span><b>grandchild</b></span></div>")

    def test_to_html_with_no_children(self):
        parent_node = ParentNode("p", [])
        self.assertEqual(parent_node.to_html(), "<p></p>")

    def test_to_html_with_no_grandchildren(self):
        child_node = ParentNode("span", [])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span></span></div>")

    def test_to_html_multiple_children(self):
        parent = ParentNode("p", [
            LeafNode("b", "Bold"),
            LeafNode(None, " normal "),
            LeafNode("i", "italic"),
        ])
        self.assertEqual(parent.to_html(), "<p><b>Bold</b> normal <i>italic</i></p>")
     
    def test_to_html_no_tag_raises(self):
         parent = ParentNode(None, [LeafNode(None, "text")])
         with self.assertRaises(ValueError):
             parent.to_html()

    def test_to_html_none_children_raises(self):
         parent = ParentNode("div", None)
         with self.assertRaises(ValueError):
             parent.to_html()

if __name__ == "__main__":
    unittest.main()

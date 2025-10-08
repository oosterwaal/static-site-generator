import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from textnode import TextNode, TextType


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )

    def test_props_to_html_no_props(self):
        node = HTMLNode("div", "Hello, world!")
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_single_prop(self):
        node = HTMLNode("a", "Click me!", None, {"href": "https://www.google.com"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com"')

    def test_props_to_html_multiple_props(self):
        node = HTMLNode(
            "a",
            "Click me!",
            None,
            {
                "href": "https://www.google.com",
                "target": "_blank",
                "class": "external-link"
            }
        )
        expected = ' href="https://www.google.com" target="_blank" class="external-link"'
        self.assertEqual(node.props_to_html(), expected)

    def test_to_html_not_implemented(self):
        node = HTMLNode("div", "test")
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_repr(self):
        node = HTMLNode("p", "What a strange world", None, {"class": "primary"})
        self.assertEqual(
            repr(node),
            "HTMLNode(p, What a strange world, children: None, {'class': 'primary'})",
        )

    def test_repr_no_props(self):
        node = HTMLNode("h1", "Title")
        self.assertEqual(
            repr(node),
            "HTMLNode(h1, Title, children: None, None)",
        )

    def test_repr_with_children(self):
        child_node = HTMLNode("span", "child")
        parent_node = HTMLNode("div", None, [child_node])
        self.assertEqual(
            repr(parent_node),
            "HTMLNode(div, None, children: [HTMLNode(span, child, children: None, None)], None)",
        )


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "This is raw text")
        self.assertEqual(node.to_html(), "This is raw text")

    def test_leaf_to_html_no_value_raises_error(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_to_html_with_props(self):
        node = LeafNode("img", "alt text", {"src": "image.jpg", "alt": "An image"})
        self.assertEqual(node.to_html(), '<img src="image.jpg" alt="An image">alt text</img>')

    def test_leaf_to_html_h1(self):
        node = LeafNode("h1", "Main Title")
        self.assertEqual(node.to_html(), "<h1>Main Title</h1>")

    def test_leaf_to_html_span_with_class(self):
        node = LeafNode("span", "Highlighted text", {"class": "highlight"})
        self.assertEqual(node.to_html(), '<span class="highlight">Highlighted text</span>')


class TestParentNode(unittest.TestCase):
    def test_parent_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_parent_to_html_with_multiple_children(self):
        child1 = LeafNode("b", "Bold text")
        child2 = LeafNode("i", "italic text")
        parent_node = ParentNode("p", [child1, child2])
        self.assertEqual(parent_node.to_html(), "<p><b>Bold text</b><i>italic text</i></p>")

    def test_parent_to_html_nested_parents(self):
        grandchild = LeafNode("span", "grandchild")
        child = ParentNode("div", [grandchild])
        parent = ParentNode("div", [child])
        self.assertEqual(parent.to_html(), "<div><div><span>grandchild</span></div></div>")

    def test_parent_to_html_with_props(self):
        child = LeafNode("span", "child")
        parent = ParentNode("div", [child], {"class": "container"})
        self.assertEqual(parent.to_html(), '<div class="container"><span>child</span></div>')

    def test_parent_to_html_no_tag_raises_error(self):
        child = LeafNode("span", "child")
        parent = ParentNode(None, [child])
        with self.assertRaises(ValueError) as context:
            parent.to_html()
        self.assertIn("ParentNode must have a tag", str(context.exception))

    def test_parent_to_html_no_children_raises_error(self):
        parent = ParentNode("div", None)
        with self.assertRaises(ValueError) as context:
            parent.to_html()
        self.assertIn("ParentNode must have children", str(context.exception))

    def test_parent_to_html_complex_nested_structure(self):
        leaf1 = LeafNode("b", "Bold text")
        leaf2 = LeafNode(None, " and some normal text ")
        leaf3 = LeafNode("i", "italic text")
        leaf4 = LeafNode(None, " and ")
        leaf5 = LeafNode("code", "code block")
        
        child_paragraph = ParentNode("p", [leaf1, leaf2, leaf3, leaf4, leaf5])
        grandparent = ParentNode("div", [child_paragraph])
        
        expected = "<div><p><b>Bold text</b> and some normal text <i>italic text</i> and <code>code block</code></p></div>"
        self.assertEqual(grandparent.to_html(), expected)


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold text")
        self.assertEqual(html_node.props, None)

    def test_italic(self):
        node = TextNode("This is italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is italic text")
        self.assertEqual(html_node.props, None)

    def test_code(self):
        node = TextNode("console.log('hello')", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "console.log('hello')")
        self.assertEqual(html_node.props, None)

    def test_link(self):
        node = TextNode("Click here", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Click here")
        self.assertEqual(html_node.props, {"href": "https://www.google.com"})

    def test_image(self):
        node = TextNode("Alt text for image", TextType.IMAGE, "https://example.com/image.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://example.com/image.jpg", "alt": "Alt text for image"})

    def test_unsupported_text_type_raises_error(self):
        # Create a mock TextNode with an invalid text_type
        node = TextNode("Some text", "INVALID_TYPE")
        with self.assertRaises(ValueError) as context:
            text_node_to_html_node(node)
        self.assertIn("Unsupported TextType", str(context.exception))


if __name__ == "__main__":
    unittest.main()
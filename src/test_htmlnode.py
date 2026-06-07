import unittest
from htmlnode import HTMLNode,LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        htmlnode = HTMLNode('a', 'value',None,{"href":'https:/bootdev.com', "target":"_blank"})
        self.assertIsInstance(htmlnode.props_to_html(), str)
    def test_repr(self):
        htmlnode = HTMLNode('a', 'value',None,{"href":'https:/bootdev.com', "target":"_blank"})
        self.assertIsInstance(htmlnode.__repr__(), str)
    def test_to_html(self):
        htmlnode = HTMLNode('a', 'value',None,{"href":'https:/bootdev.com', "target":"_blank"})
        self.assertRaises(NotImplementedError, htmlnode.tohtml)
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.tohtml(), "<p>Hello, world!</p>")
    def test_no_tag(self):
        node = LeafNode(None, "hello")
        self.assertEqual(node.tohtml(), "hello")
    def test_single_leaf_child(self):
        """Test ParentNode with a single LeafNode child"""
        leaf = LeafNode("b", "Bold")
        parent = ParentNode("p", [leaf])
        self.assertEqual(parent.tohtml(), "<p><b>Bold</b></p>")

    def test_multiple_leaf_children(self):
        """Test ParentNode with multiple LeafNode children"""
        leaf1 = LeafNode("b", "Bold")
        leaf2 = LeafNode("i", "Italic")
        leaf3 = LeafNode(None, "Plain")
        parent = ParentNode("p", [leaf1, leaf2, leaf3])
        self.assertEqual(parent.tohtml(), "<p><b>Bold</b><i>Italic</i>Plain</p>")

    # ===== NESTED PARENT NODES =====
    def test_nested_parent_nodes_two_levels(self):
        """Test ParentNode containing another ParentNode (two levels)"""
        leaf = LeafNode("span", "text")
        inner_parent = ParentNode("div", [leaf])
        outer_parent = ParentNode("section", [inner_parent])
        self.assertEqual(outer_parent.tohtml(), "<section><div><span>text</span></div></section>")

    def test_deeply_nested_parent_nodes(self):
        """Test deeply nested ParentNodes (5+ levels)"""
        leaf = LeafNode("b", "deep")
        current = ParentNode("level5", [leaf])
        current = ParentNode("level4", [current])
        current = ParentNode("level3", [current])
        current = ParentNode("level2", [current])
        outer = ParentNode("level1", [current])
        
        expected = "<level1><level2><level3><level4><level5><b>deep</b></level5></level4></level3></level2></level1>"
        self.assertEqual(outer.tohtml(), expected)

    def test_mixed_parent_and_leaf_children(self):
        """Test ParentNode with mixed parent and leaf children"""
        leaf1 = LeafNode("b", "Bold")
        inner_parent = ParentNode("span", [LeafNode("i", "Italic")])
        leaf2 = LeafNode("u", "Underline")
        
        parent = ParentNode("p", [leaf1, inner_parent, leaf2])
        expected = "<p><b>Bold</b><span><i>Italic</i></span><u>Underline</u></p>"
        self.assertEqual(parent.tohtml(), expected)

    # ===== PROPERTIES (PROPS) =====
    def test_single_prop(self):
        """Test ParentNode with a single property"""
        leaf = LeafNode("b", "text")
        parent = ParentNode("p", [leaf], props={"class": "intro"})
        self.assertEqual(parent.tohtml(), '<p class="intro"><b>text</b></p>')

    def test_multiple_props(self):
        """Test ParentNode with multiple properties"""
        leaf = LeafNode("b", "text")
        parent = ParentNode("p", [leaf], props={"class": "intro", "id": "first"})
        html = parent.tohtml()
        # Check that both props are present (order may vary)
        self.assertIn('class="intro"', html)
        self.assertIn('id="first"', html)
        self.assertIn("<p ", html)
        self.assertIn("><b>text</b></p>", html)

    def test_no_props(self):
        """Test ParentNode with no properties (None)"""
        leaf = LeafNode("b", "text")
        parent = ParentNode("p", [leaf], props=None)
        self.assertEqual(parent.tohtml(), "<p><b>text</b></p>")

    def test_props_with_special_characters(self):
        """Test props with special characters"""
        leaf = LeafNode("a", "link")
        parent = ParentNode("div", [leaf], props={"data-value": "hello world", "title": "A & B"})
        html = parent.tohtml()
        self.assertIn('data-value="hello world"', html)
        self.assertIn('title="A & B"', html)

    # ===== ERROR CASES =====
    def test_error_no_tag(self):
        """Test that ValueError is raised when tag is None"""
        leaf = LeafNode("b", "text")
        parent = ParentNode(None, [leaf])
        with self.assertRaises(ValueError) as context:
            parent.tohtml()
        self.assertIn("no tag", str(context.exception).lower())

    def test_error_no_children(self):
        """Test that ValueError is raised when children is None"""
        parent = ParentNode("p", None)
        with self.assertRaises(ValueError) as context:
            parent.tohtml()
        self.assertIn("children", str(context.exception).lower())

    def test_error_empty_children_list(self):
        """Test that ValueError is raised when children list is empty"""
        parent = ParentNode("p", [])
        with self.assertRaises(ValueError) as context:
            parent.tohtml()
        self.assertIn("children", str(context.exception).lower())

    # ===== LEAF NODES WITH NO TAG =====
    def test_leaf_child_with_no_tag(self):
        """Test ParentNode with LeafNode that has no tag (plain text)"""
        leaf = LeafNode(None, "This is plain text")
        parent = ParentNode("p", [leaf])
        self.assertEqual(parent.tohtml(), "<p>This is plain text</p>")

    def test_multiple_leaf_children_with_no_tag(self):
        """Test multiple LeafNodes with no tag mixed with tagged ones"""
        leaf1 = LeafNode(None, "Start ")
        leaf2 = LeafNode("b", "bold")
        leaf3 = LeafNode(None, " end")
        parent = ParentNode("p", [leaf1, leaf2, leaf3])
        self.assertEqual(parent.tohtml(), "<p>Start <b>bold</b> end</p>")

    # ===== EDGE CASES WITH VALUES =====
    def test_empty_string_value(self):
        """Test LeafNode with empty string value"""
        leaf = LeafNode("span", "")
        parent = ParentNode("p", [leaf])
        self.assertEqual(parent.tohtml(), "<p><span></span></p>")

    def test_whitespace_only_value(self):
        """Test LeafNode with whitespace-only value"""
        leaf = LeafNode("span", "   ")
        parent = ParentNode("p", [leaf])
        self.assertEqual(parent.tohtml(), "<p><span>   </span></p>")

    def test_value_with_html_characters(self):
        """Test that HTML special characters are NOT escaped (as per current implementation)"""
        leaf = LeafNode("span", "<script>alert('xss')</script>")
        parent = ParentNode("p", [leaf])
        # Note: Current implementation doesn't escape, this documents that behavior
        self.assertEqual(parent.tohtml(), "<p><span><script>alert('xss')</script></span></p>")

    # ===== COMPLEX NESTING SCENARIOS =====
    def test_parent_with_multiple_children_at_each_level(self):
        """Test complex structure with multiple children at multiple levels"""
        leaf1 = LeafNode("b", "1")
        leaf2 = LeafNode("b", "2")
        inner1 = ParentNode("span", [leaf1, leaf2])
        
        leaf3 = LeafNode("i", "3")
        leaf4 = LeafNode("i", "4")
        inner2 = ParentNode("span", [leaf3, leaf4])
        
        outer = ParentNode("p", [inner1, inner2])
        expected = "<p><span><b>1</b><b>2</b></span><span><i>3</i><i>4</i></span></p>"
        self.assertEqual(outer.tohtml(), expected)

    def test_parent_with_many_children(self):
        """Test ParentNode with many children (10+)"""
        children = [LeafNode("span", f"child{i}") for i in range(10)]
        parent = ParentNode("div", children)
        html = parent.tohtml()
        self.assertTrue(html.startswith("<div>"))
        self.assertTrue(html.endswith("</div>"))
        for i in range(10):
            self.assertIn(f"child{i}", html)

    def test_realistic_html_structure(self):
        """Test realistic HTML document structure"""
        # Building a list with items
        li1 = ParentNode("li", [LeafNode(None, "Item 1")])
        li2 = ParentNode("li", [LeafNode(None, "Item 2")])
        li3 = ParentNode("li", [LeafNode(None, "Item 3")])
        ul = ParentNode("ul", [li1, li2, li3])
        
        # Building a paragraph with mixed content
        p = ParentNode("p", [
            LeafNode(None, "This is "),
            LeafNode("b", "bold"),
            LeafNode(None, " and "),
            LeafNode("i", "italic"),
            LeafNode(None, " text.")
        ])
        
        # Wrap in a div
        container = ParentNode("div", [p, ul], props={"class": "container"})
        
        html = container.tohtml()
        self.assertIn('<div class="container">', html)
        self.assertIn("<p>This is <b>bold</b> and <i>italic</i> text.</p>", html)
        self.assertIn("<ul>", html)
        self.assertIn("<li>Item 1</li>", html)
        self.assertIn("<li>Item 2</li>", html)
        self.assertIn("<li>Item 3</li>", html)
        self.assertIn("</ul>", html)

    # ===== PROPS EDGE CASES =====
    def test_props_with_empty_string_value(self):
        """Test property with empty string value"""
        leaf = LeafNode("b", "text")
        parent = ParentNode("p", [leaf], props={"data-empty": ""})
        self.assertIn('data-empty=""', parent.tohtml())

    def test_nested_parents_with_props_at_each_level(self):
        """Test nested parents each with different props"""
        leaf = LeafNode("span", "text")
        inner = ParentNode("div", [leaf], props={"class": "inner"})
        outer = ParentNode("section", [inner], props={"class": "outer", "id": "main"})
        
        html = outer.tohtml()
        self.assertIn('<section ', html)
        self.assertIn('class="outer"', html)
        self.assertIn('id="main"', html)
        self.assertIn('<div class="inner">', html)

    # ===== SINGLE CHILD PARENT NODES =====
    def test_single_parent_child(self):
        """Test ParentNode containing single ParentNode child"""
        leaf = LeafNode("b", "text")
        middle = ParentNode("span", [leaf])
        outer = ParentNode("p", [middle])
        self.assertEqual(outer.tohtml(), "<p><span><b>text</b></span></p>")

    # ===== SPECIAL HTML TAGS =====
    def test_self_closing_tag_leaf_node(self):
        """Test that self-closing tags work in LeafNode"""
        # Note: ParentNode doesn't directly handle self-closing, but let's test the setup
        leaf = LeafNode("br", "")  # Use empty string instead of None
        parent = ParentNode("p", [leaf])
        html = parent.tohtml()
        self.assertIn("<p><br></br></p>", html)


    def test_common_html_tags(self):
        """Test common HTML tags"""
        tags_to_test = ["div", "section", "article", "header", "footer", "main", "nav"]
        for tag in tags_to_test:
            leaf = LeafNode("span", "content")
            parent = ParentNode(tag, [leaf])
            expected = f"<{tag}><span>content</span></{tag}>"
            self.assertEqual(parent.tohtml(), expected)

if __name__ == "__main__":
    unittest.main()

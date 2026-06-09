import unittest
from textnode import TextNode, TextType,text_node_to_html_node
from markdowntotext import markdown_to_html_node, split_nodes_delimiter, text_to_textnode,extract_markdown_images,extract_markdown_links, split_nodes_image
class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    def test_uneq(self):
        node = TextNode("this is an italic node", TextType.ITALIC)
        node2 = TextNode("this is a bold node", TextType.BOLD)
        self.assertNotEqual(node, node2)
    def test_uneq2(self):
        node = TextNode("this is an italic node", TextType.ITALIC)
        node2 = TextNode("this is also an italic node", TextType.ITALIC)
        self.assertNotEqual(node, node2)
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    def test_text_no_delimiter(self):
        node = TextNode("Hello, world!", TextType.TEXT)
        result = split_nodes_delimiter([node], "*", TextType.BOLD)
        self.assertEqual(result, [node])

    def test_single_delimiter_pair(self):
        node = TextNode("This is *bold* text", TextType.TEXT)
        result = split_nodes_delimiter([node], "*", TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_multiple_delimiter_pairs(self):
        node = TextNode("a *b* c *d*", TextType.TEXT)
        result = split_nodes_delimiter([node], "*", TextType.BOLD)
        expected = [
            TextNode("a ", TextType.TEXT),
            TextNode("b", TextType.BOLD),
            TextNode(" c ", TextType.TEXT),
            TextNode("d", TextType.BOLD),
        ]
        self.assertEqual(result, expected)

    def test_non_text_node_passed_through(self):
        bold_node = TextNode("already bold", TextType.BOLD)
        result = split_nodes_delimiter([bold_node], "*", TextType.BOLD)
        self.assertEqual(result, [bold_node])

    def test_mixed_nodes(self):
        node1 = TextNode("plain text", TextType.TEXT)
        node2 = TextNode("bold", TextType.BOLD)
        node3 = TextNode("more *italic* here", TextType.TEXT)
        result = split_nodes_delimiter([node1, node2, node3], "*", TextType.ITALIC)
        expected = [
            TextNode("plain text", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode("more ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" here", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_delimiter_at_start(self):
        node = TextNode("*bold* at start", TextType.TEXT)
        result = split_nodes_delimiter([node], "*", TextType.BOLD)
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode(" at start", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_delimiter_at_end(self):
        node = TextNode("at end *bold*", TextType.TEXT)
        result = split_nodes_delimiter([node], "*", TextType.BOLD)
        expected = [
            TextNode("at end ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
        ]
        self.assertEqual(result, expected)

    def test_unmatched_delimiter_raises(self):
        node = TextNode("unmatched *bold", TextType.TEXT)
        with self.assertRaises(Exception) as cm:
            split_nodes_delimiter([node], "*", TextType.BOLD)
        self.assertIn("unmatched '*' delimiter", str(cm.exception))

    def test_empty_input_list(self):
        self.assertEqual(split_nodes_delimiter([], "*", TextType.BOLD), [])

    def test_empty_text_node(self):
        node = TextNode("", TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([node], "*", TextType.BOLD), [])

    def test_only_delimiters(self):
        node = TextNode("****", TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([node], "*", TextType.BOLD), [])

    def test_code_delimiter(self):
        node = TextNode("some `code` here", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("some ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" here", TextType.TEXT),
        ]
        self.assertEqual(result, expected)

    def test_different_text_type(self):
        node = TextNode("hello _italic_ world", TextType.TEXT)
        result = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected = [
            TextNode("hello ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" world", TextType.TEXT),
        ]
        self.assertEqual(result, expected)
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
    )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    def test_extract_markdown_images(self):
        matches = extract_markdown_links("For more information on formatting, check out the [Markdown Guide](https://www.markdownguide.org) to learn the basics.")
        self.assertListEqual([("Markdown Guide", "https://www.markdownguide.org")], matches)
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMG, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMG, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    def test_text_to_textnode_plain(self):
        # Test 1: Verifies that a simple plain text string returns a single TEXT node
        text = "Hello world, this is plain text."
        expected = [
            TextNode("Hello world, this is plain text.", TextType.TEXT)
        ]
        self.assertEqual(text_to_textnode(text), expected)

    def test_text_to_textnode_mixed(self):
        # Test 2: Verifies chained processing of multiple markdown elements
        text = "This is **bold** text with a [link](https://boot.dev) inside."
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
            # Note: adjust TextType.LINK/IMG based on your final corrected enums
            TextNode(" inside.", TextType.TEXT)
        ]
        self.assertEqual(text_to_textnode(text), expected)
    def test_multiple_block_types(self):
        md = """
# Heading

A paragraph with **bold**.

- list item one
- list item two
"""
        node = markdown_to_html_node(md)
        html = node.tohtml()
        self.assertEqual(
            html,
            "<div><h1>Heading</h1><p>A paragraph with <b>bold</b>.</p><ul><li>list item one</li><li>list item two</li></ul></div>",
        )
if __name__ == "__main__":
    unittest.main()

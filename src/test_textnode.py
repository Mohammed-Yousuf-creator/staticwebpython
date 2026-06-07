import unittest
from textnode import TextNode, TextType

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

if __name__ == "__main__":
    unittest.main()

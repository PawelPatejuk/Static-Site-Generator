import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
	def test_eq(self):
		node1 = TextNode("This is a text node", TextType.BOLD)
		node2 = TextNode("This is a text node", TextType.BOLD)
		node3 = TextNode("This is a text noed", TextType.ITALIC)
		self.assertEqual(node1, node2)
		self.assertNotEqual(node1, node3)

	def test_text(self):
		node = TextNode("This is a text node", TextType.TEXT)
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, None)
		self.assertEqual(html_node.value, "This is a text node")

	def test_bold(self):
		node = TextNode("Bold text", TextType.BOLD)
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, "b")
		self.assertEqual(html_node.value, "Bold text")
		self.assertEqual(html_node.props, None)

	def test_italic(self):
		node = TextNode("Italic text", TextType.ITALIC)
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, "i")
		self.assertEqual(html_node.value, "Italic text")
		self.assertEqual(html_node.props, None)

	def test_code(self):
		node = TextNode("Code snippet", TextType.CODE)
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, "code")
		self.assertEqual(html_node.value, "Code snippet")
		self.assertEqual(html_node.props, None)

	def test_link(self):
		node = TextNode("Click me", TextType.LINK)
		node.url = "https://example.com"
		html_node = text_node_to_html_node(node)
		self.assertEqual(html_node.tag, "a")
		self.assertEqual(html_node.value, "Click me")
		self.assertEqual(html_node.props, {"href": "https://example.com"})

	def test_image(self):
		node = TextNode("Alt text", TextType.IMAGE)


if __name__ ==  "__main__":
	unittest.main()

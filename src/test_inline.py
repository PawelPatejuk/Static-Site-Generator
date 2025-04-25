import unittest

from textnode import TextNode, TextType
from inline import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes


class TestSplitNodesDelimiter(unittest.TestCase):
	def test_simple_code_block(self):
		node = TextNode("This is text with a `code block` word", TextType.TEXT)
		new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

		self.assertEqual(len(new_nodes), 3)

		self.assertEqual(new_nodes[0].text, "This is text with a ")
		self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
		self.assertEqual(new_nodes[1].text, "code block")
		self.assertEqual(new_nodes[1].text_type, TextType.CODE)
		self.assertEqual(new_nodes[2].text, " word")
		self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

	def test_multiple_code_blocks(self):
		# Test with multiple code blocks in a single node
		node = TextNode("Code `first` text `second` more text", TextType.TEXT)
		new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

		# Check if we got 5 nodes as expected
		self.assertEqual(len(new_nodes), 5)
		# Check content and type of each node
		self.assertEqual(new_nodes[0].text, "Code ")
		self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
		self.assertEqual(new_nodes[1].text, "first")
		self.assertEqual(new_nodes[1].text_type, TextType.CODE)
		self.assertEqual(new_nodes[2].text, " text ")
		self.assertEqual(new_nodes[2].text_type, TextType.TEXT)
		self.assertEqual(new_nodes[3].text, "second")
		self.assertEqual(new_nodes[3].text_type, TextType.CODE)
		self.assertEqual(new_nodes[4].text, " more text")
		self.assertEqual(new_nodes[4].text_type, TextType.TEXT)


	def test_extract_markdown_images(self):
		matches = extract_markdown_images(
			"This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
		)
		self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

		matches = extract_markdown_images("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")
		self.assertListEqual([("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")], matches)


	def test_extract_markdown_links(self):
		matches = extract_markdown_links(
			"This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
		)
		self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

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

	def test_split_links_basic(self):
		node = TextNode(
			"This is text with a [link](https://example.com)",
			TextType.TEXT,
		)
		new_nodes = split_nodes_link([node])
		self.assertListEqual(
			[
				TextNode("This is text with a ", TextType.TEXT),
				TextNode("link", TextType.LINK, "https://example.com"),
			],
			new_nodes,
	)

	def test_split_links_multiple(self):
		node = TextNode(
			"This is text with [link one](https://example1.com) and [link two](https://example2.com)",
			TextType.TEXT,
		)
		new_nodes = split_nodes_link([node])
		self.assertListEqual(
			[
				TextNode("This is text with ", TextType.TEXT),
				TextNode("link one", TextType.LINK, "https://example1.com"),
				TextNode(" and ", TextType.TEXT),
				TextNode("link two", TextType.LINK, "https://example2.com"),
			],
			new_nodes,
	)

	def test_split_links_no_links(self):
		node = TextNode(
			"This is text with no links",
			TextType.TEXT,
		)
		new_nodes = split_nodes_link([node])
		self.assertListEqual(
			[
				TextNode("This is text with no links", TextType.TEXT),
			],
			new_nodes,
		)

	def test_split_links_empty_text(self):
		node = TextNode(
			"[link](https://example.com)",
			TextType.TEXT,
		)
		new_nodes = split_nodes_link([node])
		self.assertListEqual(
			[
				TextNode("link", TextType.LINK, "https://example.com"),
			],
			new_nodes,
		)

	def test_split_images_basic(self):
		node = TextNode(
			"This is text with an ![image](https://example.com/img.jpg)",
			TextType.TEXT,
		)
		new_nodes = split_nodes_image([node])
		self.assertListEqual(
			[
				TextNode("This is text with an ", TextType.TEXT),
				TextNode("image", TextType.IMAGE, "https://example.com/img.jpg"),
			],
			new_nodes,
		)

	def test_split_images_multiple(self):
		node = TextNode(
			"This is text with ![image one](https://example1.com/img.jpg) and ![image two](https://example2.com/img.jpg)",
			TextType.TEXT,
		)
		new_nodes = split_nodes_image([node])
		self.assertListEqual(
			[
				TextNode("This is text with ", TextType.TEXT),
				TextNode("image one", TextType.IMAGE, "https://example1.com/img.jpg"),
				TextNode(" and ", TextType.TEXT),
				TextNode("image two", TextType.IMAGE, "https://example2.com/img.jpg"),
			],
			new_nodes,
		)

	def test_split_images_no_images(self):
		node = TextNode(
			"This is text with no images",
			TextType.TEXT,
		)
		new_nodes = split_nodes_image([node])
		self.assertListEqual(
			[
				TextNode("This is text with no images", TextType.TEXT),
			],
			new_nodes,
		)

	def test_split_images_empty_text(self):
		node = TextNode(
			"![image](https://example.com/img.jpg)",
			TextType.TEXT,
		)
		new_nodes = split_nodes_image([node])
		self.assertListEqual(
			[
				TextNode("image", TextType.IMAGE, "https://example.com/img.jpg"),
			],
			new_nodes,
		)



	def test_text_to_textnodes(self):
		nodes = text_to_textnodes(
			"This is **text** with an _italic_ word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
		)
		self.assertListEqual(
			[
				TextNode("This is ", TextType.TEXT),
				TextNode("text", TextType.BOLD),
				TextNode(" with an ", TextType.TEXT),
				TextNode("italic", TextType.ITALIC),
				TextNode(" word and a ", TextType.TEXT),
				TextNode("code block", TextType.CODE),
				TextNode(" and an ", TextType.TEXT),
				TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
				TextNode(" and a ", TextType.TEXT),
				TextNode("link", TextType.LINK, "https://boot.dev"),
			],
			nodes,
	)
	def test_complex_example1(self):
		text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
		expected = [
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
		]
		result = text_to_textnodes(text)
		self.assertEqual(result, expected)

	def test_complex_example2(self):
		text = "Start with ![image](https://example.com/img.jpg) then **bold** followed by _italics_ and `code`"
		expected = [
			TextNode("Start with ", TextType.TEXT),
			TextNode("image", TextType.IMAGE, "https://example.com/img.jpg"),
			TextNode(" then ", TextType.TEXT),
			TextNode("bold", TextType.BOLD),
			TextNode(" followed by ", TextType.TEXT),
			TextNode("italics", TextType.ITALIC),
			TextNode(" and ", TextType.TEXT),
			TextNode("code", TextType.CODE),
		]
		result = text_to_textnodes(text)
		self.assertEqual(result, expected)

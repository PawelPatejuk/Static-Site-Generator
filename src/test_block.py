import unittest

from block import markdown_to_blocks, BlockType, block_to_block_type


class TestBlock(unittest.TestCase):
	def test_markdown_to_blocks(self):
		md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
		"""
		blocks = markdown_to_blocks(md)
		self.assertEqual(
			blocks,
			[
				"This is **bolded** paragraph",
				"This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
				"- This is a list\n- with items",
			],
		)

	def test_simple_blocks(self):
		md = "Block 1\n\nBlock 2\n\nBlock 3"
		blocks = markdown_to_blocks(md)
		self.assertEqual(blocks, ["Block 1", "Block 2", "Block 3"])

	def test_with_extra_newlines(self):
		md = "Block 1\n\n\n\nBlock 2\n\nBlock 3"
		blocks = markdown_to_blocks(md)
		self.assertEqual(blocks, ["Block 1", "Block 2", "Block 3"])

	def test_with_leading_trailing_whitespace(self):
		md = "  Block 1  \n\n  Block 2  "
		blocks = markdown_to_blocks(md)
		self.assertEqual(blocks, ["Block 1", "Block 2"])

	def test_empty_string(self):
		md = ""
		blocks = markdown_to_blocks(md)
		self.assertEqual(blocks, [])

	def test_heading(self):
		self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
		self.assertEqual(block_to_block_type("### Heading 3"), BlockType.HEADING)
		self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)

	def test_code_block(self):
		self.assertEqual(block_to_block_type("```python\nprint('Hello World')\n```"), BlockType.CODE)

	def test_quote_block(self):
		self.assertEqual(block_to_block_type("> This is a quote"), BlockType.QUOTE)
		self.assertEqual(block_to_block_type("> Another line of a quote"), BlockType.QUOTE)

	def test_unordered_list(self):
		self.assertEqual(block_to_block_type("- Item 1\n- Item 2 \n  - Item 3"), BlockType.UNORDERED_LIST)
		self.assertEqual(block_to_block_type("- Item 1\n- Item 3\n- Item 2"), BlockType.UNORDERED_LIST)

	def test_ordered_list(self):
		self.assertEqual(block_to_block_type("1. Item 1\n 2. Item 2\n    3. Item 3   "), BlockType.ORDERED_LIST)
		self.assertEqual(block_to_block_type("2. Item 2\n1. Item 1\n3. Item 3"), BlockType.PARAGRAPH)

	def test_paragraph(self):
		self.assertEqual(block_to_block_type("This is a normal paragraph."), BlockType.PARAGRAPH)
		self.assertEqual(block_to_block_type("Another random paragraph here."), BlockType.PARAGRAPH)

	def test_mixed_blocks(self):
		self.assertEqual(block_to_block_type("This is a normal paragraph."), BlockType.PARAGRAPH)
		self.assertEqual(block_to_block_type("### This is a heading"), BlockType.HEADING)
		self.assertEqual(block_to_block_type("```python\nprint('Hello')\n```"), BlockType.CODE)
		self.assertEqual(block_to_block_type("> This is a quote"), BlockType.QUOTE)
		self.assertEqual(block_to_block_type("- Item 1"), BlockType.UNORDERED_LIST)
		self.assertEqual(block_to_block_type("1. Item 1"), BlockType.ORDERED_LIST)

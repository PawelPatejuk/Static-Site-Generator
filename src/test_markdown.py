import unittest

from htmlnode import HTMLNode
from markdown import markdown_to_html_node


class TestMarkdown(unittest.TestCase):
	def test_paragraph_simple(self):
		md = "This is a simple paragraph."
		node = markdown_to_html_node(md)
		#print(f"\nnode: {node}")
		html = node.to_html()
		#print(f"\nhtml: {html}")
		self.assertEqual(
			html,
			"<div><p>This is a simple paragraph.</p></div>"
		)

	def test_paragraph_with_formatting(self):
		md = "This paragraph has **bold** and _italic_ formatting."
		node = markdown_to_html_node(md)
		html = node.to_html()
		self.assertEqual(
			html,
			"<div><p>This paragraph has <b>bold</b> and <i>italic</i> formatting.</p></div>"
		)

	def test_multiple_paragraphs(self):
		md = "First paragraph.\n\nSecond paragraph."
		node = markdown_to_html_node(md)
		html = node.to_html()
		self.assertEqual(
			html,
			"<div><p>First paragraph.</p><p>Second paragraph.</p></div>"
		)

	def test_heading(self):
		md = "# This is a heading"

		node = markdown_to_html_node(md)
		html = node.to_html()
		self.assertEqual(
			html,
			"<div><h1>This is a heading</h1></div>"
		)

	def test_multiple_headings(self):
		md = """
# Heading 1

## Heading 2

### Heading 3
"""

		node = markdown_to_html_node(md)
		html = node.to_html()
		self.assertEqual(
			html,
			"<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3</h3></div>"
		)

	def test_heading_with_formatting(self):
		md = "## This is a heading with **bold** and _italic_ text"

		node = markdown_to_html_node(md)
		html = node.to_html()
		self.assertEqual(
			html,
			"<div><h2>This is a heading with <b>bold</b> and <i>italic</i> text</h2></div>"
		)

	def test_basic_code_block(self):
		md = """
```
function example() {
	return "hello world";
}
```
"""
		node = markdown_to_html_node(md)
		html = node.to_html()
		self.assertEqual(html, "<div><pre><code>function example() {\n\treturn \"hello world\";\n}</code></pre></div>")

	def test_code_block_with_formatted_content(self):
		md = """
This is a **bold** paragraph.

```
def hello():
	print("Hello, world!")
```

This is a paragraph with _italic_ text.
"""

		node = markdown_to_html_node(md)
		html = node.to_html()
		self.assertEqual(html, "<div><p>This is a <b>bold</b> paragraph.</p><pre><code>def hello():\n\tprint(\"Hello, world!\")</code></pre><p>This is a paragraph with <i>italic</i> text.</p></div>")

	def test_codeblock(self):
		md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

		node = markdown_to_html_node(md)
		html = node.to_html()
		self.assertEqual(
			html,
			"<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>",
		)

	def test_quote_block(self):
		md = """> Wisdom begins in wonder"""
		node = markdown_to_html_node(md)
		html = node.to_html()
		self.assertEqual(
			html,
			"<div><blockquote>Wisdom begins in wonder</blockquote></div>",
		)
	def test_unordered_list(self):
		md = """
- Item 1
- Item 2 with **bold** text
- Item 3 with `code` in it
"""
		node = markdown_to_html_node(md)
		html = node.to_html()
		self.assertEqual(
			html,
			"<div><ul><li>Item 1</li><li>Item 2 with <b>bold</b> text</li><li>Item 3 with <code>code</code> in it</li></ul></div>"
		)

	def test_ordered_list(self):
		md = """
1. First item
2. Second item with _italic_ text
3. Third item with `code` in it
"""
		node = markdown_to_html_node(md)
		html = node.to_html()
		self.assertEqual(
			html,
			"<div><ol><li>First item</li><li>Second item with <i>italic</i> text</li><li>Third item with <code>code</code> in it</li></ol></div>"
		)

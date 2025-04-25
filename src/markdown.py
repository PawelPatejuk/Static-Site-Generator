from htmlnode import HTMLNode
from textnode import TextType, TextNode, text_node_to_html_node
from inline import text_to_textnodes
from block import BlockType, markdown_to_blocks, block_to_block_type

def markdown_to_html_node(markdown):
	parent_node = HTMLNode(tag="div", children=[])
	#print(f"Tparent_node: {parent_node}")

	blocks = markdown_to_blocks(markdown)

	for block in blocks:
		block_type = block_to_block_type(block)
		if block_type == BlockType.PARAGRAPH:
			paragraph_node = HTMLNode(tag="p", children=[])
			text_nodes = text_to_textnodes(block)
			for text_node in text_nodes:
				html_node = text_node_to_html_node(text_node)
				paragraph_node.children.append(html_node)
			parent_node.children.append(paragraph_node)
		elif block_type == BlockType.HEADING:
			heading_node = HTMLNode(tag=f'h{len(block.split(" ")[0])}', children=[])
			block = " ".join(block.split(" ")[1:])
			text_nodes = text_to_textnodes(block)
			for text_node in text_nodes:
				html_node = text_node_to_html_node(text_node)
				heading_node.children.append(html_node)
			parent_node.children.append(heading_node)
		elif block_type == BlockType.CODE:
			code_node = HTMLNode(tag="code", value=block[3:-3].strip())
			pre_node = HTMLNode(tag="pre", children=[code_node])
			parent_node.children.append(pre_node)
		elif block_type == BlockType.QUOTE:
			quote_node = HTMLNode(tag="blockquote", value=block[1:].strip(), children=[])
			parent_node.children.append(quote_node)
		elif block_type == BlockType.UNORDERED_LIST:
			unordered_list = HTMLNode(tag="ul", children=[])
			block = block.strip()
			elements = block.split("\n")
			for element in elements:
				unordered_list_element = HTMLNode(tag="li", children=[])
				text_nodes = text_to_textnodes(element[2:])
				for text_node in text_nodes:
					html_node = text_node_to_html_node(text_node)
					unordered_list_element.children.append(html_node)
				unordered_list.children.append(unordered_list_element)
			parent_node.children.append(unordered_list)
		elif block_type == BlockType.ORDERED_LIST:
			ordered_list = HTMLNode(tag="ol", children=[])
			block = block.strip()
			elements = block.split("\n")
			for element in elements:
				ordered_list_element = HTMLNode(tag="li", children=[])
				text_nodes = text_to_textnodes(". ".join(element.split(". ")[1:]))
				for text_node in text_nodes:
					html_node = text_node_to_html_node(text_node)
					ordered_list_element.children.append(html_node)
				ordered_list.children.append(ordered_list_element)
			parent_node.children.append(ordered_list)


	return parent_node

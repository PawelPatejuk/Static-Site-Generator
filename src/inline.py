import re

from textnode import TextType, TextNode


def split_nodes_delimiter(old_nodes, delimiter, text_type=TextType.TEXT):
	result = []

	for old_node in old_nodes:
		if old_node.text_type != TextType.TEXT:
			result.append(old_node)
			continue

		parts = old_node.text.split(delimiter)

		for i, part in enumerate(parts):
			if part == "":
				continue
			if i % 2 == 1:
				result.append(TextNode(part, text_type))
			else:
				result.append(TextNode(part, TextType.TEXT))


	return result


def extract_markdown_images(text):
	return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
	return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_image(old_nodes):
	result = []

	for old_node in old_nodes:
		if old_node.text_type != TextType.TEXT:
			result.append(old_node)
			continue

		text = old_node.text

		matches = extract_markdown_images(text)

		if len(matches) == 0:
			result.append(TextNode(text, TextType.TEXT))
			continue

		for match in matches:
			match_alt = match[0]
			match_link = match[1]

			parts = text.split(f"![{match_alt}]({match_link})")

			if parts[0] != "":
				result.append(TextNode(parts[0], TextType.TEXT))

			result.append(TextNode(match_alt, TextType.IMAGE, match_link))

			if parts[1] != "" and len(extract_markdown_images(parts[1])) == 0:
				result.append(TextNode(parts[1], TextType.TEXT))

			text = parts[1]

	return result


def split_nodes_link(old_nodes):
	result = []

	for old_node in old_nodes:
		if old_node.text_type != TextType.TEXT:
			result.append(old_node)
			continue

		text = old_node.text

		matches = extract_markdown_links(text)

		if len(matches) == 0:
			result.append(TextNode(text, TextType.TEXT))
			continue

		for match in matches:
			match_alt = match[0]
			match_link = match[1]

			parts = text.split(f"[{match_alt}]({match_link})")

			if parts[0] != "":
				result.append(TextNode(parts[0], TextType.TEXT))

			result.append(TextNode(match_alt, TextType.LINK, match_link))

			if parts[1] != "" and len(extract_markdown_links(parts[1])) == 0:
				result.append(TextNode(parts[1], TextType.TEXT))

			text = parts[1]

	return result

def text_to_textnodes(text):
	nodes = [TextNode(text, TextType.TEXT)]
	nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
	nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
	nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
	nodes = split_nodes_image(nodes)
	nodes = split_nodes_link(nodes)

	return nodes

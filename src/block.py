import re
from enum import Enum


class BlockType(Enum):
	PARAGRAPH = "paragraph"
	HEADING = "heading"
	CODE = "code"
	QUOTE = "quote"
	UNORDERED_LIST = "unordered_list"
	ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
	result = []

	parts =	markdown.split("\n\n")

	for part in parts:
		part = part.strip()
		if len(part) != 0:
			result.append(part)

	return result


def block_to_block_type(text):
	if re.match("^#{1,6} .+", text.strip()):
		return BlockType.HEADING
	if text[:3] == "```" and text[-3:] == "```":
		return BlockType.CODE
	if text[0] == ">":
		return BlockType.QUOTE
	if text[:2] == "- ":
		return BlockType.UNORDERED_LIST
	if text[:3] == "1. ":
		parts = text.split("\n")
		for i, part in enumerate(parts):
			if not part.strip().startswith(f"{i + 1}. "):
				return BlockType.PARAGRAPH
		return BlockType.ORDERED_LIST

	return BlockType.PARAGRAPH

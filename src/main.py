import os
import shutil

from textnode import TextNode
from markdown import markdown_to_html_node
from htmlnode import HTMLNode


def main():
	copy_files("static", "public")
	generate_page("content/index.md", "template.html", "public/index.html")


def copy_files(src_dir, dest_dir):
	if os.path.exists(dest_dir):
		shutil.rmtree(dest_dir)

	os.mkdir(dest_dir)

	for item in os.listdir(src_dir):
		src_item = os.path.join(src_dir, item)
		dest_item = os.path.join(dest_dir, item)

		if os.path.isfile(src_item):
			shutil.copy(src_item, dest_item)
		else:
			copy_files(src_item, dest_item)


def extract_title(markdown):
	for line in markdown.split("\n"):
		if line.startswith("# "):
			return line[1:].strip()

	raise Exception("heading not found")


def generate_page(from_path, template_path, dest_path):
	print(f"Generating page from {from_path} to {dest_path} using {template_path}")

	f = open(from_path, "r")
	from_content = f.read()
	f.close()

	title = extract_title(from_content)

	f = open(template_path, "r")
	template_content = f.read()
	f.close()

	node = markdown_to_html_node(from_content)
	html = node.to_html()

	new_content = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html)

	f = open(dest_path, "w")
	f.write(new_content)
	f.close()



main()

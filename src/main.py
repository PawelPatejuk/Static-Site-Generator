import os
import shutil
from pathlib import Path
import sys

from textnode import TextNode
from markdown import markdown_to_html_node
from htmlnode import HTMLNode


def main():
	basepath = "/"
	if len(sys.argv) > 1:
		basepath = sys.argv[1]
	copy_files("static", "docs")
	generate_pages_recursive("content", "template.html", "docs", basepath)


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

	print(f"\n\nmarkdown:\n{markdown}")
	raise Exception("heading not found")


def generate_page(from_path, template_path, dest_path, base_path):
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

	new_content = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html).replace('href="/', f'href="{base_path}').replace('src="/', f'src="{base_path}')

	f = open(dest_path, "w")
	f.write(new_content)
	f.close()

	print("generate_page: Done\n")

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, base_path):
	if not os.path.exists(dest_dir_path) and not os.path.isfile(dest_dir_path):
		os.mkdir(dest_dir_path)

	for item in os.listdir(dir_path_content):
		src_item = os.path.join(dir_path_content, item)
		dest_item = os.path.join(dest_dir_path, item)

		print(f"\nsrc_item: {src_item}")

		if os.path.isfile(src_item) and src_item.endswith(".md"):
			print(f"generated page: {src_item}")
			dest_item = dest_item.replace(".md", ".html")
			generate_page(src_item, template_path, dest_item, base_path)

		elif os.path.isdir(src_item):
			print(f"recursive page: {src_item}")
			generate_pages_recursive(src_item, template_path, dest_item, base_path)

	print("generate_pages_recursive: Done\n")


main()


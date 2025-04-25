import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
	def test_eq(self):
		node1 = HTMLNode("a", "hey")
		node2 = HTMLNode("a", "hey")
		node3 = HTMLNode("p", "bye")
		props1 = HTMLNode(props={" href": "https://www.google.com", "target": "_blank"})
		props2 = HTMLNode(props={" href": "https://www.google.com", "target": "_blank"})
		props3 = HTMLNode(props={" href": "https://www.github.com"})
		self.assertEqual(node1, node2)
		self.assertNotEqual(node1, node3)
		self.assertEqual(props1, props2)
		self.assertNotEqual(props1, props3)


if __name__ == "__main__":
	unittest.main()

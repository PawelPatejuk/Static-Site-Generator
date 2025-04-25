from htmlnode import HTMLNode


class LeafNode(HTMLNode):
	def __init__(self, tag, value, props=None):
		super().__init__(tag, value, None, props)


	def to_html(self):
		if self.value == None:
			raise ValueError
		if self.tag == None:
			return self.value

		result = f"<{self.tag}"
		if self.props is not None:
			for k, v in self.props.items():
				result += f" {k}=\"{v}\""

		result += f">{self.value}</{self.tag}>"

		return result

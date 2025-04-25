from htmlnode import HTMLNode


class ParentNode(HTMLNode):
	def __init__(self, tag, children, props=None):
		super().__init__(tag, None, children, props)


	def to_html(self):
		if self.tag is None:
			raise ValueError("Tag is required")
		if self.children is None:
			raise ValueError("Children list is required")

		s = f"<{self.tag}"

		if self.props is not None:
			for k, v in self.props.items():
				s += f' {k}={"v"}'

		s += ">"

		for c in self.children:
			s += c.to_html()

		s += f"</{self.tag}>"

		return s

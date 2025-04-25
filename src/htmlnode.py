class HTMLNode():
	def __init__(self, tag=None, value=None, children=None, props=None):
		self.tag = tag
		self.value = value
		self.children = children
		self.props = props


	def to_html(self):
		if self.tag == None:
			return self.value

		html = f"<{self.tag}"

		if self.props != None:
			html += self.props_to_html()

		html += ">"

		if self.value != None:
			html += self.value

		if self.children != None:
			for child in self.children:
				html += child.to_html()

		html += f"</{self.tag}>"

		return html

	def props_to_html(self):
		s = ""
		if props:
			for k, v in props.items():
				s += f' {k}="{v}"'
		return s


	def __repr__(self):
		return f"Tag: {self.tag} | Value: {self.value} | Children: {self.children} | Props: {self.props}"


	def __eq__(self, other):
		return self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props

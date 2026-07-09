class HTMLNode:
    def __init__(self, tag: str | None = None, value: str | None = None, children: list["HTMLNode"] | None = None, props: dict | None = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if self.props is None:
            return ""
        
        res = []
        for k, v in self.props.items():
            formated = f' {k}="{v}"'
            res.append(formated)

        return "".join(res)

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def __eq__(self, other: HTMLNode):
        if self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props:
            return True
        return False

class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props: dict | None = None):
        super().__init__(tag, value, None, props)

    def to_html(self): 
        if not self.value:
            raise ValueError("leaf node has no value")
        if self.tag is None:
            return self.value

        return  f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>' 

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"

# any htmlnode that has children is a parent node
class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list["HTMLNode"], props: dict | None = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("parent node has no tag")
        if self.children is None:
            raise ValueError("parent node has no children")
        
        res = []
        for child in self.children:
            r = child.to_html()
            res.append(r)

        res = "".join(res)

        return f"<{self.tag}>{res}</{self.tag}>"

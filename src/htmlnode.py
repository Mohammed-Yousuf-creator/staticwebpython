class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def tohtml(self):
        raise NotImplementedError("child class has not overriden this method")
    def props_to_html(self):
        string = ""
        if self.props is None or len(self.props) == 0:
            return string
        for prop in self.props:
            string += f" {prop}=\"{self.props[prop]}\""
        return string
    def __repr__(self):
        return f"<{self.tag} {self.props_to_html()} children={self.children}></{self.tag}>"
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    def tohtml(self):
        if self.tag is None:
            raise ValueError("cannot nest an element with no tag")
        if self.children is None or len(self.children) == 0:
            raise ValueError("cannot nest any elements because there are no children")
        children_html = ""
        for child in self.children:
            children_html += child.tohtml()
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
    def tohtml(self):
        if self.value is None:
            raise ValueError("there is no value to render")
        if self.tag is None:
            return self.value    
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    def __repr__(self):
        return f"<{self.tag} {self.props_to_html()}>{self.value}</{self.tag}>"
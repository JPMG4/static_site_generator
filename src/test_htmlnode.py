import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_multiple(self):
        assert HTMLNode(props={"class": "my-class", "id": "my-id"}).props_to_html() == ' class="my-class" id="my-id"'
        

    def test_leaf_to_html_p(self):
        assert LeafNode("p", "Hello, World!").to_html() == "<p>Hello, World!</p>"  
        
    def test_leaf_to_html_div_with_props(self):
        assert LeafNode("a", "Content", props={"href": "my-div"}).to_html() == '<a href="my-div">Content</a>'

    def test_leaf_to_html_no_tag(self):
        assert LeafNode(None, "Just text").to_html() == "Just text"
    
    def test_leaf_to_html_no_value(self):
        with self.assertRaises(ValueError):
            LeafNode("p", None).to_html()

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_no_tag(self):
        with self.assertRaises(ValueError):
            ParentNode(None, [LeafNode("span", "child")]).to_html()

    def test_to_html_no_children(self):
        with self.assertRaises(ValueError):
            ParentNode("div", None).to_html()

if __name__ == "__main__":
    unittest.main()
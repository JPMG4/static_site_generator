import unittest

import inline_markdown
from textnode import TextNode, TextType

class TestInlineMarkdown(unittest.TestCase):
    def test_split_nodes_delimiter(self):
        old_nodes = [TextNode("This is a *bold* text", TextType.TEXT)]
        new_nodes = inline_markdown.split_nodes_delimiter(old_nodes, "*", TextType.BOLD)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0], TextNode("This is a ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("bold", TextType.BOLD))
        self.assertEqual(new_nodes[2], TextNode(" text", TextType.TEXT))

    def test_split_nodes_delimiter_unclosed(self):
        old_nodes = [TextNode("This is a *bold text", TextType.TEXT)]
        with self.assertRaises(ValueError):
            inline_markdown.split_nodes_delimiter(old_nodes, "*", TextType.BOLD)
    
    def test_extract_markdown_images(self):
        text = "Here is an image: ![alt text](image.jpg)"
        images = inline_markdown.extract_markdown_images(text)
        self.assertEqual(len(images), 1)
        self.assertEqual(images[0], ("alt text", "image.jpg"))

    def test_extract_markdown_links(self):
        text = "Here is a link: [link text](https://example.com)"
        links = inline_markdown.extract_markdown_links(text)
        self.assertEqual(len(links), 1)
        self.assertEqual(links[0], ("link text", "https://example.com"))
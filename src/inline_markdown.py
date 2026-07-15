"""
Splits TextNode objects by markdown delimiters like ** and `. Use regex to split links and images
"""
from textnode import TextType, TextNode
import re

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    # TextNode structure = (text, text_type, url)
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(TextNode(node.text, node.text_type, node.url))
            continue

        # if split returns an even amount of items, there is not a closing delimiter
        new_text = node.text.split(delimiter)
        if len(new_text) % 2 == 0:
            raise Exception("Invalid Markdown syntax. No closing delimiter")

        for i in range(len(new_text)):
            if i % 2 != 0:
                new_nodes.append(TextNode(new_text[i], text_type))
            else:
                if new_text[i] == "":
                    continue
                else:
                    new_nodes.append(TextNode(new_text[i], TextType.TEXT))
   
    return new_nodes

def extract_markdown_images(text):
    list_of_tuples = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return list_of_tuples


def extract_markdown_links(text):
    list_of_tuples = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return list_of_tuples



"""
Splits TextNode objects by markdown delimiters like ** and `. Use regex to split links and images.
Splits raw markdown text into TextNodes based on images and links.
Top function puts all the splitting functions together
"""
from textnode import TextType, TextNode
import re

def text_to_textnodes(text: str) -> list[TextNode]:
    new_nodes = []
    curr_text = TextNode(text, TextType.TEXT)

    bold_delimiter_split = split_nodes_delimiter([curr_text], "**", TextType.BOLD)
    italic_delimiter_split = split_nodes_delimiter(bold_delimiter_split, "_", TextType.ITALIC)
    code_delimiter_split = split_nodes_delimiter(italic_delimiter_split, "`", TextType.CODE)
    image_delimiter_split = split_nodes_image(code_delimiter_split)
    link_delimiter_split = split_nodes_link(image_delimiter_split)

    return link_delimiter_split

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

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    # TextNode structure = (text, text_type, url)
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(TextNode(node.text, node.text_type, node.url))
            continue

        # make a list of images inside text 
        images = extract_markdown_images(node.text)
        if images == []:
            new_nodes.append(TextNode(node.text, node.text_type, node.url))
            continue
        
        # need to split the node.text on each tuple pair in images
        curr_text = node.text
        for image in images:
            image_alt, image_link = image[0], image[1]
            sections = curr_text.split(f"![{image_alt}]({image_link})", 1)
            
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
            curr_text = sections[1]
            
        if curr_text != "":
            new_nodes.append(TextNode(curr_text, TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    # TextNode structure = (text, text_type, url)
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(TextNode(node.text, node.text_type, node.url))
            continue

        # make a list of links inside text 
        links = extract_markdown_links(node.text)
        if links == []:
            new_nodes.append(TextNode(node.text, node.text_type, node.url))
            continue
        
        # need to split the node.text on each tuple pair in links
        curr_text = node.text
        for link in links:
            link_alt, link_url = link[0], link[1]
            sections = curr_text.split(f"[{link_alt}]({link_url})", 1)
            
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link_alt, TextType.LINK, link_url))
            curr_text = sections[1]
            
        if curr_text != "":
            new_nodes.append(TextNode(curr_text, TextType.TEXT))

    return new_nodes

def extract_markdown_images(text):
    list_of_tuples = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return list_of_tuples

def extract_markdown_links(text):
    list_of_tuples = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return list_of_tuples



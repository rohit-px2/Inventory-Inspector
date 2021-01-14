# Contains some functions to parse HTML which I need.
# Created to prevent code from being too cluttered in sc_window.py (functions outside of class, functions defined before constants
# makes it more messy to read)

def get_closing_tag(tag: str) -> str:
    ''' Returns the closing tag from a corresponding tag.\n
    The tag must be a valid HTML tag.'''
    # To get the name we remove any parameters and remove the forward angle bracket (first char)
    tag_name = tag.split(" ")[0][1:]
    # tag_name may end with ">" if there are no spaces (e.g. <p>)
    return "</" + tag_name if tag_name.endswith(">") else "</" + tag_name + ">"

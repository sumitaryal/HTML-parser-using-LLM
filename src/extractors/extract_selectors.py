from bs4 import BeautifulSoup
from lxml import etree
from pprint import pprint
from src.extractors.extract_attributes import ExtractAttributes
from src.utils.utils import CheckHTMLContent, CleanHTML

class ExtractSelectors:
    """
    ExtractSelectors is a class designed to extract CSS selectors and XPaths for given attributes
    from HTML content. It utilizes BeautifulSoup for CSS selectors and lxml for XPaths.
    """

    def __init__(self, html_content, attributes):
        """
        Initializes the ExtractSelectors class with the provided HTML content and attributes.
        
        Args:
            html_content (str): The HTML content from which to extract selectors.
            attributes (dict): The attributes for which to extract selectors.
        """
        self.html_content = html_content
        self.attributes = attributes
        self.soup = BeautifulSoup(html_content, 'html.parser')
        self.tree = etree.HTML(html_content)

    def get_css_selector(self, element):
        """
        Generates a CSS selector for a given BeautifulSoup element.
        
        Args:
            element (bs4.element.Tag): The BeautifulSoup element for which to generate a CSS selector.
        
        Returns:
            str: The CSS selector for the given element.
        """
        components = []
        while element.parent is not None:
            siblings = element.parent.find_all(element.name, recursive=False)
            if len(siblings) > 1:
                components.append(f'{element.name}:nth-of-type({siblings.index(element) + 1})')
            else:
                components.append(element.name)
            element = element.parent
        components.reverse()
        return " > ".join(filter(None, components))

    def get_xpath(self, element):
        """
        Generates an XPath for a given lxml element.
        
        Args:
            element (lxml.etree.Element): The lxml element for which to generate an XPath.
        
        Returns:
            str: The XPath for the given element.
        """
        path = []
        while element is not None:
            siblings = list(element.itersiblings(preceding=True))
            index = len(siblings) + 1
            tag = element.tag
            if tag is not None:
                path.append(f"{tag}[{index}]")
            element = element.getparent()
        path.reverse()
        return '/' + '/'.join(filter(None, path))

    def extract_selectors(self):
        """
        Extracts CSS selectors and XPaths for the provided attributes from the HTML content.
        
        Returns:
            dict: A dictionary containing the CSS selectors and XPaths for each attribute.
        """
        selectors = {}
        for key, value in self.attributes.items():
            if value != "None":
                if isinstance(value, list):
                    selectors[key] = []
                    for item in value:
                        element = self.soup.find(lambda tag: tag.has_attr('src') and tag['src'] == item)
                        if element:
                            css_selector = self.get_css_selector(element)
                            xpath_elements = self.tree.xpath(f"//*[@src='{item}']")
                            if xpath_elements:
                                xpath = self.get_xpath(xpath_elements[0])
                            else:
                                xpath = "inferred"
                            selectors[key].append({"css_selector": css_selector, "xpath": xpath})
                        else:
                            selectors[key].append({"css_selector": "No CSS Selector Found", "xpath": "No XPath Found"})
                else:
                    element = self.soup.find(string=value)
                    if element:
                        css_selector = self.get_css_selector(element)
                        xpath_elements = self.tree.xpath(f"//*[text()='{value}']")
                        if xpath_elements:
                            xpath = self.get_xpath(xpath_elements[0])
                        else:
                            xpath = "inferred"
                        selectors[key] = {"css_selector": css_selector, "xpath": xpath}
                    else:
                        selectors[key] = {"css_selector": "No CSS Selector Found", "xpath": "No XPath Found"}
            else:
                selectors[key] = {"css_selector": "Not Found", "xpath": "Not Found"}
        return selectors

def main():
    """
    Main function to read HTML content from a file, extract e-commerce attributes, and then extract
    CSS selectors and XPaths for those attributes.
    """
    with open("./data/sample_1.html", "r") as file:
        html_content = file.read()
    
    # Check if the content is valid HTML
    if not CheckHTMLContent(html_content).is_html:
        print("The provided content is not HTML")
        return
    
    # Clean the HTML content
    html_content = CleanHTML(html_content).cleaned_html

    attribute_extractor = ExtractAttributes(html_content)
    attributes = attribute_extractor.get_response().choices[0].message.tool_calls[0].function.arguments

    selector_extractor = ExtractSelectors(html_content, attributes)
    print("Extracting selectors from the HTML content...")
    try:
        selectors = selector_extractor.extract_selectors()
        pprint(selectors)
    except Exception as e:
        print("An error occurred while extracting selectors from the HTML content")
        print(e)

if __name__ == "__main__":
    main()
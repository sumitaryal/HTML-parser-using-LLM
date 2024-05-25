from bs4 import BeautifulSoup
import re

class MergeAttributesAndSelectors:
    """
    MergeAttributesAndSelectors is a class designed to merge extracted e-commerce attributes
    with their corresponding CSS selectors and XPaths.
    """

    def __init__(self, attributes, selectors):
        """
        Initializes the MergeAttributesAndSelectors class with the provided attributes and selectors.
        
        Args:
            attributes (dict): The extracted attributes of the e-commerce product.
            selectors (dict): The corresponding CSS selectors and XPaths for the attributes.
        """
        self.attributes = attributes
        self.selectors = selectors
        self.result = self.merge_attributes_and_selectors()

    def merge_attributes_and_selectors(self):
        """
        Merges the attributes with their corresponding CSS selectors and XPaths.
        
        Returns:
            dict: A dictionary where each attribute is merged with its selectors.
        """
        result = {}
        for key, value in self.attributes.items():
            if isinstance(value, list):
                result[key] = []
                for index, item in enumerate(value):
                    if self.selectors[key][index]:
                        result[key].append({
                            'value': item,
                            'selectors': self.selectors[key][index]
                        })
                    else:
                        result[key].append({
                            'value': item,
                            'selectors': None
                        })
            else:
                if key in self.selectors:
                    result[key] = {
                        'value': value,
                        'selectors': self.selectors[key]
                    }
                else:
                    result[key] = {
                        'value': value,
                        'selectors': None
                    }
        return result

class CheckHTMLContent:
    """
    CheckHTMLContent is a class designed to verify if the provided content is valid HTML.
    """

    def __init__(self, html_content):
        """
        Initializes the CheckHTMLContent class with the provided HTML content.
        
        Args:
            html_content (str): The HTML content to be verified.
        """
        self.html_content = html_content
        self.is_html = self.is_html_content()

    def is_html_content(self):
        """
        Checks if the provided content is valid HTML.
        
        Returns:
            bool: True if the content is valid HTML, False otherwise.
        """
        pattern = r"<(\"[^\"]*\"|'[^']*'|[^'\">])*>"

        if not self.html_content:
            return False

        if re.match(pattern, self.html_content):
            return True
        else:
            return False
        

class CleanHTML:
    """
    CleanHTML is a class designed to clean HTML content by removing scripts, styles, anchor, svg elements, style attributes, and unnecessary tags.
    """

    def __init__(self, html_content):
        """
        Initializes the CleanHTML class with the provided HTML content.

        Args:
        html_content (str): The raw HTML content.
        """
        self.html_content = html_content
        self.cleaned_html = self.clean_html()

    def clean_html(self):
        """
        Clean HTML content by removing scripts, styles, anchor, svg elements, style attributes, and unnecessary tags.

        Args:
        html_content (str): The raw HTML content.

        Returns:
        str: The cleaned HTML content.
        """

        # Parse the HTML content
        soup = BeautifulSoup(self.html_content, 'html.parser')

        # Remove script, style, a, i and svg elements
        for tag in soup(['script', 'style', 'a', 'svg']):
            tag.decompose()

        # Remove style attributes from all tags
        for tag in soup.find_all(True):
            del tag['style']
        
        # Remove unnecessary tags but keep their contents
        for tag in soup.find_all(['div', 'span', 'header', 'footer', 'nav', 'aside', 'form', 'iframe', 'noscript', 'input', 'textarea', 'button', 'ul']):
            tag.unwrap()

        return soup
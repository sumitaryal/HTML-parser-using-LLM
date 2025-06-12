from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os
from pprint import pprint
from src.utils.utils import CheckHTMLContent, CleanHTML

class ExtractAttributes:
    """
    ExtractAttributes is a class designed to extract e-commerce attributes from HTML content.
    It utilizes a language model from Hugging Face's Inference API to parse and analyze HTML content,
    extracting relevant product details such as name, price, description, images, category, and brand.
    """

    def __init__(self, html_content):
        """
        Initializes the ExtractAttributes class with the provided HTML content.
        
        Args:
            html_content (str): The HTML content from which to extract product attributes.
        """
        # Load environment variables
        load_dotenv()
        self.HF_TOKEN = os.getenv("HF_TOKEN")
        self.html_content = html_content
        self.model_id = "meta-llama/Llama-3.1-8B-Instruct"
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "extract_ecommerce_attributes",
                    "description": "Extract e-commerce attributes from HTML content",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "product_name": {
                                "type": "string",
                                "description": "The name of the product"
                            },
                            "product_price": {
                                "type": "string",
                                "description": "The price of the product"
                            },
                            "product_description": {
                                "type": "string",
                                "description": "The description of the product"
                            },
                            "product_images": {
                                "type": "array",
                                "items": {
                                    "type": "string"
                                },
                                "description": "The URLs of the images of the product"
                            },
                            "product_category": {
                                "type": "string",
                                "description": "The category in which the product falls into"
                            },
                            "brand_name": {
                                "type": "string",
                                "description": "The name of the brand which produced the product"
                            }
                        },
                        "required": ["product_name", "product_price", "product_description", "product_images", "product_category", "brand_name"]
                    }
                }
            }
        ]
        self.client = self.get_client()
        self.messages = self.setup_messages()

    def get_client(self):
        """
        Initializes the InferenceClient with the specified model ID and token.
        
        Returns:
            InferenceClient: An instance of the InferenceClient configured with the model and token.
        """
        return InferenceClient(
            model=self.model_id,
            timeout=120,
            token=self.HF_TOKEN
        )

    def setup_messages(self):
        """
        Sets up the messages to be sent to the language model, including system instructions and user input.
        
        Returns:
            list: A list of message dictionaries containing the roles and content for the language model.
        """
        return [
            {
                "role": "system",
                "content": "You are an expert in analyzing and parsing HTML content. \
                            Your expertise lies in identifying and extracting meaningful attributes relevant to e-commerce contexts.\
                            You should be able to extract attributes such as product name, product price, product description, \
                            product images, product category, brand name, etc. from the HTML content. \
                            If the attribute is present, it should be extracted  as it is without any modification. \
                            If product description is missing, generate description of the product by inferring from other attributes. \
                            The description should be meaningful and relevant to the product. \
                            If product category is missing, infer it from other attributes. \
                            If brand name is missing, try to generate brand name from the product name. \
                            If attributes cannot be generated or inferred then generate 'None' for the missing attributes.",
            },
            {
                "role": "user",
                "content": f"Analyze and parse the following HTML content to extract the different attributes {self.html_content}",
            },
        ]

    def get_response(self):
        """
        Sends a request to the language model to analyze and parse the HTML content and extract e-commerce attributes.
        
        Returns:
            dict: The response from the language model containing the extracted attributes.
        
        Raises:
            Exception: If an error occurs during the request to the language model.
        """
        try:
            return self.client.chat_completion(
                model=self.model_id,
                messages=self.messages,
                tools=self.tools,
                tool_choice="auto",
                max_tokens=1000,
                temperature=0.0,
                top_p=0.9,
            )
        except Exception as e:
            raise Exception(f"An error occurred while extracting attributes from the HTML content: {str(e)}")

def main():
    """
    Main function to read HTML content from a file, create an instance of ExtractAttributes, and extract e-commerce attributes.
    """
    with open("./data/sample_1.html", "r") as file:
        html_content = file.read()
    
    # Check if the content is valid HTML
    if not CheckHTMLContent(html_content).is_html:
        print("The provided content is not HTML")
        return
    
    # Clean the HTML content
    html_content = CleanHTML(html_content).cleaned_html

    extractor = ExtractAttributes(html_content)
    print("Extracting attributes from the HTML content...")
    try:
        response = extractor.get_response()
        pprint(response.choices[0].message.tool_calls[0].function.arguments)
    except Exception as e:
        print("An error occurred while extracting attributes from the HTML content")
        print(e)

if __name__ == "__main__":
    main()
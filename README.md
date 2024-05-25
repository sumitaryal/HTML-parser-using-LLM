# HTML-parser-using-LLM

## Overview
This repository provides an API for extracting e-commerce attributes from HTML content. It utilizes a LLM from Hugging Face's Inference API to parse and analyze HTML content, extracting relevant product details to e-commerce contexts such as name, price, description, images, category, and brand.

## Choice of LLM and Rationale
The chosen LLM is `meta-llama/Meta-Llama-3-8B-Instruct` from Hugging Face's Inference API. This model is selected because of its strong performance in natural language understanding and generation taks, and as it is available for open-source use cases. Further this variant of Llama-3 model is fine-tuned to follow instructions accurately so it is well-suited for extracting structured data from HTML content, making it a good choice for e-commerce attribute extraction.  The context window of `Meta-Llama-3-8B-Instruct` is 8192 tokens which is an important factor of an LLM, so to take the adavantage of this context window, the HTML content is cleaned by removing scripts, styles, anchor, svg elements, style attributes, and unnecessary tags reducing the content size and saving the tokens for the actual content.

## Directory Structure
The repository is organized as follows:
- `src`: Contains the source code for the API.
- `data`: Contains sample HTML files for testing the API.
- `Dockerfile`: Contains the Docker configuration for building the project as a Docker image.
- `requirements.txt`: Contains the Python dependencies required for the project.
- `README.md`: Contains the documentation for the whole project.
- `src/api/main.py`: Contains the FastAPI code for the API endpoint.
- `src/extractors/extarct_attributes.py`: Contains the code for extracting attributes from HTML content.
- `src/extractors/extract_selectors.py`: Contains the code for extracting CSS selectors and XPaths from HTML content.
- `src/utils/utils.py`: Contains utility functions for the API such as HTML cleaning, and validation and response formatting.

## API Documentation
```python
@app.post("/extract-attributes-and-selectors/")
async def extract_attributes_and_selectors(request: Request):
    """
    Endpoint to extract e-commerce attributes and their corresponding CSS selectors and XPaths from HTML content.
    
    Args:
        request (Request): The incoming HTTP request containing the HTML content.
    
    Returns:
        JSON: A JSON object containing the extracted attributes and their corresponding CSS selectors and XPaths.
    
    Raises:
        HTTPException: If the provided content is not valid HTML or if there is an error during attribute extraction or any other exception.
    """
```

## API Workflow
 * The API is built using FastAPI.
 * The API has a single endpoint `/extract-attributes-and-selectors`.
 * The request body should contain the HTML content to be analyzed.
 * The HTML content is first validated to ensure it is a valid HTML document. If not, an HTTPException is raised.
 * The HTML is cleaned by removing scripts, styles, anchor, svg elements, style attributes, and unnecessary tags.
 * The HTML content is then passed to the LLM for attribute extraction.
 * The CSS selectors and XPaths corresponding to the extracted attributes are extracted from the HTML content.
 * The extracted attributes and their corresponding CSS selectors and XPaths are returned as a JSON object.
/**

## Setting Up
1. Clone the repository:
    ```bash
    git clone https://github.com/sumitaryal/HTML-parser-LLM.git
    ```

2. Set up environment variables:

    Create a .env file in the project root directory based on the .envexample file and fill in the necessary HuggingFace API key. 
    
    The HuggingFace API key should be write type key.

3. Build and run the API using Docker or locally:
   
- Dockerized Approach: 
    ```bash
    docker build -t html-parser-llm .
    docker run -p 8000:8000 html-parser-llm
    ```

- Local Approach:
    ```bash
    python -m venv <env_name>
    source <env_name>/bin/activate
    pip install -r requirements.txt
    uvicorn src.api.main:app --host 0.0.0.0 --port 8000
    ```

4. The API will be running at `http://localhost:8000`.

## Usage
1. Python script to extract attributes and selectors from HTML content:
    ```python
    import requests
    
    with open("data/sample_1.html", "r") as file:
        html_content = file.read()
    
    response = requests.post("http://localhost:8000/extract-attributes-and-selectors/", headers={"Content-Type": "text/html"}, data=html_content)
    print(response.json())
    ```

2. Using POSTMAN:
- Set the request type to POST.
- Set the request URL to `http://localhost:8000/extract-attributes-and-selectors/`.
- Set the request body to `raw` and the content type to `html`.
- Set the body content to the HTML content to be analyzed.
- Send the request and view the extracted attributes and selectors in the response.
- The response will be a JSON object containing the extracted attributes and their corresponding CSS selectors and XPaths.

3. Using CURL:
Open a terminal in the project root directory and run the following command:
    ```bash
    curl -X 'POST' \
      'http://localhost:8000/extract-attributes-and-selectors/' \
      -H 'Content-Type: text/html' \
      -d @data/sample_1.html
    ```

## Examples of Input HTML blocks and the corresponding JSON outputs
HTML Block:
```html
<div class="product">
    <h2 class="product-name">Product Name</h2>
    <p class="product-description">Product Description</p>
    <span class="product-price">Rs. 100</span>
    <img src="product_image.jpg" alt="Product Image">
</div>
```

JSON Output:
```json
{
    "brand_name": {
        "value": "None",
        "selectors": {
            "css_selector": "Not Found",
            "xpath": "Not Found"
        }
    },
    "product_category": {
        "value": "None",
        "selectors": {
            "css_selector": "Not Found",
            "xpath": "Not Found"
        }
    },
    "product_description": {
        "value": "Product Description",
        "selectors": {
            "css_selector": "div > p",
            "xpath": "/html[1]/body[1]/div[1]/p[2]"
        }
    },
    "product_images": [
        {
            "value": "product_image.jpg",
            "selectors": {
                "css_selector": "div > img",
                "xpath": "/html[1]/body[1]/div[1]/img[4]"
            }
        }
    ],
    "product_name": {
        "value": "Product Name",
        "selectors": {
            "css_selector": "div > h2",
            "xpath": "/html[1]/body[1]/div[1]/h2[1]"
        }
    },
    "product_price": {
        "value": "Rs. 100",
        "selectors": {
            "css_selector": "div > span",
            "xpath": "/html[1]/body[1]/div[1]/span[3]"
        }
    }
}
```

The `data` directory contains sample HTML files that can be used for testing the API. The samples are taken from daraz.com.np, an e-commerce website in Nepal.

Contents of data/

- sample_1.html: [Link to product page](https://www.daraz.com.np/products/didian-compressed-high-energy-biscuit-strawberry-milk-flavor-300-gm-15-gm-x-20-packs-i127897228-s1034908129.html?spm=a2a0e.11779170.just4u.252.49132d2bLoQA1I&scm=1007.28811.376629.0&pvid=71dcd380-a254-43b4-a0a0-b5040193bed5&clickTrackInfo=pvid:71dcd380-a254-43b4-a0a0-b5040193bed5;channel_id:0000;mt:hot;item_id:127897228;)
- sample_2.html: [Link to product page](https://www.daraz.com.np/products/cadeve-9122-rainbow-backlit-waterproof-multimedia-mechanical-gaming-keyboard-and-mouse-i102969260-s1023705840.html?spm=a2a0e.11779170.just4u.198.49132d2bLoQA1I&scm=1007.28811.376629.0&pvid=0b322174-e0da-4074-a7ee-310ba924bc6d&clickTrackInfo=pvid:0b322174-e0da-4074-a7ee-310ba924bc6d;channel_id:0000;mt:hot;item_id:102969260;)
- sample_3.html [Link to product page](https://www.daraz.com.np/products/redmi-buds-4-active-earbud-30-hrs-ultra-battery-life-bluetooth-53-google-fast-pair-i127913639-s1034928636.html?spm=a2a0e.searchlist.sku.1.624d4749o8dCwV&search=1)

The `results` directory contains the JSON outputs for the sample HTML files.
- sample_1_result.json
- sample_2_result.json
- sample_3_result.json
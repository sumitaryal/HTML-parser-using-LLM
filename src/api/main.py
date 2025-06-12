import json

from fastapi import FastAPI, HTTPException, Request
from src.extractors.extract_attributes import ExtractAttributes
from src.extractors.extract_selectors import ExtractSelectors
from src.utils.utils import MergeAttributesAndSelectors, CheckHTMLContent, CleanHTML
import uvicorn

app = FastAPI()

@app.post("/extract-attributes-and-selectors/")
async def extract_attributes_and_selectors(request: Request):
    """
    Endpoint to extract e-commerce attributes and their corresponding CSS selectors and XPaths from HTML content.
    
    Args:
        request (Request): The incoming HTTP request containing the HTML content.
    
    Returns:
        dict: A dictionary containing the extracted attributes and their corresponding selectors.
    
    Raises:
        HTTPException: If the provided content is not valid HTML or if there is an error during attribute extraction or any other exception.
    """
    try:
        # Read and decode the HTML content from the request body
        html_content = await request.body()
        html_content = html_content.decode("utf-8")
        
        # Check if the content is valid HTML
        if not CheckHTMLContent(html_content).is_html:
            raise HTTPException(status_code=400, detail="The provided content is not HTML")
        
        cleaned_html_content = CleanHTML(html_content).cleaned_html

        # Extract attributes using the ExtractAttributes class
        attribute_extractor = ExtractAttributes(cleaned_html_content)
        try:
            response = attribute_extractor.get_response()
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))
        
        # Extract selectors using the ExtractSelectors class
        attributes = response.choices[0].message.tool_calls[0].function.arguments
        attributes = json.loads(attributes) if isinstance(attributes, str) else attributes
        selectors = ExtractSelectors(html_content, attributes).extract_selectors()
        
        # Merge attributes and selectors
        result = MergeAttributesAndSelectors(attributes, selectors).result
        return result
    
    except HTTPException as e:
        # Raise HTTPException for known errors
        raise e
    
    except Exception as e:
        # Catch all other exceptions and raise a 500 HTTPException
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    """
    Main entry point for the FastAPI application. Runs the app on localhost.
    """
    uvicorn.run(app, host="127.0.0.1", port=8000)
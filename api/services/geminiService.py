import os
import re
from typing import Optional, Tuple, List
from google import genai
from google.genai.types import Tool, GenerateContentConfig, GoogleSearch
from .ai import AIService
from dotenv import load_dotenv

load_dotenv()

class GeminiService(AIService):
    def __init__(self):
        pass

    def get_price(self, book_name: str, format_type: Optional[str] = None) -> Tuple[Optional[float], List[str]]:
        client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
        model_id = "gemini-2.0-flash"

        google_search_tool = Tool(
            google_search = GoogleSearch()
        )
        
        book_format = format_type if format_type else "hardcover"
        
        prompt = f"""
        I need the price of the {book_format} edition of '{book_name}'. 
        Provide the euro price as a single floating-point number ONLY in a codeblock like this:
        ```
        25.99
        ```
        If the price cannot be determined from the sources, respond with 'N/A'. Please make sure the price is the current avaible price that you can find in the Sources below.
        Also add a List of all sources in square brackets at the end of the response.
        Each source should be separated by a comma. The source itself should be a DIRECT link to the ACTUAL website where the price was found, with NO placeholder text like 'example'.
        The sources should be reliable and well-known online bookstores. Remember to ONLY check for {book_format} books, no audio, e books or paperbacks.
        At best check multiple sources, and then average out the price or take the median price. ONLY GIVE ME THE FINAL PRICE AND THE ACTUAL SOURCE LINKS IN A LIST.
        Do not include any other text or explanation. When asked for a book, only check for the book alone, not bundles or sets.

        Sources to check:
        - Barnes & Noble
        - Book Depository
        - Thalia
        - Amazon
        """

        try:
            response = client.models.generate_content(
                model=model_id,
                contents=prompt,
                config=GenerateContentConfig(
                    tools=[google_search_tool],
                    response_modalities=["TEXT"],
                )
            )

            response_text = ""
            for part in response.candidates[0].content.parts:
                response_text += part.text
                
            print(response_text)
                
            # Extract price from the response using regex to find content in code blocks
            price_match = re.search(r'```(?:\w*)\n(.*?)\n```', response_text, re.DOTALL)
            
            if price_match:
                price_str = price_match.group(1).strip()
            else:
                # Try to find a plain number in the response if no code block is found
                price_str = response_text.strip()
            
            # Extract sources from square brackets
            sources = []
            sources_match = re.search(r'\[(.*?)\]', response_text, re.DOTALL)
            if sources_match:
                sources_str = sources_match.group(1).strip()
                # Split by comma and clean up the sources
                raw_sources = [source.strip() for source in sources_str.split(',')]
                
                # Filter out placeholder sources that contain "example"
                sources = [source for source in raw_sources if "example" not in source.lower()]
                
                # If no valid sources were found, add a generic source
                if not sources:
                    sources = ["Search results aggregated from online bookstores"]
            
            price = None
            if price_str.upper() != "N/A":
                try:
                    # Find the first floating point number in the response
                    number_match = re.search(r'(\d+(?:\.\d+)?)', price_str)
                    if number_match:
                        price = round(float(number_match.group(1)))
                    else:
                        print(f"No numeric price found in: {price_str}")
                except ValueError:
                    print(f"Could not convert price string to float: {price_str}")
                    
            return price, sources
            
        except Exception as e:
            print(f"Error in Gemini API call: {str(e)}")
            return None, ["Error occurred during Gemini API call"]
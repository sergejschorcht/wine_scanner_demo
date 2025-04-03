import os
import re
from typing import Optional, Tuple, List
from openai import OpenAI
from .ai import AIService
from dotenv import load_dotenv

load_dotenv()

class OpenAIService(AIService):
    def __init__(self):
        pass

    def get_price(self, book_name: str, format_type: Optional[str] = None) -> Tuple[Optional[float], List[str]]:
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        book_format = format_type if format_type else "hardcover"
        
        prompt = f"""
        I need the average price of the {book_format} edition of '{book_name}'. 
        Provide the final average price as a single floating-point number ONLY in a codeblock like this:
        ```
        25.99
        ```
        If the price cannot be determined from the sources, respond with 'N/A'. 
        Also add a List of all sources in square brackets at the end of the response like this:
        [https://www.amazon.com/example, https://www.barnesandnoble.com/example]
        Each source should be separated by a comma. The source itself should be a link to the website where the price was found.
        The sources should be reliable and well-known online bookstores. Remember to ONLY check for {book_format} books, no audio, e books or other formats.
        At best check multiple sources, and then average out the price or take the median price.

        Sources to check:
        - Barnes & Noble
        - Book Depository
        - Thalia
        - Amazon
        """
        response = client.responses.create(
            model="gpt-4o-mini",
            tools=[{"type": "web_search_preview"}],
            input=prompt
        )

        print(response.output_text)

        # Extract price from the response using regex to find content in code blocks
        price_match = re.search(r'```(?:\w*)\n(.*?)\n```', response.output_text, re.DOTALL)
        
        if price_match:
            price_str = price_match.group(1).strip()
        else:
            # Try to find a plain number in the response if no code block is found
            price_str = response.output_text.strip()
        
        # Extract sources from square brackets
        sources = []
        sources_match = re.search(r'\[(.*?)\]', response.output_text, re.DOTALL)
        if sources_match:
            sources_str = sources_match.group(1).strip()
            # Split by comma and clean up the sources
            sources = [source.strip() for source in sources_str.split(',')]
        
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


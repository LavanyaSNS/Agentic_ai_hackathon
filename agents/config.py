import os
from dotenv import load_dotenv 
load_dotenv() 


# Access the keys
OPENAI_API_KEY = os.getenv("OPEN_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")
together_api = os.getenv("TOGETHER_API")
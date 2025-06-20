import os
from dotenv import load_dotenv 
load_dotenv() 


# Access the keys
OPENAI_API_KEY = os.getenv("OPEN_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")
TOGETHER_API = os.getenv("TOGETHER_API")
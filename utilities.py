import json 
from langchain_community.chat_models import ChatOpenAI 
from dotenv import load_dotenv
import os

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
 
def to_obj(s):
    try:
        return json.loads(s)
    except Exception:
        return {}

def get_llm():
    return ChatOpenAI(
        openai_api_key=OPENAI_API_KEY,
        model_name="gpt-4o-mini"
    )
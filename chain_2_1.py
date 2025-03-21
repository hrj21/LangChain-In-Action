from utilities import to_obj, get_llm

from prompts import (
    WEB_SEARCH_PROMPT_TEMPLATE
)
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnableLambda
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
 
def web_search(web_query: str, num_results: int) -> list[str]:
    return [r["link"] for r in DuckDuckGoSearchAPIWrapper().results(web_query, num_results)]
 
NUM_SEARCH_QUERIES = 2
 
web_searches_chain = (
    RunnableLambda(lambda x:
        {
            'assistant_instructions': x['assistant_instructions'],
            'num_search_queries': NUM_SEARCH_QUERIES,
            'user_question': x['user_question']
        }
    )
    | WEB_SEARCH_PROMPT_TEMPLATE | get_llm() | StrOutputParser() | to_obj 
)
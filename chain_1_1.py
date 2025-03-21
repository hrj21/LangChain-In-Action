from utilities import to_obj, get_llm
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
 
def web_search(web_query: str, num_results: int) -> list[str]:
    return [r["link"] for r in DuckDuckGoSearchAPIWrapper().results(web_query, num_results)]

from prompts import (
    ASSISTANT_SELECTION_PROMPT_TEMPLATE, 
)

from langchain.schema.output_parser import StrOutputParser
 
assistant_instructions_chain = (
    ASSISTANT_SELECTION_PROMPT_TEMPLATE | get_llm() | StrOutputParser() | to_obj
)
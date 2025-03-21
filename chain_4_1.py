from utilities import get_llm
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnableLambda, RunnableParallel
from prompts import (
    SUMMARY_PROMPT_TEMPLATE
)
from bs4 import BeautifulSoup
# from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
 
# def web_search(web_query: str, num_results: int) -> list[str]:
#     return [r["link"] for r in DuckDuckGoSearchAPIWrapper().results(web_query, num_results)]
def web_scrape(url: str) -> str:
    try:
        response = requests.get(url)
 
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            page_text = soup.get_text(separator=" ", strip=True)
 
            return page_text
        else:
            return f"Could not retrieve the webpage: Status code {response.status_code}"
    except Exception as e:
        print(e)
        return f"Could not retrieve the webpage: {e}"
 
RESULT_TEXT_MAX_CHARACTERS = 10000
 
search_result_text_and_summary_chain = (
    RunnableLambda(lambda x:
        {
            'search_result_text': web_scrape(url=x['result_url'])[:RESULT_TEXT_MAX_CHARACTERS],
            'result_url': x['result_url'], 
            'search_query': x['search_query'],
            'user_question': x['user_question']
        }
    )
    | RunnableParallel (
        {
            'text_summary': SUMMARY_PROMPT_TEMPLATE | get_llm() | StrOutputParser(),
            'result_url': lambda x: x['result_url'],
            'user_question': lambda x: x['user_question']            
        }
    )
    | RunnableLambda(lambda x: 
        {
            'summary': f"Source Url: {x['result_url']}\nSummary: {x['text_summary']}",
            'user_question': x['user_question']
        }
    ) 
)
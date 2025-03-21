from langchain.schema.runnable import RunnableLambda
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper
 
def web_search(web_query: str, num_results: int) -> list[str]:
    return [r["link"] for r in DuckDuckGoSearchAPIWrapper().results(web_query, num_results)]

NUM_SEARCH_RESULTS_PER_QUERY = 3
 
search_result_urls_chain = (
    RunnableLambda(lambda x: 
        [
            {
                'result_url': url, 
                'search_query': x['search_query'],
                'user_question': x['user_question']
            }
            for url in web_search(web_query=x['search_query'], 
                                  num_results=NUM_SEARCH_RESULTS_PER_QUERY)
        ]
    )
)
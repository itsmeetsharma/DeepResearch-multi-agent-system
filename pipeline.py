from agents import build_reader_agent, build_search_agent, writer_chain, Critic_chain

def run_research_pipeline(topic: str) -> dict:
    state = {}

    # search agent working
    print("\n" + " =" * 50)
    print("\n[bold green]step 1:Search Agent is working ...[/bold green]")
    print("\n" + " =" * 50)

    search_agent = build_search_agent()
    search_result = search_agent.invoke({
        "messages": [{"role": "user", "content": f"Find recent, reliable and detailed information about: {topic}"}]
    })
    state["search_results"] = search_result['messages'][-1].content # extracting content from agent response

    print("\n search result ", state['search_results'])

    # step 2 - reader agent 
    print("\n" + " =" * 50)
    print("\n[bold green]step 2:Reader Agent is scraping top resources ...[/bold green]")
    print("\n" + " =" * 50)

    reader_agent = build_reader_agent()
    reader_result = reader_agent.invoke({
        "messages": [{
            "role": "user",
            "content": (
                f"Based on the following search results about '{topic}', "
                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                f"Search Results:\n{state['search_results'][:800]}"
            )
        }]
    })
    state["scraped_content"] = reader_result['messages'][-1].content

    print("\nScraped content\n", state['scraped_content'])

    # step 3 - writer agent
    print("\n" + " =" * 50)
    print("\n[bold green]step 3:Writer Agent is writing report ...[/bold green]")
    print("\n" + " =" * 50)

    research_combined = (
        f"SEARCH RESULTS :\n{state['search_results'][:3000]}\n\n"
        f"DETAILED SCRAPED CONTENT :\n{state['scraped_content'][:3000]}"
    )
    state["report"] = writer_chain.invoke({
        "topic": topic,
        "research": research_combined
    })

    print("\n Final Report\n", state['report'])

    # step 4 - critic report
    print("\n" + " =" * 50)
    print("\n[bold green]step 4:Critic is reviewing the report ...[/bold green]")
    print("=" * 50)

    state['feedback'] = Critic_chain.invoke({
        "report": state['report']
    })

    print("\n critic report \n", state['feedback'])

    return state

if __name__ == "__main__":
    topic = input("\n Enter a research topic: ")
    run_research_pipeline(topic)

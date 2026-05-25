from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from tools import web_search, scrape_url
from dotenv import load_dotenv

load_dotenv()

# ── Backup models for rate-limit resilience ──
# Models are tried in order. If one hits a rate limit, the next takes over.
MODELS = [
    "openai/gpt-oss-20b",           # primary
    "llama-3.3-70b-versatile",       # fallback 1
    "llama-3.1-8b-instant",          # fallback 2
]

def _llm(model_name):
    """Create a ChatGroq instance for a given model."""
    return ChatGroq(model=model_name, temperature=0)

# Lazy initialization for LLM with automatic fallbacks
_llm_chain = None

def get_llm():
    """Lazy load LLM chain when first needed."""
    global _llm_chain
    if _llm_chain is None:
        import os
        if not os.getenv("GROQ_API_KEY"):
            raise ValueError(
                "GROQ_API_KEY environment variable not set. "
                "Please set it in Streamlit Secrets or environment variables."
            )
        _llm_chain = _llm(MODELS[0]).with_fallbacks([_llm(m) for m in MODELS[1:]])
    return _llm_chain

# Legacy support - allow imports to work
def get_llm_lazy():
    """Alias for backwards compatibility."""
    return get_llm()


# 1st agent — builds one agent per model, chains them as fallbacks
def build_search_agent():
    agents = [
        create_agent(
            model=_llm(m),
            tools=[web_search],
            system_prompt="You are a careful research search agent. Use the search tool and return useful titles, URLs, and snippets."
        )
        for m in MODELS
    ]
    return agents[0].with_fallbacks(agents[1:])

# 2nd agent
def build_reader_agent():
    agents = [
        create_agent(
            model=_llm(m),
            tools=[scrape_url],
            system_prompt="You are a careful research reader. Pick the most relevant URL from the search results, scrape it, and summarize the useful content."
        )
        for m in MODELS
    ]
    return agents[0].with_fallbacks(agents[1:])

# writer chain(using LCEL(LangChain Expression Language) pipline)

writer_prompt = ChatPromptTemplate.from_messages([
    ("system","You are an expert research writer. write clear, structured and insightful reports."),
    ("human", """Write a detailed research report on topic below.

Topic:{topic}

Research Gathered:
{research}

Structure the report as:
-Introduction
-Key Findings (minimum 3 well-explained points)
-Conclusion
-sources (list all URLs used for research)

Be detailed, factual and professional."""),
])

def get_writer_chain():
    """Lazy load writer chain."""
    return writer_prompt | get_llm() | StrOutputParser()

# Legacy support
writer_chain = None

# Critic_chain (Using LCEL pipeline)

critic_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a sharp and constructive research critic. Be honest and specific."),
    ("human", """Review the research report below and evaluate it strictly.

Report:
{report}
    
Respond in this exact format:

score: x/10

strengths:
-...
-...

Areas to Improve:
-...
-...
     
One line verdict:
..."""),
])

def get_critic_chain():
    """Lazy load critic chain."""
    return critic_prompt | get_llm() | StrOutputParser()

# Legacy support
Critic_chain = None

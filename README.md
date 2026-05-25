<div align="center">

# 🧠 DeepResearch — AI Multi-Agent Research System

**Four specialized AI agents collaborate to deliver publication-ready research reports in seconds.**

[![Streamlit](https://img.shields.io/badge/Streamlit-1.48-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![LangChain](https://img.shields.io/badge/LangChain-1.0+-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)](https://langchain.com)
[![Groq](https://img.shields.io/badge/Groq-LLM-F55036?style=for-the-badge&logo=groq&logoColor=white)](https://groq.com)

---

</div>

## 🎯 What is DeepResearch?

DeepResearch is a **multi-agent AI research system** that automates the entire research workflow — from finding sources to writing a polished report — using a pipeline of four specialized agents:

| Agent | Role | Tool |
|-------|------|------|
| 🔍 **Search Agent** | Discovers relevant, reliable sources | Tavily Search API |
| 📖 **Reader Agent** | Scrapes and extracts key content | BeautifulSoup |
| ✍️ **Writer Agent** | Drafts a structured research report | Groq LLM |
| 🧐 **Critic Agent** | Reviews, scores, and critiques the report | Groq LLM |

## ✨ Features

- **🚀 Full Research Pipeline** — Enter a topic and watch all four agents work in real-time
- **📝 Standalone Critic Review** — Paste any report (yours or AI-generated) and get instant, structured feedback
- **⬇️ Download Reports** — Export your research as a Markdown file
- **🎨 Premium Dark UI** — Animated gradients, glassmorphism cards, circular score gauge, vertical timeline
- **⚡ Blazing Fast** — Powered by Groq's ultra-fast LLM inference

## 🛠️ Tech Stack

- **Framework:** [LangChain](https://langchain.com) (Agents + LCEL Chains)
- **LLM:** [Groq](https://groq.com) — `openai/gpt-oss-20b`
- **Search:** [Tavily](https://tavily.com) — AI-optimized search engine
- **Scraping:** [BeautifulSoup4](https://beautiful-soup-4.readthedocs.io)
- **UI:** [Streamlit](https://streamlit.io)

## 📁 Project Structure

```
DeepResearch-multi-agent-system/
├── app.py              # Streamlit UI (main entry point)
├── pipeline.py         # CLI pipeline runner
├── agents.py           # Agent & chain definitions
├── tools.py            # Search & scraping tools
├── requirements.txt    # Python dependencies
├── .streamlit/
│   └── config.toml     # Streamlit theme & config
└── .env                # API keys (not committed)
```

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- [Groq API key](https://console.groq.com)
- [Tavily API key](https://tavily.com)

### Installation

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/DeepResearch-multi-agent-system.git
cd DeepResearch-multi-agent-system

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate   # Windows
# source .venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

### Run

```bash
# Streamlit UI (recommended)
streamlit run app.py

# CLI mode
python pipeline.py
```

## 🎨 Screenshots

> _Add screenshots of your running app here_

## 📄 How It Works

```mermaid
graph LR
    A[👤 User Topic] --> B[🔍 Search Agent]
    B --> C[📖 Reader Agent]
    C --> D[✍️ Writer Agent]
    D --> E[🧐 Critic Agent]
    E --> F[📄 Final Report + Score]
```

1. **Search Agent** uses Tavily to find 5 relevant, recent sources with titles, URLs, and snippets
2. **Reader Agent** picks the most relevant URL and scrapes it for deeper content using BeautifulSoup
3. **Writer Agent** combines all research into a structured report (Intro → Key Findings → Conclusion → Sources)
4. **Critic Agent** reviews the report and provides a score out of 10, strengths, areas to improve, and a one-line verdict

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## 📜 License

This project is open source and available under the [MIT License](LICENSE).

---

<div align="center">

**⭐ Star this repo if you found it useful!**

</div>

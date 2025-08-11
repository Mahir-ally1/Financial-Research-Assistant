# Financial Research Assistant

A lightweight research assistant that analyzes public markets using tool-augmented LLM calls. It fetches market data, computes RSI, summarizes earnings-call transcripts via Amazon Bedrock, and aggregates news, insider activity, institutional ownership, and EPS YoY growth — all in a simple Streamlit chat UI.


## Features
- Chat UI (Streamlit) — Ask a question or a ticker-based query; responses are evidence-based.
- RSI Summary — Computes RSI from historical prices (yfinance) and returns min/max/avg + signal.
- News Sentiment — Pulls ticker news via yfinance.get_news, runs NLTK VADER sentiment.
- Insider Activity — Summarizes 6M insider buys/sells & net bias.
- Institutional Ownership — Top-5 holders, % held, and net bias (accumulating vs trimming).
- EPS YoY Growth — Quarter-over-quarter YoY growth stats from the income statement.
- Earnings Call Summaries (Bedrock) — Fetches Alpha Vantage transcripts and summarizes with Amazon Bedrock (Converse API, Anthropic Claude 3.5 Haiku).

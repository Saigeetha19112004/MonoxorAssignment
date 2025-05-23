# MonoxorAssignment
# 📈 Multi-Agent System for Stock Analysis using Google ADK

This project is a modular, intelligent multi-agent system built using **Google ADK** and **Python**, designed to handle natural language stock-related queries.

## 🎯 Objective

To create a robust system that can analyze stock-related questions by leveraging multiple intelligent subagents, each specialized in a specific task. The system is capable of understanding queries like:

- “Why did Tesla stock fall today?”
- “What’s the current price of Nvidia?”
- “Give me recent news about Apple.”
- “How has Palantir’s stock changed in the last week?”

---

## 🧠 Subagents Overview

The system uses 5 independent but orchestrated subagents:

| Subagent Name        | Role                                                                 |
|----------------------|----------------------------------------------------------------------|
| `identify_ticker`     | Extracts the stock ticker symbol from user queries.                 |
| `ticker_price`        | Fetches the real-time stock price using the Alpha Vantage API.      |
| `ticker_news`         | Retrieves the latest stock-related news headlines.                  |
| `ticker_price_change` | Calculates how much the stock price changed in a specific timeframe.|
| `ticker_analysis`     | Summarizes possible reasons behind recent price movements.          |

Each agent is modular and can be replaced or extended independently.

---

## Tech Stack

-  **Google ADK (Agent Developer Kit)** – For creating modular intelligent agents
-  **Python** – Agent logic and data processing
-  **Flask (optional)** – Backend integration (if using webhooks)
-  **Alpha Vantage API** – Real-time stock prices and news
-  **python-dotenv** – Secure environment variable management

---



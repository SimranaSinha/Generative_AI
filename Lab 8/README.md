# Lab 8 – Multi-Agent Investment Analysis with CrewAI 💼🤖

This lab focuses on building a **multi-agent investment analysis system** using CrewAI, where multiple specialized agents collaborate to analyze stocks, assess risks, and generate final investment recommendations.

---

## 📌 Overview

The system simulates a real-world investment workflow by coordinating multiple AI agents, each responsible for a specific task such as market research, financial analysis, strategy formulation, and final decision-making.

The workflow integrates:

* Multi-agent collaboration
* Real-time financial data
* Risk-based strategy design
* Retrieval-Augmented Generation (RAG)

---

## 🎯 Objectives

* Build and coordinate multiple AI agents using CrewAI
* Implement **task delegation and sequential workflows**
* Integrate **live financial data (yfinance + web scraping)**
* Incorporate **RAG for enhanced analysis**
* Generate structured **investment recommendations (BUY / HOLD / SELL)**

---

## 🧠 Agents in the System

The system uses **4 specialized agents**, each with a distinct role:

* **Market Research Analyst**
  → Analyzes stock trends and market positioning

* **Research Analyst**
  → Evaluates company fundamentals, growth, and risks

* **Risk-Aware Strategist** *(customized)*
  → Designs strategy using:

  * Entry price
  * Stop loss
  * Target price
  * Risk-reward ratio

* **Portfolio Manager**
  → Combines all insights into a final recommendation

---

## ⚙️ Key Customizations

Compared to the base lab, the system was enhanced with:

* ✅ Renamed **Trading Strategist → Risk-Aware Strategist**
* ✅ Added **risk_reward_calculator** for:

  * Risk/reward ratio
  * Capital at risk
  * Position sizing
* ✅ Integrated **live data using yfinance + Yahoo Finance scraping**
* ✅ Structured **sequential multi-agent workflow**

As noted in your report, this made the system more realistic and aligned with actual portfolio decision processes 

---

## 📊 Stocks Tested

The system was tested on:

* **TSLA** → High volatility, growth-focused
* **GOOGL** → Stable, strong fundamentals
* **NVDA** → High growth driven by AI demand

---

## 📈 Observations

* Each agent contributed **distinct and complementary insights**
* Multi-agent setup produced **more structured and logical outputs** than a single model
* Final recommendations were more reliable due to:

  * Market trends
  * Fundamentals
  * Risk management

Example findings:

* **TSLA** → Cautious strategy due to volatility
* **GOOGL** → Balanced recommendation
* **NVDA** → Strong positive outlook

These observations are consistent with your analysis where different agents contributed specialized reasoning for each stock 

---

## 🧪 Workflow

1. Fetch real-time stock data
2. Market analysis by Agent 1
3. Fundamental analysis by Agent 2
4. Strategy creation by Agent 3
5. Final decision by Agent 4

---

## 📂 Project Structure

```
📦 Lab 8/
│
├── 📄 Multi_Agent_Investment_Analysis_Simran.ipynb   # Main implementation
│
├── 📄 Simran_Sinha_CrewAI Report.pdf                 # 1–2 page report
│
└── 📘 README.md                                      # Project documentation
```

---

## 🛠️ Tools & Technologies

* Python
* CrewAI
* OpenAI / LLMs
* yfinance
* Web Scraping (Yahoo Finance)
* RAG (Retrieval-Augmented Generation)

---

## 📚 Key Learnings

* Multi-agent systems improve **reasoning quality and structure**
* Proper **agent role design is critical**
* Real-time data significantly enhances decision-making
* RAG helps integrate external knowledge effectively
* AI works best as a **decision support system**, not a replacement

As highlighted in your report, poorly defined agent roles can lead to overlapping or confusing outputs 

---

## 📸 Completion Certificate

Include your certificate screenshot at the end of the report as required.

---

## 🚀 Conclusion

This lab demonstrates how **multi-agent AI systems can handle complex decision-making tasks** like investment analysis. By combining structured workflows, real-time data, and risk-aware strategies, the system produces more reliable and practical recommendations.

---

If you want, I can also:

* make a **short version (like 5–6 lines for quick repo view)**
* or make it **more recruiter-facing for GitHub/portfolio**


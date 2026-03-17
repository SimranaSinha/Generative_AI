# Generative_AI

---

## Assignment 1 : Prompt Roles & API Basics

This assignment demonstrates the fundamentals of **role-based prompting** using a chat model and a basic **OpenAI API call**.
The notebook focuses on understanding how **System, User, and Assistant** roles influence model behavior and response quality.

## Contents
* `Assignment1_Simran Sinha.ipynb` — Jupyter notebook with prompt roles and API execution

## Key Concepts
* Role-based prompting
* Prompt structure control
* Introductory OpenAI API usage

---

## Lab 1 : ExcelGPT & AI_Reply Function

This assignment demonstrates the integration of generative AI into Microsoft Excel using a custom AI_Reply function powered by the OpenAI API. The workbook focuses on applying prompt-driven AI to common business and analytics tasks directly within a spreadsheet environment.

The assignment highlights how structured prompts and inputs can be used to automate formatting, analysis, content generation, data cleaning, translation, summarization, and classification workflows while following responsible API usage practices.

## Contents
* ` ExcelGPT_v3_Simran Sinha.xlsm ` — Excel workbook implementing the AI_Reply function with multiple real-world use cases

## Key Concepts
* Generative AI in Excel
* Prompt design for business workflows
* AI-assisted data analysis and transformation
* Secure API handling and best practices

---

## Lab 2 : Prompting Strategies

This lab demonstrates how different prompting strategies influence the reasoning quality, consistency, and accuracy of large language model outputs. The notebook focuses on applying structured prompts to the same problem and analyzing how model behavior changes based on prompt design and temperature settings.

The lab emphasizes practical experimentation with prompting techniques rather than application development.

## Contents
* ` Lab_2_Module_3_Prompting_Strategies_in_Practice_Simran.ipynb ` — Jupyter notebook exploring multiple prompting strategies and response analysis

## Key Concepts
* Prompt engineering techniques
* Zero-shot and few-shot prompting
* Chain-of-thought reasoning
* Self-consistency and temperature effects

---

## Lab 3 : GenAI-Assisted Decision Making in the Beer Game

This lab explores the use of Generative AI as a decision-support tool in the Beer Game supply chain simulation. The focus is on understanding how prompt design and human–AI collaboration influence ordering decisions, cost behavior, and stability over multiple simulation runs.

Rather than modifying the simulation logic, the lab emphasizes prompt experimentation, comparative analysis, and evaluation of GenAI-assisted versus manual decision-making.

### Contents
* ` M4_Lab2_GenAI_BeerGame_V1.ipynb ` — Jupyter notebook exploring GenAI-assisted decision making and prompt-based order planning in the Beer Game
* Part 1 — Prompt engineering experiments using three strategies (Baseline, Cost-Aware Conservative, Risk-Constrained Data-Driven)
* Part 2 — Manual vs. GenAI-assisted order planning comparison
* Reports — PDF summaries of findings for Part 1 and Part 2
* CSV / Excel files — Combined experimental results

### Key Concepts
* Prompt engineering for operational decision-making
* GenAI as a decision-support system
* Cost and variability analysis in supply chains
* Human–AI collaboration in multi-period environments

---

## Discussion 1 : GenAI_Triage

This discussion examines the use of Generative AI models for medical triage support, focusing on how prompt design and model selection influence reasoning quality, consistency, and safety in healthcare decision-making.

The notebook explores AI-assisted triage as a decision-support tool, emphasizing human-in-the-loop workflows rather than autonomous clinical decisions.

### Contents
* ` Discussion_1_GenAI_Triage.ipynb` — Jupyter notebook analyzing GenAI-assisted triage, prompt variations, and model behavior
* ` Gemini and OpenAI.png `
* ` Human-in-the-Loop Triage Integration.png `   

### Key Concepts
* AI-assisted medical triage
* Prompt engineering for clinical reasoning
* Model comparison and response consistency
* Human-in-the-loop decision support

---

## Lab 4: LangChain Templates & Memory

This lab explores how different LangChain memory types influence conversational context retention, reasoning behavior, and response quality in AI systems. 

The focus is on understanding how memory design impacts sequential decision-making rather than building a full application.

### Contents
* ` Simran Sinha_LangChainMemory.ipynb ` - Jupyter notebook implementing prompt templates and multiple LangChain memory modules
* ` beer_game_memory_comparison.xlsx` - Memory behavior comparison using a supply chain (Beer Game) example
* ` stock_market_memory_comparison.xlsx` - Memory behavior comparison using stock market trend prediction

### Key Concepts
* Prompt templates and structured prompting
* LangChain memory modules
* Short-term vs long-term context retention
* Memory impact on AI reasoning and predictions

---

## Lab 5: Building AI Agents with LangChain

This lab explores how structured chains and autonomous agents can be built using LangChain to enable multi-step reasoning, tool usage, and dynamic decision-making.

The focus is on understanding the difference between deterministic workflows (chains) and flexible reasoning systems (agents).

### Contents

* `M6_Lab5_AI_Agents_Simran Sinha.ipynb` – Jupyter notebook implementing prompt chains, sequential chains, and an AI agent with tools
* `AI_Agents_Simran Sinha_Report.pdf` – Detailed analysis of agent behavior and comparison between chains and agents

### Key Concepts

* Single prompt chains
* Multi-step sequential chains
* Agent initialization and tool integration
* Conversation memory in agents
* Chains vs Agents comparison
* Structured orchestration of LLM workflows

---

## Assignment 2: Data Analysis with AI_Analyse Function

This assignment focuses on extending Excel with an AI-powered function, **AI_Analyse**, to perform contextual, multi-dimensional data analysis directly from spreadsheet ranges.

The objective was to move beyond traditional Excel formulas and enable descriptive, diagnostic, and prescriptive insights using structured prompts.

### Contents

* `Simran Sinha_ExcelGPT.xlsm` – Excel macro-enabled file implementing the `AI_Analyse` VBA function
* `Simran Sinha_ExcelGPT_Report.pdf` – Detailed report explaining implementation, experiments, and findings

### Key Concepts

* VBA integration with external AI API
* Converting Excel ranges into structured text for AI processing
* Prompt refinement for improved analytical depth
* Descriptive vs Diagnostic vs Prescriptive analysis
* AI-assisted interpretation of financial, marketing, and operations data
* Limitations of AI-based spreadsheet integration

---

## Hackathon : World Cup 2026 Squad Builder

A multi-step LangChain reasoning pipeline that builds a **23-player FIFA World Cup squad** from real football statistics using semantic search, constraint enforcement, and LLM-backed justifications.

Built for the **World Cup GenAI Hackathon**, this project demonstrates structured orchestration of retrieval, reasoning, tools, memory, and explainability.

### Contents

* `Hackathon/app.py` — Streamlit chat application
* `Hackathon/squad_builder.ipynb` — End-to-end notebook pipeline
* `Hackathon/squad_builder.html` — Exported notebook version
* `Hackathon/requirements.txt` — Project dependencies

### Key Concepts

* Multi-step reasoning pipelines
* LangChain agents and tool orchestration
* Retrieval-Augmented Generation (RAG) with FAISS
* Constraint-based decision systems (World Cup roster rules)
* LLM-generated tactical justifications
* Interactive analytics dashboard with Plotly

---

## Lab 6: RAG Comparison – FAISS + OpenAI vs ChromaDB + HuggingFace

A Retrieval-Augmented Generation (RAG) comparison project that evaluates two pipelines using different vector databases and embedding models. The experiment measures response accuracy, processing speed, and setup complexity using a renewable energy dataset.

Built as part of a Generative AI lab to demonstrate how different vector databases and embedding models impact RAG performance.

### Contents

* `RAG_Simran_Sinha.ipynb` — End-to-end RAG implementation notebook  
* `Accuracy.png` — Accuracy comparison chart  
* `Time.png` — Response time comparison chart  
* `Simran Sinha_RAG Report.pdf` — 1-page experiment report  

### Key Concepts

* Retrieval-Augmented Generation (RAG) pipelines  
* Vector databases (FAISS vs ChromaDB)  
* Embedding models (OpenAI vs HuggingFace)  
* Semantic search and document chunking  
* Performance comparison of RAG systems  
* Response accuracy and latency evaluation

---
## Notes

All the labs are intended for academic learning and experimentation purposes. Model outputs should not be assumed to be correct without verification, especially in high-stakes or real-world applications.

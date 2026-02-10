# Lab 2: Prompting Strategies

## Overview

This lab focuses on exploring and comparing different prompting strategies used with large language models to improve reasoning quality, consistency, and correctness. The goal is to understand how prompt structure and guidance influence model outputs when applied to the same problem.

Rather than building a full application, this lab emphasizes prompt experimentation, analytical comparison, and thoughtful evaluation of model behavior.

---

## Objectives
	•	Experiment with multiple prompting strategies on the same task
	•	Understand how reasoning guidance affects model responses
	•	Compare output quality across different prompting techniques
	•	Analyze the strengths and limitations of each approach

---

## Project Structure

```
📦 Lab 4/
│
├── 📄 Simran Sinha_LangChainMemory.ipynb
│
├── 📊 beer_game_memory_comparison.xlsx
│
├── 📊 stock_market_memory_comparison.xlsx
│
└── 📘 README.md   # Project documentation
```

---

## Tools & Technologies
- Jupyter Notebook
- Python
- OpenAI Chat Models
- Prompt engineering techniques

---

## Prompting Strategies Covered

The notebook demonstrates multiple prompting approaches applied to the same reasoning problem.
	•	Zero-shot Prompting
  
Directly asks the model to solve the task without examples or additional guidance.
	•	Few-shot Prompting
  
Provides one or more examples to guide the model toward the expected reasoning pattern.
	•	Chain-of-Thought Prompting
  
Explicitly encourages step-by-step reasoning before arriving at a final answer.
	•	Self-Consistency Strategy
  
Generates multiple reasoning paths and compares outputs to identify the most consistent result.
	•	ReAct Style Prompting
  
Combines reasoning steps with intermediate actions to improve structured problem solving.

---

## Experiment Design
- The same logical problem is tested across different prompting strategies
- Model temperature values are varied to observe changes in creativity and determinism
- Outputs are evaluated for correctness, clarity, and depth of reasoning

---

## Observations & Analysis

Key observations include:
	•	Structured prompts significantly improve reasoning accuracy
	•	Chain-of-Thought prompting produces clearer and more interpretable responses
	•	Higher temperature increases response diversity but can reduce consistency
	•	Self-consistency improves reliability at the cost of additional computation

---

## Learning Outcomes

Through this lab, I gained practical experience with:
	•	Designing effective prompts for reasoning-focused tasks
	•	Understanding how temperature impacts model outputs
	•	Comparing prompting strategies in a controlled experimental setup
	•	Evaluating AI responses beyond surface-level correctness

---

## Notes

This lab is intended for academic learning and experimentation purposes. Model outputs should not be assumed to be correct without verification, especially in high-stakes or real-world applications.


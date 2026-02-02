# Lab 3: GenAI-Assisted Decision Making in the Beer Game

## Overview

This lab focuses on applying Generative AI as a decision-support tool within the Beer Game supply chain simulation. The objective is to study how different prompt designs and levels of AI involvement influence ordering decisions, cost behavior, and stability over multiple weeks.

Rather than modifying the underlying simulation logic, the lab emphasizes prompt engineering, controlled experimentation, and comparative analysis of GenAI-driven decision outcomes.

---

## Objectives

* Apply Generative AI to weekly order planning in a supply chain simulation
* Evaluate how prompt structure affects GenAI decision quality
* Compare cost behavior and variability across different prompt strategies
* Analyze GenAI’s role as a decision-support system rather than full automation

---

## Project Structure
```
📦 Lab 3/
│
├── 📂 Part 1/
│   │
│   ├── 📂 Prompt 1/
│   │   # Baseline (Full GenAI) experiments
│   │
│   ├── 📂 Prompt 2/
│   │   # Cost-Aware Conservative prompting experiments
│   │
│   ├── 📂 Prompt 3/
│   │   # Risk-Constrained Data-Driven prompting experiments
│   │
│   ├── 📄 Simran_Sinha_BeerGame_Part1.xlsx
│   │   # Experimental results for Part 1
│   │
│   └── 📄 Simran_Sinha_Part1.pdf
│       # Report for Part 1 (Prompt Engineering Analysis)
│
├── 📂 Part 2/
│   │
│   ├── 📂 GenAI-Assisted/
│   │   # GenAI-assisted order planning runs
│   │
│   ├── 📂 Manual/
│   │   # Manual order planning runs
│   │
│   ├── 📄 Simran_Sinha_Part2.pdf
│   │   # Report for Part 2 (Manual vs GenAI comparison)
│   │
│   ├── 📄 Simran_BeerGame_GenAI.csv
│   │   # Combined CSV results for all Part 2 runs
│   │
│   ├── 📄 Simran_BeerGame_GenAI.xlsx
│   │   # Excel version of combined results
│   │
│   └── 📄 M4_Lab2_GenAI_BeerGame_V1.ipynb
│       # Beer Game simulation notebook
│
├── 📂 M4_Lab2_GenAI_BeerGame_V1.ipynb
│     # Python file 
│
└── 📘 README.md
    # Project documentation
```
---

## Tools & Technologies

* Python
* Jupyter Notebook
* Beer Game simulation environment
* Generative AI (Chat-based LLMs)
* Prompt engineering techniques

---

## Prompting Strategies Covered

The notebook evaluates multiple prompting approaches applied to the same Beer Game decision task.

**Baseline (Full GenAI)**  
A flexible prompt with minimal constraints, allowing GenAI to freely determine weekly order quantities.

**Cost-Aware Conservative Prompt**  
Introduces cost-minimization goals and conservative ordering constraints to limit inventory buildup.

**Risk-Constrained Data-Driven Prompt**  
A highly structured prompt with explicit constraints on decision variables to reduce risk and volatility.

---

## Experiment Design

* Experiments are conducted at the retailer level of the Beer Game
* Each prompt strategy is evaluated over multiple iterations
* Simulations run across multiple weeks per iteration
* Performance is measured using total cost and variability metrics
* Results are compared across prompting strategies under identical conditions

---

## Observations & Analysis

**Key observations include:**

* Prompt structure has a significant impact on GenAI decision outcomes
* Flexible prompts can outperform conservative ones under moderate demand variability
* Over-constraining GenAI may lead to excessive safety buffers and higher costs
* Variability (standard deviation) is as important as average cost when evaluating performance
* GenAI performs best when used as a decision-support tool rather than full automation

---

## Learning Outcomes

Through this lab, I gained experience with:

* Applying Generative AI to operational decision-making problems
* Designing prompts that balance flexibility and constraint
* Evaluating AI systems using both cost and stability metrics
* Understanding the limitations of GenAI in dynamic, multi-period environments

---

## Notes

This lab is intended for academic experimentation and analysis. GenAI-generated decisions should always be reviewed and validated, especially in real-world or high-stakes supply chain applications.

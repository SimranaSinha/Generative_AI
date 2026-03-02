# Lab 5 – Building AI Agents with LangChain

## Overview

This lab focuses on building structured AI workflows using **LangChain and Agents**.
The primary objective was to move beyond single prompt interactions and design multi-step reasoning systems that combine LLMs with structured logic and external tools.

The lab has **3 sections**:

* Single Prompt Chain
* Multi-step Sequential Chain
* Agent with Tools (dynamic reasoning and actions)

I implemented controlled pipelines as well as autonomous agent behavior and analyzed how decision-making differs between static chains and dynamic agents.

---

## Implementation Details

### Single Prompt Chain

The first task involved creating an LLM pipeline using:

* PromptTemplate
* ChatOpenAI
* Pipe operator (`|`) to chain components

System flow:

```
Prompt → LLM → Response
```

This exercise demonstrated that prompts can be separated from models to increase flexibility.

**Main Idea:**
Decoupling prompts from models increases modularity and reuse.

---

### Multi-Step Sequential Chain (Customer Review Pipeline)

This section divided the problem into two structured steps:

1. Sentiment Analysis
2. Response Generation based on detected sentiment

Two separate prompt templates were created.
The output of the first LLM call became the input of the second LLM call.

This mirrors real-world reasoning, where decisions are segmented rather than compressed into a single prompt.

#### Observations:

* Breaking tasks into smaller components improved clarity.
* Sentiment classification performance was more stable when isolated.
* Packing everything into one prompt reduced reasoning quality.
* Debugging multi-step chains was easier than debugging long prompts.

**Main Idea:**
Segmenting reasoning reduces cognitive burden on the model.

---

### Agent with Tools (Unit Conversion Agent)

This final section introduced a dynamic AI Agent using:

* `initialize_agent`
* Custom Tool
* `ConversationBufferMemory`
* LLM with reasoning capability

Unlike static chains, the agent can:

* Select which tool to use
* Perform calculations dynamically
* Maintain conversational memory
* Reason through intermediate steps

In the unit conversion task, the agent parsed the user query, selected the appropriate tool, applied the logic, and returned the result.

This marked the transition from static pipelines to autonomous reasoning systems.

---

## Observations on Agent Performance

### What Worked Well

* Well-defined prompts improved tool selection accuracy.
* Memory enabled smooth conversational flow.
* Agents handled multi-step reasoning better than single-step chains.
* Clear tool descriptions improved decision-making quality.

### What Did Not Work Perfectly

* Ambiguous tool descriptions caused inconsistent behavior.
* Agents sometimes over-explained simple calculations.
* Memory occasionally retained unnecessary context.
* Debugging agents was more complex than debugging simple chains.

---

## Chains vs Agents Comparison

| Feature              | Chains  | Agents    |
| -------------------- | ------- | --------- |
| Control              | High    | Moderate  |
| Flexibility          | Limited | High      |
| Debugging            | Easy    | Harder    |
| Autonomy             | Low     | High      |
| Multi-step reasoning | Manual  | Automatic |

**Key Difference:**
Chains are deterministic with predefined execution paths.
Agents introduce dynamic reasoning, which increases flexibility but also variability.

---

## What We Learned

* Chains perform best in deterministic, step-by-step workflows.
* Agents perform best in dynamic decision environments.
* Prompt wording directly influences tool selection and reasoning.
* Modular design improves robustness over large monolithic prompts.

---

## Key Takeaway

Structure makes intelligent systems.

By combining:

* Prompt Engineering
* Memory
* Tool Integration
* Sequential Logic

We can build intelligent reasoning agents.

Agents provide flexibility, but also introduce unpredictability. The challenge lies in balancing control and autonomy.

---

## Conclusion

Intelligent AI systems are not built through large models alone. They require orchestration.

* Chains offer predictability and control.
* Agents offer autonomy and flexibility.

The transition from single prompts to structured workflows represents the shift from simply using a model to designing intelligent AI systems.

---

## Notes

This lab is intended for academic learning and experimentation purposes. Model outputs should not be assumed to be correct without verification, especially in high-stakes or real-world applications.

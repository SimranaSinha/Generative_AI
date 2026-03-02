# Lab 4 – LangChain Templates and Memory

## Objective

The purpose of this lab was to examine the impact of **prompt templates** and different **LangChain memory structures** on conversational context retention and context-aware response generation 

Specifically, this lab explored:

* How prompt templates enable structured and reusable prompts
* How different memory types affect recall, reasoning continuity, and response quality
* The trade-offs between full conversation history and limited memory windows
* Realistic applications using supply chain (Beer Game) and stock market trend prediction examples

---

## Prompt Templates – Key Observations

Prompt templates were used to standardize model input while allowing dynamic variable injection at runtime using placeholders such as `{topic}`, `{context}`, and `{stock history}` 

### Description

* Improved consistency in responses due to structured format
* Separation of prompt logic from input values reduced errors
* Easier experimentation compared to hard-coded prompts

**Main Insight:**
Templates improve modularity, scalability, and experimental control.

---

## ConversationBufferMemory (Full History)

This memory type stores the entire conversation history and passes it to the model at every interaction 

### Observations – Beer Game (Supply Chain)

* The model correctly recalled previously stated demand values
* When constraints were unclear, the model requested clarification instead of guessing 

### Observations – Stock Market Example

* Context grew with each week processed
* Predictions increasingly relied on early volatility patterns 

### Strengths

* Strong recall accuracy
* Better long-term trend awareness
* Suitable for tasks requiring historical reasoning 

### Limitations

* Context size increases rapidly
* Higher token usage
* May include irrelevant older information 

---

## ConversationBufferWindowMemory (Limited History)

This memory type stores only the last **k interactions**.
In this lab, a window size of **3** was used 

### Observations – Stock Market Example

* Early price changes were dropped once outside the window
* Predictions became more influenced by recent prices
* Less reliance on long-term patterns 

### Comparative Behavior

* Buffer memory produced more historically grounded predictions
* Window memory produced shorter, recent-context-driven predictions 

### Strengths

* Lower memory overhead
* Focused on recent signals
* Suitable for streaming-style applications 

### Limitations

* Loss of early context can change predictions
* Less reliable for long-term trend detection 

---

## Memory Retrieval and Analysis

Memory states were retrieved using `load_memory_variables()` after each interaction, allowing direct comparison between memory types 

Key differences observed:

* Buffer memory continuously grew in size
* Window memory remained capped
* Prediction differences were directly linked to available context

Results were saved to Excel files to compare:

* Stock prices
* Stored memory context
* Model predictions

This clearly demonstrated how memory selection impacts reasoning behavior 

---

## Key Takeaways

1. Prompt templates provide consistency and experimental control
2. Memory type significantly affects reasoning behavior
3. ConversationBufferMemory supports long-term historical reasoning
4. ConversationBufferWindowMemory emphasizes recent context
5. AI predictions depend heavily on the context provided, even when prompts remain identical 

---

## Conclusion

This lab highlights the importance of **memory design** in AI systems 

By keeping prompts constant and only modifying memory type, the experiment demonstrated that:

* Differences in predictions were not random
* They were driven by context availability

Memory is not just storage. It directly shapes reasoning, trend detection, and overall model behavior.

---

## Notes

This lab is intended for academic learning and experimentation purposes. Model outputs should not be assumed to be correct without verification, especially in high-stakes or real-world applications.



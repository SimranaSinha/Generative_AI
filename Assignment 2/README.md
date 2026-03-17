# Assignment 2 : Data Analysis with AI_Analyse Function

## Overview

This assignment focuses on extending Excel with an AI-powered function, **`AI_Analyse`**, designed to perform structured, contextual data analysis directly on spreadsheet ranges.

The primary objective was to move beyond traditional Excel formulas and enable descriptive, diagnostic, and prescriptive analysis using prompt-driven AI reasoning integrated through VBA.

The assignment includes:

* Designing a reusable AI-powered Excel function
* Converting structured Excel ranges into AI-readable format
* Comparing analysis quality across progressively refined prompts
* Evaluating AI-assisted insights across Finance, Marketing, and Operations use cases

I implemented a modular function that integrates Excel with an external AI API while maintaining flexibility, reusability, and structured experimentation.

---

## Project Structure

```
📦 Assignment 2/
│
├── 📄 Simran Sinha_ExcelGPT.xlsm
│
├── 📄 Simran Sinha_ExcelGPT_Report.pdf
│
└── 📘 README.md   # Project documentation
```

---

## Implementation Details

### AI_Analyse Function Design

The `AI_Analyse` function was built as an extension of an existing `AI_Reply` function.

The function accepts:

* API Key
* Excel data range
* Analysis prompt
* Optional model specification
* Optional temperature setting

The selected Excel range is converted into a structured, CSV-like text representation before being embedded into a carefully constructed instruction prompt. This prompt is then passed to the AI model for analysis.

**Main Idea:**
Separate data processing from prompt logic to ensure modularity and reusability.

---

### Prompt Refinement Strategy

To evaluate analytical depth, three progressively refined prompts were used for each domain:

1. Basic descriptive analysis
2. Diagnostic reasoning with deeper criteria
3. Executive-level summary with recommendations

This was tested across:

* Finance – Time series trend analysis
* Marketing – Channel performance comparison
* Operations – Anomaly detection and root cause analysis

Each refinement improved clarity, depth, and business relevance of insights.

---

## Analytical Capabilities Beyond Excel

Traditional Excel functions can calculate trends, averages, and outliers, but they do not provide contextual interpretation.

AI_Analyse enabled:

* Multi-metric pattern interpretation
* Natural-language business explanations
* Identification of plausible causes (seasonality, inefficiencies, disruptions)
* Prescriptive recommendations
* Rapid iteration by modifying only the prompt

**Key Insight:**
Changing the prompt allows rapid movement from descriptive to diagnostic to prescriptive analysis without altering formulas or data structure.

---

## Observations

### What Worked Well

* Prompt refinement significantly improved output quality
* AI connected multiple dimensions of data simultaneously
* Generated contextual business explanations
* Enabled faster experimentation compared to manual analytics

### Limitations

* Dependent on API connectivity and system configuration
* Data quality directly affects insight reliability
* Does not replace statistical validation
* Requires careful prompt engineering for best results

---

## Key Takeaways

* Prompt design directly impacts analytical depth
* AI can augment spreadsheet analytics with contextual reasoning
* Modular VBA design improves flexibility and reuse
* AI-driven range analysis enables faster decision support

---

## Conclusion

The `AI_Analyse` function demonstrates how AI can significantly enhance Excel’s analytical capabilities.

While traditional formulas focus on computation, AI enables interpretation and recommendation. This assignment highlights the shift from static spreadsheet calculations to AI-assisted decision support systems driven by structured prompts and modular design.

---

## Notes

This assignment is intended for academic experimentation. AI-generated insights should always be validated before being used in real-world business decisions.



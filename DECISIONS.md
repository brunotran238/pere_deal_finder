# Project Decisions & Trade-offs

This document outlines the key assumptions and tradeoffs made in the design and implementation of the Real Estate Deal Analysis CrewAI system.

---

## ✅ Assumptions

1. **Scoring Criteria Are Defined Externally**
   - The scoring logic is not hardcoded but provided through external files: `criteria_pere.md` and `scoring_template_pere.json`.

2. **Input Property Dataset Is Clean and Complete**
   - Assumes `seed_properties.csv` contains no missing critical values and is well-formatted.

3. **Top 12 Assets Is a Fixed Number**
   - The system is designed to extract exactly 12 top-scoring assets — not a dynamic threshold.

4. **Citations Are Searchable Online**
   - Assumes that meaningful market references for each top asset can be retrieved via web search (Serper).

5. **Agents Operate Sequentially**
   - Each task fully completes before the next starts to ensure correct data dependency handling.

---

## ⚖️ Tradeoffs

1. **🧠 Hardcoded API Usage vs. Tool Generalization**
   - Chose Serper for web search due to simplicity; not abstracted to allow switching tools easily.

2. **⚙️ Static Workflow vs. Dynamic Agent Chaining**
   - Opted for `Process.sequential` to guarantee order and reduce complexity; prevents parallel task execution for speed optimization.

3. **🔎 Reference Quantity Limitation**
   - Enforces a minimum of 2 references per asset; may reduce quality if good sources are limited or redundant.

4. **📜 Markdown-Based Memos Only**
   - Output memos in markdown format; tradeoff between readability and machine-readability (e.g., no HTML or PDF export).

---

## 💡 Future Improvements

- Support for CSV or Markdown input/output configuration.
- Dynamic agent selection or scoring threshold.
- Alternate search providers (Brave, Bing via LangChain).
- Parallel research/memo writing to reduce runtime.
- GUI or dashboard for investor-facing outputs.


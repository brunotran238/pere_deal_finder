# Project Decisions & Trade-offs

This document outlines the key assumptions and tradeoffs made in the design and implementation of the Real Estate Deal Analysis CrewAI system.

---

## ✅ Assumptions

## Assumptions I Made (to Keep Moving)

1. **Scoring Criteria Would Come from a Structured Source**  
   I assumed we'd have scoring logic (weights, priorities) in a file like `scoring_template_pere.json`. That way I didn't have to hardcode it. It also allows others to change the logic later without changing code.

2. **12 Assets Is a Good Cutoff**  
   Picking exactly 12 top assets was arbitrary but helpful — it let me constrain the output and simplify logic (no sorting thresholds or edge cases).

3. **Citations Can Be Found for Any Asset**  
   I assumed Serper search results would give *something useful* for every top asset. In real life, this could totally fail if the asset isn’t public, so this is fragile — but I moved forward anyway to test the flow.

4. **Agents Can Share Data Through Output Files**  
   I avoided memory-sharing between agents and just passed data through JSON files. It’s more manual but less error-prone than trying to pass complex Python objects across agents.

---


## Trade-Offs I Made (and Why)

1. **Kept It Sequential (Not Parallel)**  
   I went with `Process.sequential` even though it’s slower. Why? Because each task depends directly on the one before — memo writing doesn’t make sense without validated signals, and signals don’t exist without scored assets.

2. **Used JSON Instead of a Database**  
   I chose to write to `top_assets.json`, `top_assets_url.json` and `investment_memos.md` files instead of a database or CSV. It’s easier to structure, and I didn’t want to get stuck on schema design.

3. **Relied on Serper for All Signal Research**  
   I only used one tool (SerperDevTool). That’s risky if Serper results are bad or blocked, but it kept things simple. In the future I’d add fallbacks like Brave or Bing.

4. **Didn’t Over-Validate Inputs**  
   I assumed that `seed_properties.csv` would be clean enough to work with. This could break in edge cases, but it saved time during prototyping.

--- 

## 💡 Future Improvements

- Support for CSV or Markdown input/output configuration.
- Dynamic agent selection or scoring threshold.
- Alternate search providers (Brave, Bing via LangChain).
- Parallel research/memo writing to reduce runtime.
- GUI or dashboard for investor-facing outputs.

## TL;DR
I prioritized **clarity and linear progress** over perfection. Made assumptions to keep momentum, isolated complexity into files, and aimed for a flow that **actually finishes**, even if the results aren’t perfect every time.



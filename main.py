import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import SerperDevTool, CSVSearchTool, FileReadTool, JSONSearchTool

# 🔑 Set your API keys
os.environ["OPENAI_API_KEY"] = "your-open-api-key"
os.environ["SERPER_API_KEY"] = "your-serper-api-key"

# --- TOOLS ---
csv_tool = CSVSearchTool(csv_path="seed_properties.csv")
scoring_tool = JSONSearchTool(json_path="scoring_template_pere.json")
criteria_tool = FileReadTool(file_path="criteria_pere.md")
search_tool = SerperDevTool()
top_assets_tool = JSONSearchTool(json_path="top_12_assets.json")



# --- JSON SCHEMA DEFINITION ---
JSON_SCHEMA = """
The JSON must be an array of exactly 12 objects. Each object must follow this schema:
{
  "id": "string - unique property identifier from seed_properties.csv",
  "name": "string - property name",
  "location": "string - city, state",
  "score": "integer - score calculated using scoring_template_pere.json",
  "justification": "string - 1-2 sentence explanation of why the property scored this way",
  "signals": "array of objects - initially empty, will be filled later",
  "memo": "string - initially empty, will be filled later"
}
"""

# --- AGENTS ---
deal_scoring_analyst = Agent(
    role="Deal Scoring Analyst",
    goal="Score all properties and create a structured JSON file with the top 12 assets.",
    backstory="You are a meticulous real estate deal scoring analyst.",
    tools=[csv_tool, criteria_tool, scoring_tool],
    verbose=True,
    memory=True,
)

signals_researcher = Agent(
    role="Signals Researcher",
    goal="Validate the top 12 assets by finding citations, references, and market signals.",
    backstory="You are a deep-dive researcher who validates deals with market data."
            "You use cutting-edge tools to track real estate activity, news, and economic indicators to uncover opportunities before others do",
    tools=[search_tool, top_assets_tool],
    verbose=True,
    memory=True,
)

memo_writer = Agent(
    role="Memo Writer",
    goal="Write concise 2–3 sentence memos for the top 12 assets.",
    backstory="You are an expert communicator who writes short, impactful investor memos.",
    tools=[top_assets_tool],
    verbose=True,
    memory=True,
)

# --- TASKS ---
# score_properties = Task(
#     description=(
#         "Read 'seed_properties.csv'. Apply the scoring framework from "
#         "'criteria_pere.md' and 'scoring_template_pere.json'. Rank all properties "
#         "and select the top 12. Output the result as a JSON file called 'top_12_assets.json'. "
#         f"The JSON MUST strictly follow this schema:\n{JSON_SCHEMA}"
#     ),
#     expected_output="A structured JSON file 'top_12_assets.json' with details of the 12 top-ranked assets.",
#     tools=[csv_tool, criteria_tool, scoring_tool],
#     agent=deal_scoring_analyst,
#     output_file="top_12_assets.json",
# )

score_properties = Task(
    description=(
        "Read 'seed_properties.csv'. Apply the scoring framework from "
        "'criteria_pere.md' and 'scoring_template_pere.json'. Rank all properties based on score"
        "and select the top 12. Output the result as a JSON file called 'top_12_assets.json'.\n\n"
        "⚠️ STRICT REQUIREMENTS:\n"
        "- You must output EXACTLY 12 objects in the JSON array.\n"
        "- Do NOT use placeholders, comments, or text like 'additional assets would follow'.\n"
        "- Every asset object MUST have values for: id, name, location, score, justification, signals.\n"
        "- The 'signals' field must always be an empty array [].\n"
        "- If the CSV does not contain enough unique properties, duplicate the top-scoring assets "
        "until there are exactly 12 objects in the output.\n\n"
        f"The JSON MUST strictly follow this schema:\n{JSON_SCHEMA}"
    ),
    expected_output="A structured JSON file 'top_12_assets.json' with exactly 12 full objects following the schema.",
    tools=[csv_tool, criteria_tool, scoring_tool],
    agent=deal_scoring_analyst,
    output_file="top_12_assets.json",
)

validate_signals = Task(
    description=(
        "Read 'top_12_assets.json'. For each asset, search for citations, references, "
        "and supporting market signals that validate its attractiveness. Add them to "
        "the 'signals' array of each asset object."
        "For each signal, you MUST include:\n"
        "- A 2-3 sentence summary of the signal\n"
        "- A direct source URL where the information was found\n"
        "- The article title or headline if available"
    ),
    expected_output="An updated 'top_12_assets.json' file with 'signals' filled for each asset."
                    "Each signal must include a summary, a clickable URL source, and a title.",
    tools=[search_tool, top_assets_tool],
    agent=signals_researcher,
    output_file="top_12_assets.json",
)

write_memos = Task(
    description=(
        "Read 'top_12_assets.json'. For each asset, write a short 2–3 sentence memo "
        "summarising why it is promising, based on its score and signals. "
        "Write the text into the 'memo' field of each asset object. "
    ),
    expected_output="An updated 'top_12_assets.json' file with memos filled for each asset.",
    tools=[top_assets_tool],
    agent=memo_writer,
    output_file="top_12_assets.json",
)

# --- CREW ---
crew = Crew(
    agents=[deal_scoring_analyst, signals_researcher, memo_writer],
    tasks=[score_properties, validate_signals, write_memos],
    process=Process.sequential,
)

if __name__ == "__main__":
    result = crew.kickoff()
    print("\n=== FINAL RESULT ===\n")
    print(result)

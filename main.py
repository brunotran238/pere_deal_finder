# Warning control
import warnings
warnings.filterwarnings('ignore')

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
top_assets_tool = JSONSearchTool(json_path="top_assets.json")
top_assets_url_tool = JSONSearchTool(json_path="top_assets_url.json")


# --- JSON SCHEMA DEFINITION ---
# JSON_SCHEMA = """
# The JSON must be an array of 8 to 12 objects. Each object must follow this schema:
# {
#   "id": "string - unique property identifier from seed_properties.csv",
#   "name": "string - property name",
#   "location": "string - city, state",
#   "score": "integer - score calculated using scoring_template_pere.json",
#   "justification": "string - 1-2 sentence explanation of why the property scored this way",
#   "signals": "array of objects - initially empty, will be filled later",
#   "memo": "string - initially empty, will be filled later"
# }
# """

# --- AGENTS ---
deal_scoring_analyst = Agent(
    role="Deal Scoring Analyst",
    goal="Evaluate and score all assets based on investment potential",
    backstory="You are a skilled investment analyst with experience in quantifying asset value "
        "using risk, return, strategic fit, and market timing. You produce consistent scoring.",
    tools=[csv_tool, criteria_tool, scoring_tool],
    verbose=True
)

signals_researcher = Agent(
    role="Signals Research Analyst",
    goal="Find strong external references that support the top investment assets",
    backstory="You're an expert researcher who tracks citations, news articles, and credible reports "
        "to validate investment ideas. You specialize in finding credible and timely evidence.",
    tools=[search_tool, top_assets_tool],
    verbose=True
)

memo_writer = Agent(
    role="Investment Memo Writer",
    goal="Write consise 3 sentences investment memos based on references and research provided",
    backstory="As a senior financial writer, you're responsible for creating polished investment memos "
        "that summarize the opportunity, evidence, and recommendation in a compelling format.",
    tools=[top_assets_tool],
    verbose=True
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

# score_properties = Task(
#     description=(
#         "Read 'seed_properties.csv'. Apply the scoring framework from "
#         "'criteria_pere.md' and 'scoring_template_pere.json'. Rank all properties based on score"
#         "and select the top 12. Output the result as a JSON file called 'top_assets.json'.\n\n"
#         "⚠️ STRICT REQUIREMENTS:\n"
#         "- You must output 8-12 objects in the JSON array.\n"
#         "- Do NOT use placeholders, comments, or text like 'additional assets would follow'.\n"
#         "- Every asset object MUST have values for: id, name, location, score, justification, signals.\n"
#         "- The 'signals' field must always be an empty array [].\n"
#         "- If the CSV does not contain enough unique properties, duplicate the top-scoring assets "
#         "until there are exactly 12 objects in the output.\n\n"
#         f"The JSON MUST strictly follow this schema:\n{JSON_SCHEMA}"
#     ),
#     expected_output="A structured JSON file 'top_assets.json' with exactly 12 full objects following the schema.",
#     tools=[csv_tool, criteria_tool, scoring_tool],
#     agent=deal_scoring_analyst,
#     output_file="top_assets.json",
# )

scoring_task = Task(
    description=(
        "Read 'seed_properties.csv'. Apply the scoring framework from "
        "'criteria_pere.md' and 'scoring_template_pere.json'."
        "You MUST assign a score between 0-10 for each asset and provide a short reason.\n"
        "From the scored list, select the top 12 assets and output them to a file named `top_assets.json` "
        "as an array of objects with keys: `name`, `score`, `reason`.\n\n"
        "Example format:\n"
        "[{\"id\": \"AUS-001\",\"name\": \"Asset A\", \"score\": 9, \"reason\": \"Strong growth and low risk\"}, ...]"
    ),
    expected_output='A structured JSON file `top_assets.json` file with 12 scored assets.',
    tools=[csv_tool, criteria_tool, scoring_tool],
    agent=deal_scoring_analyst,
    output_file='top_assets.json'
)

# validate_signals = Task(
#     description=(
#         "Read 'top_assets.json'. For each asset, search for citations, references, "
#         "and supporting market signals that validate its attractiveness. Add them to "
#         "the 'signals' array of each asset object."
#         "For each signal, you MUST include:\n"
#         "- A 2-3 sentence summary of the signal\n"
#         "- A direct source URL where the information was found\n"
#         "- The article title or headline if available"
#     ),
#     expected_output="An updated 'top_assets.json' file with 'signals' filled for each asset."
#                     "Each signal must include a summary, a real clickable URL source, and a title.",
#     tools=[top_assets_tool,search_tool],
#     agent=signals_researcher,
#     output_file="top_assets.json",
# )

research_task = Task(
    description=(
        "For each of the 12 top assets in `top_assets.json`, search the web for credible references (news, articles, reports).\n"
        "Find at least 2 citations per asset and summarize each source with its URL.\n\n"
        "Output example for each asset:\n"
        "{\n"
        "  \"id\": \"AUS-001\",\n"
        "  \"name\": \"Asset A\",\n"
        "  \"references\": [\n"
        "    {\"url\": \"https://example.com/1\", \"summary\": \"Strong market position.\"},\n"
        "    ...\n"
        "  ]\n"
        "}"
    ),
    expected_output='A structured JSON file `top_assets_url.json` of 12 assets with 2+ references each and summaries.',
    tools=[top_assets_tool, search_tool],
    agent=signals_researcher,
    output_file='top_assets_url.json',
)
# write_memos = Task(
#     description=(
#         "Read updated with signals filled 'top_assets.json'. For each asset, write a short 2–3 sentence memo "
#         "summarising why it is promising, based on its score and signals. "
#         "Write the text into the 'memo' field of each asset object. "
#     ),
#     expected_output="An updated 'top_assets.json' file with memos filled for each asset.",
#     tools=[top_assets_tool],
#     agent=memo_writer,
#     output_file="top_assets.json",
# )

memo_task = Task(
    description=(
        "For each of the top 12 assets and their references, write an investment memo.\n"
        "Format: Markdown. Length: 2-3 sentences each. Total: 12 memos.\n"
        "Include hyperlinks to citations when relevant."
    ),
    expected_output='12 markdown-formatted investment memos, each 2-3 sentences long.',
    tools=[top_assets_url_tool],
    agent=memo_writer,
    output_file='investment_memos.md',
)

# --- CREW ---
crew = Crew(
    agents=[deal_scoring_analyst, signals_researcher, memo_writer],
    tasks=[scoring_task, research_task, memo_task],
    process=Process.sequential,
    max_iterations=50,
    verbose=True
)

if __name__ == "__main__":
    result = crew.kickoff()
    print("\n=== FINAL RESULT ===\n")
    print(result)

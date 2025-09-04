# Real Estate Deal Analysis with CrewAI

This project uses CrewAI to automatically analyze real estate properties, score them based on defined criteria, and generate investment recommendations with supporting market signals and memos.

## Overview

The system employs three AI agents working sequentially:
1. **Deal Scoring Analyst** -    Scores all properties and selects the top 12 investment opportunities.
2. **Signals Researcher** - Gathers citations, news, and reports to validate each selected asset
3. **Memo Writer** - Produces a 2-3 sentences investment memo per asset based on research findings.

## Prerequisites

### Required Python Packages
```bash
pip install crewai
pip install crewai-tools
```

### API Keys Required
- **OpenAI API Key** - For AI agent functionality
- **Serper API Key** - For web search capabilities

## Project Structure

```
project/
├── main.py                       # Main execution file
├── seed_properties.csv           # Property dataset (input)
├── criteria_pere.md              # Evaluation framework (input)
├── scoring_template_pere.json    # Scoring logic (input)
├── top_assets.json               # Generated output file
├── top_assets_url.json           # Generated output file
└── investment_memos.md           # Generated output file

```

## Input Files

### 1. seed_properties.csv
Contains the property dataset with columns for property details that will be analyzed and scored.

### 2. criteria_pere.md
Markdown document describing how to evaluate deals (qualitative guidance).

### 3. scoring_template_pere.json
JSON with scoring weights and attribute importance (quantitative logic).

## Setup Instructions

### 1. Set API Keys
Before running, you need to set your API keys in the environment or directly in the `main.py`:

```python
os.environ["OPENAI_API_KEY"] = "your-openai-api-key-here"
os.environ["SERPER_API_KEY"] = "your-serper-api-key-here"
```

**Note**: The current code has hardcoded API keys which should be replaced with your own keys or environment variables for security.

### 2. Ensure Input Files Exist
Make sure these files are in the same directory as `main.py`:
- `seed_properties.csv`
- `criteria_pere.md`
- `scoring_template_pere.json`

## How to Run

### Execute the Main Script
```bash
python main.py
```

## Process Flow

### Stage 1: Property Scoring
- Reads all properties from `seed_properties.csv`
- Applies scoring framework from `criteria_pere.md` and `scoring_template_pere.json`
- Score each asset (0-10) and select top 12
- Write result to `top_assets.json`

### Stage 2: Signal Validation
- Performs web search via Serper API for 12 assets
- Gathers 2+ citations (URL, source, summary)
- Write result to `top_assets_url.json`

### Stage 3: Memo Generation
- Writes 2-3 sentence investment memos for each asset
- Write result to investment_memos.md

## Output Format

The final `top_assets.json` follows this schema:

```json
[
  {
    "id": "AUS-001", 
    "name": "Retail (Neighbourhood) Western Sydney Sydney", 
    "score": 7.53, 
    "reason": "Good yield and strong rent gap with moderate stability"}
]
```

## Key Features

- **Agent Collaboration**: Built with CrewAI’s agent-task framework
- **Quantitative Scoring**: Uses structured criteria and weights
- **Live Signal Research**: Pulls real-time references from the web
- **Memo Generation**: Produces markdown memos suitable for investor decks
- **Modular Design**: Easy to adapt to other asset classes

## Troubleshooting

### Common Issues

1. **Missing API Keys**: Ensure both OpenAI and Serper API keys are valid and set
2. **File Not Found**: Verify all input files are in the correct directory
3. **Invalid JSON Output**: The system enforces exactly 12 objects in the output

### Debug Mode
The agents run in verbose mode by default, providing detailed logs of their decision-making process.

## Security Note

⚠️ **Important**: The current code contains hardcoded API keys. For production use:
- Store API keys in environment variables
- Use a `.env` file with `python-dotenv`
- Never commit API keys to version control

```python
# Recommended approach:
import os
from dotenv import load_dotenv

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["SERPER_API_KEY"] = os.getenv("SERPER_API_KEY")
```

## Expected Runtime

- **Stage 1 (Scoring)**: 2-5 minutes depending on dataset size
- **Stage 2 (Signals)**: 3-5 minutes (includes web searches)
- **Stage 3 (Memos)**: 1-2 minutes
- **Total**: Approximately 6-12 minutes for complete analysis
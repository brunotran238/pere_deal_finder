# Real Estate Deal Analysis with CrewAI

This project uses CrewAI to automatically analyze real estate properties, score them based on defined criteria, and generate investment recommendations with supporting market signals and memos.

## Overview

The system employs three AI agents working sequentially:
1. **Deal Scoring Analyst** - Scores properties and selects top 12 assets
2. **Signals Researcher** - Validates assets with market data and citations
3. **Memo Writer** - Creates concise investment summaries

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
├── main.py                      # Main execution file
├── seed_properties.csv          # Property dataset (input)
├── criteria_pere.md            # Evaluation framework (input)
├── scoring_template_pere.json  # Scoring logic (input)
└── top_12_assets.json          # Generated output file
```

## Input Files

### 1. seed_properties.csv
Contains the property dataset with columns for property details that will be analyzed and scored.

### 2. criteria_pere.md
Defines the evaluation framework and criteria used to assess each property.

### 3. scoring_template_pere.json
Contains the specific scoring logic and weights applied to different property attributes.

## Setup Instructions

### 1. Set API Keys
Before running, you need to set your API keys in the environment or directly in the code:

```python
os.environ["OPENAI_API_KEY"] = "your-openai-api-key-here"
os.environ["SERPER_API_KEY"] = "your-serper-api-key-here"
```

**Note**: The current code has hardcoded API keys which should be replaced with your own keys or environment variables for security.

### 2. Ensure Input Files Exist
Make sure these files are in the same directory as `test.py`:
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
- Ranks properties and selects top 12
- Creates `top_12_assets.json` with initial structure

### Stage 2: Signal Validation
- Searches for market signals and citations for each of the top 12 assets
- Updates the `signals` array in `top_12_assets.json`
- Each signal includes: source, URL, and summary

### Stage 3: Memo Generation
- Writes 2-3 sentence investment memos for each asset
- Updates the `memo` field in `top_12_assets.json`
- Summarizes why each property is promising

## Output Format

The final `top_12_assets.json` follows this schema:

```json
[
  {
    "id": "unique property identifier from CSV",
    "name": "property name",
    "location": "city, state",
    "score": 85,
    "justification": "1-2 sentence explanation of the score",
    "signals": [
      {
        "source": "Market data source",
        "url": "https://example.com",
        "summary": "Supporting market information"
      }
    ],
    "memo": "2-3 sentence investment summary"
  }
]
```

## Key Features

- **Automated Scoring**: Uses AI to apply complex scoring criteria consistently
- **Market Validation**: Searches for real market signals to validate recommendations
- **Investment Memos**: Generates concise, actionable investment summaries
- **Structured Output**: Produces machine-readable JSON for further analysis

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
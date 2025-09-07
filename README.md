# Bushfire Plan Generator

An AI-powered application that helps Australian property owners create comprehensive bushfire survival plans through an interactive assessment process.

***Note that these instructions are for a Mac OS machine. You will find equivalent instructions for a Windows machine on the Internet.***

## Overview

This application uses LangGraph and OpenAI's GPT-4 to guide users through a structured bushfire planning process:

1. **Risk Assessment** - Evaluates bushfire risk based on location, vegetation, and property characteristics
2. **Defense Capability Assessment** - Determines ability to defend property during a bushfire
3. **Plan Creation** - Generates either a "leave early" or "stay and defend" plan
4. **Final Documentation** - Produces a comprehensive Markdown-formatted bushfire plan

## Setup

Once cloned, enter the folder and set up a virtual Python environment:
```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Create an OpenAI account and retrieve an API key. Create a `.env` file in the project root:
```
OPENAI_API_KEY="<your OpenAI API key>"
```

## Running

To run the application:
```bash
python3 main.py
```

Follow the interactive prompts to:
- Describe why you want to create a bushfire plan
- Answer questions about your property and circumstances
- Make choices about your preferred approach (stay/defend vs. leave early)
- Receive a personalized bushfire survival plan

## Features

- **Interactive Assessment** - Guided questioning process tailored to your responses
- **Australian Context** - Uses Australian bushfire terminology and safety protocols
- **Structured Output** - Generates plans using Pydantic models for consistency
- **State Persistence** - Maintains conversation state throughout the planning process
- **Comprehensive Plans** - Covers evacuation routes, timing, supplies, and backup procedures

## Architecture

Built using:
- **LangGraph** - Workflow orchestration and state management
- **OpenAI GPT-4** - Natural language processing and plan generation
- **Pydantic** - Structured data validation and parsing
- **LangChain** - LLM integration and prompt management

## Output

The application generates a detailed bushfire plan including:
- Risk assessment summary
- Defense capability evaluation
- Recommended strategy (leave or defend)
- Detailed action steps
- Backup plans for various scenarios

## Notes

- Plans are generated based on Australian bushfire safety guidelines
- The application prioritizes human safety over property protection
- All assessments use evidence-based risk evaluation methods
- Generated plans should be reviewed with local fire authorities
- Based on LLM AI models, there is no guarentee that the plan is correct, effective or complete - please review before use
- Once reviewed share with all occupants at the property
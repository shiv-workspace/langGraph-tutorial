
# langgraph-example-repo

This repository contains ready-to-run example code for the LangGraph Day exercises (multi-agent, stateful graph with persistence and human-in-the-loop).

## Prerequisites
- Python 3.9+
- Docker (optional, for building image)
- `langgraph-cli` (to run `langgraph dev`, `langgraph build`, `langgraph up`)

Install CLI (recommended in a virtualenv):
```bash
pip install --upgrade pip
pip install langgraph-cli langgraph langchain-openai
# or if you prefer the JS CLI: npm i -g @langchain/langgraph-cli
```

## Files
- `app.py` - example multi-agent stateful graph application (entrypoint)
- `requirements.txt` - Python dependencies
- `langgraph.json` - minimal config used by `langgraph` CLI
- `Dockerfile` - image for running the app in a container
- `run_local.sh` - convenience script to run locally in dev mode (uses langgraph dev)

## Quick start (development)
1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start dev server (hot-reload):
   ```bash
   langgraph dev
   ```
4. Open LangGraph Studio and connect to `http://localhost:8123` (or use the CLI to invoke the graph).

## Build & Run with Docker (optional)
1. Build image:
   ```bash
   langgraph build -t langgraph-example:latest
   ```
   or
   ```bash
   docker build -t langgraph-example:latest .
   ```
2. Run container:
   ```bash
   docker run --env-file .env -p 8123:8000 langgraph-example:latest
   ```

## Notes
- The `app.py` file contains runnable examples and also exposes a compiled graph object for the LangGraph server to pick up (depending on your LangGraph CLI expectations).
- You may need to set your OpenAI API key if you plan to run the LLM-based examples:
  ```bash
  export OPENAI_API_KEY="sk-..."
  ```

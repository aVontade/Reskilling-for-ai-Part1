# AI Insight Generator

This directory contains the source code for the "AI Insight Generator" project.

## Setup

To get started, install the project dependencies from the repository root:

```bash
pip install -e .[dev]
```

## Data Pipeline

The data pipeline consists of two main scripts that should be run in order from the repository root.

### 1. Parse Book Content

This script reads the main `README.md` file from the repository root, parses its content, and loads it into a local SQLite database (`book_data.db`).

```bash
python -m ai_insight_generator.src.data_parser
```

### 2. Create Vector Embeddings

This script reads the content from the SQLite database, generates vector embeddings for each chapter, and uploads them to a Pinecone vector database.

**IMPORTANT:** This script requires API keys to be set as environment variables.

#### Required Environment Variables

You must set the following environment variable before running the script:

*   `PINECONE_API_KEY`: Your API key for the Pinecone service.

For local development, it is recommended to create a `.env` file in the repository root and use a library like `python-dotenv` to load the variables. **Ensure `.env` is included in your `.gitignore` file to avoid committing secrets.**

Example `.env` file:
```
PINECONE_API_KEY="your-pinecone-api-key-here"
```

Once the environment variable is set, you can run the script:

```bash
python -m ai_insight_generator.src.create_embeddings
```

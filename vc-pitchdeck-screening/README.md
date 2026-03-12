# vc-pitchdeck-screening

This project is a minimal MVP of an AI-based venture capital screening system. It transforms startup pitch decks into structured startup representations and retrieves comparable startups from public web data for similarity-based ranking.

## Project Structure

```text
vc-pitchdeck-screening/
├── README.md
├── requirements.txt
├── pipeline.py
├── data/
│   └── pitch_decks/
│       └── Palta.pdf
└── src/
    ├── pdf_extraction.py
    ├── information_extraction.py
    ├── startup_search.py
    └── similarity.py
```

## Installation

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project root:

```env
OPENAI_API_KEY=
TAVILY_API_KEY=
```

## Run the Pipeline

```bash
cd vc-pitchdeck-screening
python pipeline.py
```

The pipeline performs:

1. Pitch deck text extraction from PDF (`PyMuPDF`).
2. Structured startup representation extraction (`OpenAI API`).
3. Comparable startup retrieval from public web data (`Tavily`).
4. Similarity ranking with sentence embeddings (`all-MiniLM-L6-v2`).
5. Console output of the startup JSON and ranked comparable startups.

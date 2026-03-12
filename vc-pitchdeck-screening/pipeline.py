import json
from pathlib import Path

from dotenv import load_dotenv

from src.information_extraction import extract_startup_representation
from src.pdf_extraction import extract_pitchdeck_text
from src.similarity import rank_similar_startups
from src.startup_search import search_comparable_startups


def _build_search_query(startup_representation: dict) -> str:
    fields = [
        startup_representation.get("value_proposition", ""),
        startup_representation.get("customer_segments", ""),
        startup_representation.get("product_technology", ""),
        startup_representation.get("industry_market", ""),
    ]
    query = " ".join(part for part in fields if part).strip()
    return query or "innovative startup company"


def main() -> None:
    project_root = Path(__file__).resolve().parent
    load_dotenv(project_root / ".env", override=True)

    pdf_path = project_root / "data" / "pitch_decks" / "Palta.pdf"
    if not pdf_path.exists():
        raise FileNotFoundError(f"Pitch deck not found: {pdf_path}")

    pitchdeck_text = extract_pitchdeck_text(str(pdf_path))
    startup_representation = extract_startup_representation(pitchdeck_text)

    query = _build_search_query(startup_representation)
    startup_results = search_comparable_startups(query)
    ranked_startups = rank_similar_startups(startup_representation, startup_results)

    print("Startup Representation (JSON):")
    print(json.dumps(startup_representation, indent=2, ensure_ascii=False))
    print("\nTop Comparable Startups:")

    for idx, startup in enumerate(ranked_startups, start=1):
        print(f"\n{idx}. {startup.get('company_name', 'Unknown')}")
        print(f"   Description: {startup.get('description', '')}")
        print(f"   Similarity Score: {startup.get('similarity_score', 0.0):.4f}")
        print(f"   URL: {startup.get('url', '')}")


if __name__ == "__main__":
    main()

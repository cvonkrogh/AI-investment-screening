import json
from typing import Any, Dict, List

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


def _representation_to_text(startup_representation: Dict[str, Any]) -> str:
    return json.dumps(startup_representation, ensure_ascii=True, sort_keys=True)


def rank_similar_startups(
    startup_representation: Dict[str, Any],
    startup_results: List[Dict[str, str]],
) -> List[Dict[str, Any]]:
    """Rank startup results by cosine similarity against pitch deck representation."""
    if not startup_results:
        return []

    model = SentenceTransformer("all-MiniLM-L6-v2")

    source_text = _representation_to_text(startup_representation)
    candidate_texts = [item.get("description", "") for item in startup_results]

    source_embedding = model.encode([source_text])
    candidate_embeddings = model.encode(candidate_texts)

    similarity_scores = cosine_similarity(source_embedding, candidate_embeddings)[0]

    ranked = []
    for item, score in zip(startup_results, similarity_scores):
        ranked_item = dict(item)
        ranked_item["similarity_score"] = float(score)
        ranked.append(ranked_item)

    ranked.sort(key=lambda x: x["similarity_score"], reverse=True)
    return ranked

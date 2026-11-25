from app.evaluation.factuality import split_claims


def analyze_context_groundedness(response: str, context: str) -> dict:
    normalized_context = (context or "").lower()
    claims = []
    for claim in split_claims(response):
        key_words = [word.lower() for word in claim.split() if len(word) > 4]
        supported_words = sum(1 for word in key_words if word in normalized_context)
        ratio = supported_words / len(key_words) if key_words else 0
        label = "Supported" if ratio >= 0.5 else "Unverifiable"
        claims.append({"claim": claim, "label": label, "evidence": context or "No context supplied"})
    return {"claims": claims, "summary": "Claim-level groundedness analysis against the supplied context."}

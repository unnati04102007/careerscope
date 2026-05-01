"""
chatbot_logic.py
----------------
Core chatbot response logic for CareerScope.
Integrates NLP-based college review recommendations (TF-IDF / Cosine Similarity)
with the existing keyword-based intent detection.
"""

import random

# ---------------------------------------------------------------------------
# NLP recommender — graceful fallback if module is unavailable
# ---------------------------------------------------------------------------
try:
    from chatbot.nlp_recommender import get_nlp_recommendations, is_review_query
    _NLP_LOADED = True
except Exception as _nlp_err:
    _NLP_LOADED = False

    def get_nlp_recommendations(q, top_n=3):
        return []

    def is_review_query(msg):
        return False


# ---------------------------------------------------------------------------
# Main entry point (signature unchanged)
# ---------------------------------------------------------------------------
def get_chat_response(message: str) -> str:
    """
    Return a chatbot reply for *message*.

    When the query looks like a review / experience / culture question the NLP
    model is invoked first to produce review-backed college recommendations
    which are then woven into the final response.
    """
    msg = message.lower().strip()

    # ------------------------------------------------------------------
    # 1. NLP enrichment — build extra context from student reviews
    # ------------------------------------------------------------------
    nlp_context = ""
    if _NLP_LOADED and is_review_query(message):
        nlp_results = get_nlp_recommendations(message, top_n=3)
        if nlp_results:
            out_lines = ["📚 STUDENT REVIEW-BASED RECOMMENDATIONS:"]
            for r in nlp_results:
                out_lines.append(
                    f"• {r['college']} "
                    f"(Review Match: {r['match_score']:.0%}, "
                    f"Avg Rating: {r['avg_rating']:.1f}/10, "
                    f"Reviews: {r['total_reviews']})"
                )
                out_lines.append(f'  Student says: "{r["highlight"]}..."')
            nlp_context = "\n".join(out_lines)

    # ------------------------------------------------------------------
    # 2. Keyword-based intent detection (existing logic — unchanged)
    # ------------------------------------------------------------------
    keyword_response = ""

    if any(x in msg for x in ['hi', 'hello', 'hey', 'namaste']):
        keyword_response = (
            "Hello! I am your CareerScope assistant. 😊 "
            "Ask me about careers or colleges — e.g., "
            "'Suggest colleges in Mumbai', 'Hostel life at IIT Bombay'."
        )

    elif any(x in msg for x in ['career', 'job', 'profession']):
        keyword_response = (
            "For career advice, focus on your interests. "
            "If you love coding, explore CS/IT. "
            "If you enjoy design, look at UI/UX or Architecture. "
            "Check our Questionnaire page for a personalised path!"
        )

    elif any(x in msg for x in ['salary', 'money', 'earn', 'package', 'lpa']):
        keyword_response = (
            "Salaries vary by field:\n"
            "• Data Scientist: ₹8–15 LPA avg\n"
            "• Software Engineer: ₹6–20 LPA avg\n"
            "• CA: ₹7–10 LPA starting\n"
            "• Doctor (MBBS): ₹8–15 LPA in hospitals\n"
            "Want details for a specific career?"
        )

    elif 'college' in msg or 'university' in msg or 'institute' in msg:
        keyword_response = (
            "You can explore top colleges in the Colleges section. "
            "Do you have a specific location, stream, or budget in mind?"
        )

    # ------------------------------------------------------------------
    # 3. Compose final response
    # ------------------------------------------------------------------
    if nlp_context and keyword_response:
        # Both NLP results AND a keyword match — combine them
        return f"{nlp_context}\n\n{keyword_response}"

    if nlp_context:
        # Only NLP results — add a helpful closing line
        return (
            f"{nlp_context}\n\n"
            "These recommendations are based on actual student reviews. "
            "Want more details about a specific college?"
        )

    if keyword_response:
        return keyword_response

    # Default fallback
    return (
        "I'm still learning! 🤖 You can ask me about:\n"
        "• College culture, campus life, or placements\n"
        "• Career options and expected salaries\n"
        "• Top colleges in a specific city or state"
    )

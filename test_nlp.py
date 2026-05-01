import sys
sys.path.insert(0, '.')

from chatbot.nlp_recommender import get_nlp_recommendations, is_review_query, _model_ready

print("Model ready:", _model_ready)
print("is_review_query('hostel life at IIT'):", is_review_query("hostel life at IIT"))
print("is_review_query('fees under 1 lakh'):", is_review_query("fees under 1 lakh"))

if _model_ready:
    res = get_nlp_recommendations("good coding culture and placements", top_n=3)
    print("NLP results count:", len(res))
    for r in res:
        print(f"  - {r['college']} | score={r['match_score']:.2f} | rating={r['avg_rating']}")

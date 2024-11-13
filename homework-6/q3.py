from recommendations import loadMovieLens, getRecommendations

prefs = loadMovieLens('ml-100k')
substitute_user = '359'

recommendations = getRecommendations(prefs, substitute_user)

top_recommendations = recommendations[:5]
bottom_recommendations = recommendations[-5:]

print("Top 5 Recommendations for Substitute User:")
for score, movie in top_recommendations:
    print(f"    Movie: {movie}, Predicted Score: {score:.2f}")

print("Bottom 5 Recommendations for Substitute User:")
for score, movie in bottom_recommendations:
    print(f"    Movie: {movie}, Predicted Score: {score:.2f}")
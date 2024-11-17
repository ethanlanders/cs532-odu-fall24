# Import necessary functions from the recommendations module
from recommendations import loadMovieLens, getRecommendations

# Load user preferences and movie data from the MovieLens dataset
# 'prefs' is a dictionary mapping user IDs to their ratings for various movies
prefs = loadMovieLens('ml-100k')

# Define a substitute user for whom recommendations will be generated
# This is the user ID of the target user (me)
substitute_user = '359'

# Generate movie recommendations for the substitute user
recommendations = getRecommendations(prefs, substitute_user)

# Retrieve the top 5 recommended movies (highest predicted scores)
top_recommendations = recommendations[:5]

# Retrieve the bottom 5 recommended movies (lowest prediced scores)
bottom_recommendations = recommendations[-5:]

# Print the top 5 recommended movies for the substitute user
print("Top 5 Recommendations for Substitute User:")
for score, movie in top_recommendations:
    # Each recommendation includes the movie title and the predicted rating score
    print(f"    Movie: {movie}, Predicted Score: {score:.2f}")

# Print the bottom 5 recommended movies for the substitute user
print("Bottom 5 Recommendations for Substitute User:")
for score, movie in bottom_recommendations:
    print(f"    Movie: {movie}, Predicted Score: {score:.2f}")
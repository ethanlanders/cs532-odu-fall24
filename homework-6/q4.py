# Import necessary functions from the recommendations module
from recommendations import loadMovieLens_v2, calculateSimilarItems

# Load the movie data and user preferences
# 'movies' is a dictionary mapping movie IDs to their titles
# 'prefs' is a dictionary mapping user IDs to their ratings for movies
movies, prefs = loadMovieLens_v2('ml-100k')

# Define my favorite and least favorite movies by title
favorite_movie = "Trainspotting (1996)"
least_favorite_movie = "Sleepless in Seattle (1993)"

# Retrieve the ID of my favorite movie by searching through the movies dictionary
favorite_movie_id = next(
    (movie_id for movie_id, title in movies.items() if title.strip().lower() == favorite_movie.strip().lower()),
    None # Default to None if the movie is not found
)

# Retrieve the ID of the least favorite movie in a similar manner
least_favorite_movie_id = next(
    (movie_id for movie_id, title in movies.items() if title == least_favorite_movie),
None # Default to None if the movie is not found
)

# Generate a dictionary of item-item similarities
# 'itemMatch' maps movie IDs to their top similar movies
itemMatch = calculateSimilarItems(prefs, n=10)
for movie_id in list(itemMatch.keys())[:5]:  # Just show the first 5 movie IDs
    print(f"Movie ID: {movie_id}, Similar movies: {itemMatch[movie_id]}")

# Get the top 5 movies most similar to the favorite movie from 'itemMatch'
# If the movie ID is not in 'itemMatch', return an empty list
top_similar_favorite = itemMatch.get(favorite_movie, [])[:5]
if not top_similar_favorite:
    print("No similar movies found for favorite movie.")
else:
    print("Top 5 Most Correlated Movies to Favorite Movie:")
    for similarity, movie_title in top_similar_favorite:
        print(f"    Movie: {movie_title}, Correlation: {similarity:.2f}")

# Get the bottom 5 movies (least correlated) for the favorite movie
bottom_similar_favorite = itemMatch.get(favorite_movie, [])[-5:]

if not bottom_similar_favorite:
    print("No bottom similar movies were found for favorite movie.")
else:
    print("Top 5 Least Correlated Movies to Favorite Movie:")
    for similarity, movie_title in bottom_similar_favorite:
        print(f"    Movie: {movie_title}, Correlation: {similarity:.2f}")

# Get the top 5 movies most similar to the least favorite movie
top_similar_least_favorite = itemMatch.get(least_favorite_movie, [])[:5]
if not top_similar_least_favorite:
    print("No similar movies found for least favorite movie.")
else:
    print("Top 5 Most Correlated Movies to Least Favorite Movie:")
    for similarity, movie_title in top_similar_least_favorite:
        print(f"    Movie: {movie_title}, Correlation: {similarity:.2f}")

# Get the bottom 5 movies (least correlated) for the least favorite movie
bottom_similar_least_favorite = itemMatch.get(least_favorite_movie, [])[-5:]
if not bottom_similar_least_favorite:
    print("No bottom similar movies found for least favorite movie.")
else:
    print("Top 5 Least Correlated Movies to Least Favorite Movie:")
    for similarity, movie_title in bottom_similar_least_favorite:
        print(f"    Movie: {movie_title}, Correlation: {similarity:.2f}")    
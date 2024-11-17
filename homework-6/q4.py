from recommendations import loadMovieLens, calculateSimilarItems, getRecommendations

movies, prefs = loadMovieLens('ml-100k')

favorite_movie = "Trainspotting (1996)"
least_favorite_movie = "Sleepless in Seattle (1993)"

favorite_movie_id = next(
    (movie_id for movie_id, title in movies.items() if title.strip().lower() == favorite_movie.strip().lower()),
    None
)

least_favorite_movie_id = next(
    (movie_id for movie_id, title in movies.items() if title == least_favorite_movie),
None
)

print(f"Favorite movie ID: {favorite_movie_id}")
print(f"Least favorite movie ID: {least_favorite_movie_id}")

itemMatch = calculateSimilarItems(prefs, n=10)

print("First few entries in itemMatch:")
for movie_id in list(itemMatch.keys())[:5]:  # Just show the first 5 movie IDs
    print(f"Movie ID: {movie_id}, Similar movies: {itemMatch[movie_id]}")

top_similar_favorite = itemMatch.get(favorite_movie_id, [])[:5]
if not top_similar_favorite:
    print("No similar movies found for favorite movie.")
else:
    print("Top 5 Most Correlated Movies to Favorite Movie:")
    for similarity, movie_id in top_similar_favorite:
        print(f"    Movie: {movies[movie_id]}, Correlation: {similarity:.2f}")

bottom_similar_favorite = itemMatch.get(favorite_movie_id, [])[-5:]

if not bottom_similar_favorite:
    print("No bottom similar movies were found for favorite movie.")
else:
    print("Top 5 Least Correlated Movies to Favorite Movie:")
    for similarity, movie_id in bottom_similar_favorite:
        print(f"    Movie: {movies[movie_id]}, Correlation: {similarity:.2f}")

top_similar_least_favorite = itemMatch.get(least_favorite_movie_id, [])[:5]
if not top_similar_least_favorite:
    print("No similar movies found for least favorite movie.")
else:
    print("Top 5 Most Correlated Movies to Least Favorite Movie:")
    for similarity, movie_id in top_similar_least_favorite:
        print(f"    Movie: {movies[movie_id]}, Correlation: {similarity:.2f}")

bottom_similar_least_favorite = itemMatch.get(least_favorite_movie_id, [])[-5:]
if not bottom_similar_least_favorite:
    print("No bottom similar movies found for least favorite movie.")
else:
    print("Top 5 Least Correlated Movies to Least Favorite Movie:")
    for similarity, movie_id in bottom_similar_least_favorite:
        print(f"    Movie: {movies[movie_id]}, Correlation: {similarity:.2f}")    
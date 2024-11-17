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

itemMatch = calculateSimilarItems(prefs, n=10)

top_similar_favorite = itemMatch.get(favorite_movie, [])[:5]
if not top_similar_favorite:
    print("No similar movies found for favorite movie.")
else:
    print("Top 5 Most Correlated Movies to Favorite Movie:")
    for similarity, movie_title in top_similar_favorite:
        print(f"    Movie: {movie_title}, Correlation: {similarity:.2f}")

bottom_similar_favorite = itemMatch.get(favorite_movie, [])[-5:]

if not bottom_similar_favorite:
    print("No bottom similar movies were found for favorite movie.")
else:
    print("Top 5 Least Correlated Movies to Favorite Movie:")
    for similarity, movie_title in bottom_similar_favorite:
        print(f"    Movie: {movie_title}, Correlation: {similarity:.2f}")

top_similar_least_favorite = itemMatch.get(least_favorite_movie, [])[:5]
if not top_similar_least_favorite:
    print("No similar movies found for least favorite movie.")
else:
    print("Top 5 Most Correlated Movies to Least Favorite Movie:")
    for similarity, movie_title in top_similar_least_favorite:
        print(f"    Movie: {movie_title}, Correlation: {similarity:.2f}")

bottom_similar_least_favorite = itemMatch.get(least_favorite_movie, [])[-5:]
if not bottom_similar_least_favorite:
    print("No bottom similar movies found for least favorite movie.")
else:
    print("Top 5 Least Correlated Movies to Least Favorite Movie:")
    for similarity, movie_title in bottom_similar_least_favorite:
        print(f"    Movie: {movie_title}, Correlation: {similarity:.2f}")    
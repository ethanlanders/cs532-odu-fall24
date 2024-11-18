from recommendations import loadMovieLens, getRecommendations, calculateSimilarItems

def filter_movies_by_ratings(prefs, min_ratings=10):
    # Count the number of ratings for each movie
    movie_counts = {}
    for user_ratings in prefs.values():
        for movie in user_ratings:
            movie_counts[movie] = movie_counts.get(movie, 0) + 1

    # Filter out movies with fewer than 'min_ratings' ratings
    filtered_movies = {movie for movie, count in movie_counts.items() if count >= min_ratings}

    # Create a filtered prefs dictionary
    filtered_prefs = {}
    for user, user_ratings in prefs.items():
        filtered_prefs[user] = {movie: rating for movie, rating in user_ratings.items() if movie in filtered_movies}

    return filtered_prefs

if __name__ == "__main__":
    # Load original dataset
    prefs = loadMovieLens('ml-100k')

    # Filter the dataset to include only movies with at least 10 ratings
    filtered_prefs = filter_movies_by_ratings(prefs, min_ratings=10)

    # Count how many unique movies are in the filtered dataset
    unique_movies = {movie for user_ratings in filtered_prefs.values() for movie in user_ratings}
    print(f"Number of movies in filtered dataset: {len(unique_movies)}")

    # Re-do Q3 (User recommendations)
    substitute_user = '359'
    recommendations = getRecommendations(filtered_prefs, substitute_user)
    print("(Q3) Top 5 Recommendations for Substitute User:")
    for score, movie in recommendations[:5]:
        # Each recommendation includes the movie title and the predicted rating score
        print(f"    Movie: {movie}, Predicted Score: {score:.2f}")
    
    # Redo Q4 (Item-item correlations)
    item_match = calculateSimilarItems(filtered_prefs, n=10)
    favorite_movie = "Aliens (1986)"
    least_favorite_movie = "Sleepless in Seattle (1993)"

    top_similar_favorite = item_match.get(favorite_movie, [])[:5]
    if not top_similar_favorite:
        print("(Q4) No similar movies found for favorite movie.")
    else:
        print("(Q4) Top 5 Most Correlated Movies to Favorite Movie:")
        for similarity, movie_title in top_similar_favorite:
            print(f"    Movie: {movie_title}, Correlation: {similarity:.2f}")
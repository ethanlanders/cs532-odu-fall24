# Import necessary functions from the recommendations module
from recommendations import loadMovieLens, find_least_most_correlated_users

# Main script execution starts here
if __name__ == "__main__":
    # Load user preferences and movie data from the MovieLens dataset
    # 'prefs' is a dictionary mapping user IDs to their ratings for various movies
    prefs = loadMovieLens('ml-100k')

    # Define a substitue user for whom correlations with other users will be analyzed
    substitute_user_id = '359'

    # Find the most and least correlated user for the substitute user
    # 'find_least_most_correlated_users()' is expected to return two lists:
    # 1. Most correlated users (sorted by highest similarity scores)
    # 2. Least correlated users (sorted by lowest similarity scores)
    most_correlated_users, least_correlated_users = find_least_most_correlated_users(prefs, substitute_user_id)

    # Print the top 5 most correlated users
    print("Top 5 Most Correlated Users:")
    for score, user in most_correlated_users:
        # Each entry contains a user ID and their correlation score with the substitute user
        print(f"    User ID: {user}, Correlation: {score:.2f}")
    
    # Print the top 5 least correalted users
    print("\nTop 5 Least Correlated Users:")
    for score, user in least_correlated_users:
        print(f"    User ID: {user}, Correlation: {score:.2f}")

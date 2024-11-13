from recommendations import loadMovieLens, find_least_most_correlated_users

if __name__ == "__main__":
    prefs = loadMovieLens('ml-100k')

    substitute_user_id = '359'

    most_correlated_users, least_correlated_users = find_least_most_correlated_users(prefs, substitute_user_id)

    print("Top 5 Most Correlated Users:")
    for score, user in most_correlated_users:
        print(f"    User ID: {user}, Correlation: {score:.2f}")
    
    print("\nTop 5 Least Correlated Users:")
    for score, user in least_correlated_users:
        print(f"    User ID: {user}, Correlation: {score:.2f}")

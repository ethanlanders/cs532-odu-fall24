# Import the loadMovieLens function to load user prefernces and movie ratings
from recommendations import loadMovieLens

# Function to load user demographic data from a file
def load_user_data(file_path='ml-100k/u.user'):
    user_data = {}
    with open(file_path, 'r') as f:
        for line in f:
            # Each line in the file is split into components
            user_id, age, gender, occupation, zipcode = line.strip().split('|')
            # Store relevant user details in a dictionary
            user_data[int(user_id)] = {
                'age': int(age),
                'gender': gender,
                'occupation': occupation,
            }
    return user_data

# Function to calculate similarity between two users based on demographic data
def calculate_user_similarity(my_age, my_gender, my_occupation, user_data, user_id):
    # Compute absolute difference in age
    age_diff = abs(my_age - user_data[user_id]['age'])
    # Assign a binary difference for gender (0 if the same, 1 otherwise)
    gender_diff = 0 if my_gender == user_data[user_id]['gender'] else 1
    # Assign a binary difference for occupation (0 if the same, 1 otherwise)
    occupation_diff = 0 if my_occupation == user_data[user_id]['occupation'] else 1
    # The total similarity is the sum of these differences
    return age_diff + gender_diff + occupation_diff

# Function to find the closest users based on demographic similarity
def find_closest_users(my_age, my_gender, my_occupation, user_data, n=3):
    similarities = []
    for user_id in user_data:
        # Avoid comparing a user with themselves
        if user_id != user_data:
            # Calculate the similarity score
            similarity = calculate_user_similarity(my_age, my_gender, my_occupation, user_data, user_id)
            similarities.append((similarity, user_id))
    # Sort the users by similarity score (lowest score indicated closest match)
    similarities.sort(key=lambda x: x[0])
    # Return the IDs of the top N closest users
    return [user_id for _, user_id in similarities[:n]]

# Function to get the top and bottom N movies rated by a user
def get_top_bottom_movies(prefs, user_id, n=3):
    # Get movie ratings from the preferences
    user_ratings = prefs.get(str(user_id), {})
    # Sort the ratings in descending order
    sorted_ratings = sorted(user_ratings.items(), key=lambda x: x[1], reverse=True)
    # Select the top and bottom N movies
    top_movies = sorted_ratings[:3]
    bottom_movies = sorted_ratings[-3:]
    return top_movies, bottom_movies

# Function to display recommendations for a list of users
def display_user_recommendations(prefs, closest_users):
    for user_id in closest_users:
        print(f"User {user_id}'s Recommendations:")
        # Get the user's top and bottom movies
        top_movies, bottom_movies = get_top_bottom_movies(prefs, user_id)
        # Display the top 3 movies
        print(f"    Top 3 Movies:")
        for title, rating in top_movies:
            print(f"        {title} - Rating: {rating}")
        # Display the bottom 3 movies
        print(f"    Bottom 3 Movies:")
        for title, rating in bottom_movies:
            print(f"        {title} - Rating: {rating}")
        print('\n')

# Define my demographic data
my_age = 22
my_gender = 'M'
my_occupation = 'student'

# Main script starts here
if __name__ == "__main__":
    # Load user demographic data
    user_data = load_user_data('ml-100k/u.user')
    # Load user preferences and movie ratings
    prefs = loadMovieLens('ml-100k')

    # Find the closest users to me based on demographic data
    closest_users = find_closest_users(my_age, my_gender, my_occupation, user_data)
    # Display recommendations based on the closest users
    display_user_recommendations(prefs, closest_users)
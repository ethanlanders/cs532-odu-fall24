from recommendations import loadMovieLens

def load_user_data(file_path='ml-100k/u.user'):
    user_data = {}
    with open(file_path, 'r') as f:
        for line in f:
            user_id, age, gender, occupation, zipcode = line.strip().split('|')
            user_data[int(user_id)] = {
                'age': int(age),
                'gender': gender,
                'occupation': occupation,
            }
    return user_data

def calculate_user_similarity(my_age, my_gender, my_occupation, user_data, user_id):
    age_diff = abs(my_age - user_data[user_id]['age'])
    gender_diff = 0 if my_gender == user_data[user_id]['gender'] else 1
    occupation_diff = 0 if my_occupation == user_data[user_id]['occupation'] else 1
    return age_diff + gender_diff + occupation_diff

def find_closest_users(my_age, my_gender, my_occupation, user_data, n=3):
    similarities = []
    for user_id in user_data:
        if user_id != user_data:
            similarity = calculate_user_similarity(my_age, my_gender, my_occupation, user_data, user_id)
            similarities.append((similarity, user_id))
    similarities.sort(key=lambda x: x[0])
    return [user_id for _, user_id in similarities[:n]]

def get_top_bottom_movies(prefs, user_id, n=3):
    user_ratings = prefs.get(str(user_id), {})
    sorted_ratings = sorted(user_ratings.items(), key=lambda x: x[1], reverse=True)
    top_movies = sorted_ratings[:3]
    bottom_movies = sorted_ratings[-3:]
    return top_movies, bottom_movies

def display_user_recommendations(prefs, closest_users):
    for user_id in closest_users:
        print(f"User {user_id}'s Recommendations:")
        top_movies, bottom_movies = get_top_bottom_movies(prefs, user_id)
        print(f"    Top 3 Movies:")
        for title, rating in top_movies:
            print(f"        {title} - Rating: {rating}")
        print(f"    Bottom 3 Movies:")
        for title, rating in bottom_movies:
            print(f"        {title} - Rating: {rating}")
        print('\n')

my_age = 22
my_gender = 'M'
my_occupation = 'student'

if __name__ == "__main__":
    user_data = load_user_data('ml-100k/u.user')
    prefs = loadMovieLens('ml-100k')

    closest_users = find_closest_users(my_age, my_gender, my_occupation, user_data)
    display_user_recommendations(prefs, closest_users)
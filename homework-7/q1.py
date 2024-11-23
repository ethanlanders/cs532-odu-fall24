import os

def generate_files(base_folder, dataset_types, categories, count_per_category):
    os.makedirs(base_folder, exist_ok=True)  # Create base folder if it doesn't exist

    for dataset_type in dataset_types:
        dataset_folder = os.path.join(base_folder, dataset_type)
        os.makedirs(dataset_folder, exist_ok=True)  # Create dataset-specific folder

        for category in categories:
            category_folder = os.path.join(dataset_folder, category)
            os.makedirs(category_folder, exist_ok=True)  # Create category-specific folder

            # Generate files for this category
            count = count_per_category[dataset_type]
            for i in range(1, count + 1):
                file_path = os.path.join(category_folder, f"{dataset_type}_{category}_{i}.txt")
                if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
                    print(f"File '{file_path} already exists and is not empty. Skipping.")
                else:
                    with open(file_path, 'w') as f:
                        f.write("")  # Create an empty file
                    print(f"Created file: {file_path}")

# Specify parameters
base_folder = "emails_dataset"
dataset_types = ["training", "testing"]
categories = ["on_topic", "off_topic"]
count_per_category = {"training": 20, "testing": 5}

# Generate the files
generate_files(base_folder, dataset_types, categories, count_per_category)
print(f"Dataset files processed in {base_folder}/")
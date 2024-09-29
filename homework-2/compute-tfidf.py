import math
import os

# Function to compute Term Frequency (TF)
def compute_tf(word, document):
    words = document.split() # Split document into words (tokens)
    return words.count(word) / len(words) 

# Function to compute Inverse Document Frequency (IDF)
def compute_idf(word, documents, total_docs_in_directory):
    num_docs_with_word = 0
    
    # Loop through each document to check if the word exists
    for doc in documents:
        if word in doc:
            num_docs_with_word += 1
    
    # Compute the IDF using the total number of document and number off docs with term
    return math.log((total_docs_in_directory) / (num_docs_with_word), 2)

# Define the query term for which we want to calculate TF-IDF
query_term = "climate"

# List of 10 files that contain the query term (found using grep)
file_uris = [
    'homework-2/processed_html/3ac6cb5edbed898516d4a54c7af9e22d.html',
    'homework-2/processed_html/3ba3eee197e9cd3a3851eb90582df2dd.html',
    'homework-2/processed_html/43467e2d0e365325ee8fe173596d9ced.html',
    'homework-2/processed_html/43ff03d9016f244c156f7f5ea1f9fc7c.html',
    'homework-2/processed_html/4eb1d913502d08a092762b06cdca73d6.html',
    'homework-2/processed_html/6baf10afbd7528a00d476e6181cebf06.html',
    'homework-2/processed_html/7fb7eaa6fa739a6a93501f73f610cb91.html',
    'homework-2/processed_html/8aed4e66a46468f71768f5084888dfce.html',
    'homework-2/processed_html/8dd04c0da91729a320d7c34b43c7f729.html',
    'homework-2/processed_html/90a687c0ed013c36ee44a64c87ba55d6.html'
]

# Path to the directory containing the processed HTML files
directory_path = 'homework-2/processed_html'

# Get the total number of documents (processed HTML files) in the directory
total_docs_in_directory = len([doc for doc in os.listdir(directory_path)])

# Dictionary to store the content of each file
documents = {}

# Read the content of each file and store it in the 'documents' dictionary
for uri in file_uris:
    with open(uri, 'r', encoding='utf-8') as file:
        documents[uri] = file.read()

# List to store the computed TF-IDF results for each file
tf_idf_results = []

# Loop through each document, compute TF, IDF, and TF-IDF, and store the results
for uri, document in documents.items():
    tf = compute_tf(query_term, document)
    idf = compute_idf(query_term, documents.values(), total_docs_in_directory)
    tf_idf = tf * idf
    tf_idf_results.append((tf_idf, tf, idf, uri))

# Sort the results by the TF-IDF
tf_idf_results.sort(key=lambda x: x[0], reverse=True)

# Print out the TF-IDF, TF, IDF values along with the file URI for each document
for result in tf_idf_results:
    print(f"TF-IDF: {result[0]:.4f}, TF: {result[1]:.4f}, IDF: {result[2]:.4f}, URI: {result[3]}\n")
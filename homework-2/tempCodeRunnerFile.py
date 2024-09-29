import math

def compute_tf(word, document):
    words = document.split()
    return words.count(word) / len(words)

def compute_idf(word, documents):
    num_docs_with_word = 0
    
    for doc in documents:
        if word in doc:
            num_docs_with_word += 1
    # one (1) added to denominator to prevent division by zero if word not found:
    if(num_docs_with_word != 0):
        return math.log((len(documents) + 1) / (1 + num_docs_with_word), 2)
    else:
        return 0

query_term = "climate"

# Files that contain the query term (got with grep)
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

# Dictionary to store the content of each file
documents = {}

for uri in file_uris:
    with open(uri, 'r', encoding='utf-8') as file:
        documents[uri] = file.read()

tf_idf_results = []

for uri, document in documents.items():
    tf = compute_tf(query_term, document)
    idf = compute_idf(query_term, documents.values())
    tf_idf = tf * idf
    tf_idf_results.append((tf_idf, tf, idf, uri))

tf_idf_results.sort(key=lambda x: x[3], reverse=True)

for result in tf_idf_results:
    print(f"TF-IDF: {result[0]:.8f}, TF: {result[1]:.4f}, IDF: {result[2]:.8f}, URI: {result[3]}\n")
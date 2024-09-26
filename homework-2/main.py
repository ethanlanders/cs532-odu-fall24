import download_html
import process_html
import compute_tfidf
import pagerank
import inverted_index

if __name__ == "__main__":
    download_html.main()
    process_html.main()
    compute_tfidf.main()
    pagerank.main()
    inverted_index.main()
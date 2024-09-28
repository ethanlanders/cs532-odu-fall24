# Original PageRank values from https://searchenginereports.net/google-pagerank-checker
pagerank_values = {
    "https://www.odu.edu/oir": 7,
    "https://news-un-org.translate.goog/en/?_x_tr_sl=en&_x_tr_tl=ru": 6,
    "https://news-un-org.translate.goog/en/focus/mali?_x_tr_sl=en&_x_tr_tl=ru": 6,
    "https://news-un-org.translate.goog/en/content/un-news-go?_x_tr_sl=en&_x_tr_tl=ru": 6,
    "https://www.odu.edu/research-0": 7,
    "https://news-un-org.translate.goog/en/un-podcasts?_x_tr_sl=en&_x_tr_tl=ru": 6,
    "https://www-leibniz--gemeinschaft-de.translate.goog/en/about-us/whats-new/news/forschungsnachrichten-single/newsdetails/solidaritaet-mit-der-ukraine?_x_tr_sl=en&_x_tr_tl=uk": 0,
    "https://news-un-org.translate.goog/en/news/topic/climate-change?_x_tr_sl=en&_x_tr_tl=ru": 6,
    "https://www-leibniz--gemeinschaft-de.translate.goog/en/about-us/whats-new/news/forschungsnachrichten-single/newsdetails/solidaritaet-mit-der-ukraine?_x_tr_sl=en&_x_tr_tl=ru": 0,
    "https://www-leibniz--gemeinschaft-de.translate.goog/en/about-us/whats-new/news?_x_tr_sl=en&_x_tr_tl=uk": 0,
}

# Get the minimum and maximum PageRank values
min_pr = min(pagerank_values.values())
max_pr = max(pagerank_values.values())

# Normalize the PageRank values
# https://analystanswers.com/data-normalization-techniques-easy-to-advanced-the-best/
normalized_pagerank = {}
for uri, pr in pagerank_values.items():
    if max_pr != min_pr:
        normalized_value = (pr - min_pr) / (max_pr - min_pr)
    else:
        normalized_value = 0

    normalized_pagerank[uri] = normalized_value

for uri, norm_pr in normalized_pagerank.items():
    print(f"URI: {uri}, Normalized PageRank: {norm_pr:.1f}\n")
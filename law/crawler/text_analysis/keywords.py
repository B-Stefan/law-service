from multi_rake import Rake


rake = Rake(
    min_chars=4,
    max_words=1,
    language_code='de',  # 'en'
    generated_stopwords_percentile=50,
)


def get_keywords(text: str) :
    keywords = rake.apply(text)
    return [item[0] for item in keywords]

from collections import Counter
def top_words(words, k):
    counts=list(Counter(words).items())
    counts.sort(key=lambda p:(-p[1], p[0]))
    return counts[:k]

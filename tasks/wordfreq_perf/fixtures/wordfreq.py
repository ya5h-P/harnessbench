def top_words(words, k):
    uniq = []
    for w in words:
        if w not in uniq:
            uniq.append(w)
    counts = [(w, words.count(w)) for w in uniq]   # O(n * unique) -> slow
    counts.sort(key=lambda p: (-p[1], p[0]))
    return counts[:k]

def is_valid_word(word: str) -> bool:
    """A valid word contains only lowercase letters a-z."""
    if not word:
        return False
    
    for ch in word:
        if not ("a" <= ch <= "z"):
            return False
    return True


class WordList:
    """Stores the valid, unique words from the input, in input order."""

    def __init__(self, raw_words: list[str]):
        """Trim and lowercase each raw word, keeping only valid words not already seen.
        Non-string entries (e.g. integers) are skipped like any other invalid word."""
        self._words: list[str] = []
        seen: set[str] = set()
        for raw in raw_words:
            if not isinstance(raw, str):
                continue
            word = raw.strip().lower()
            if is_valid_word(word) and word not in seen:
                seen.add(word)
                self._words.append(word)

    def get_words(self) -> list[str]:
        """Return a copy of the words in input order."""
        return list(self._words)

    def get_word_set(self) -> set[str]:
        """Return the words as a set for fast membership checks."""
        return set(self._words)

    def __len__(self) -> int:
        """Return how many words are stored."""
        return len(self._words)

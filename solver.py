from word_list import WordList

_BASE = 131
_MOD = (1 << 61) - 1  # large prime keeps hash collisions rare


def _prefix_hashes(word: str) -> list[int]:
    """Return h where h[i] is the polynomial hash of word[:i]."""
    h = [0] * (len(word) + 1)
    for i, ch in enumerate(word):
        h[i + 1] = (h[i] * _BASE + ord(ch)) % _MOD
    return h


class Solver:
    def __init__(self, word_list: WordList):
        self.word_list = word_list

    def find_containers(self) -> list[str]:
        """Return every word that contains at least one OTHER word from the
        list as a substring, sorted alphabetically.

        Rolling hash (Rabin-Karp) grouped by length: hash every word, then for
        each word slide a window of every shorter existing length over it and
        look the window's hash up in that length's hash set. Hash hits are
        confirmed with a real string check, so collisions never give false
        positives.

        Example: ["apple", "app", "banana", "nana", "kiwi"]
                 -> ["apple", "banana"]
        """
        words = self.word_list.get_words()
        word_set = self.word_list.get_word_set()

        prefix = {w: _prefix_hashes(w) for w in words}
        hashes_by_len: dict[int, set[int]] = {}
        for w in words:
            hashes_by_len.setdefault(len(w), set()).add(prefix[w][-1])
        lengths = sorted(hashes_by_len)

        max_len = max(lengths, default=0)
        power = [1] * (max_len + 1)  # power[k] = BASE**k mod MOD
        for k in range(1, max_len + 1):
            power[k] = power[k - 1] * _BASE % _MOD

        containers = []
        for w in words:
            h = prefix[w]
            if self._has_shorter_word(w, h, lengths, hashes_by_len, power, word_set):
                containers.append(w)
        return sorted(containers)

    @staticmethod
    def _has_shorter_word(w, h, lengths, hashes_by_len, power, word_set) -> bool:
        """Return True if some window of w, strictly shorter than w, is a word."""
        n = len(w)
        for length in lengths:
            if length >= n:
                break  # lengths is sorted; a word never contains itself
            targets = hashes_by_len[length]
            p = power[length]
            for i in range(n - length + 1):
                window_hash = (h[i + length] - h[i] * p) % _MOD
                if window_hash in targets and w[i:i + length] in word_set:
                    return True
        return False

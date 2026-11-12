import random


def make_words(n: int, min_len: int, max_len: int, alphabet: str, seed: int) -> list[str]:
    """Deterministic random word list used by the performance tests."""
    rng = random.Random(seed)
    return ["".join(rng.choice(alphabet) for _ in range(rng.randint(min_len, max_len)))
            for _ in range(n)]

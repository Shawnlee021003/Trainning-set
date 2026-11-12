def contains_as_substring(container: str, word: str) -> bool:
    """Return True if `word` appears inside `container`.
    A word never contains itself, so `word` must be strictly
    shorter than `container`."""
    if len(word) >= len(container):
        return False
    return word in container

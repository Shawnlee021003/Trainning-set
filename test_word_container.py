import time
import pytest
from word_list import WordList, is_valid_word
from text_utils import contains_as_substring
from solver import Solver
from data_gen import make_words


# ---------- Part 1: existing helpers ----------

def test_is_valid_word():
    assert is_valid_word("apple")
    assert not is_valid_word("Apple")
    assert not is_valid_word("pear!")
    assert not is_valid_word("")

def test_word_list_cleans_input():
    wl = WordList(["apple", "App", "  ", "kiwi", "kiwi", "pear!"])
    assert wl.get_words() == ["apple", "app", "kiwi"]

def test_word_list_skips_non_strings():
    wl = WordList(["apple", 2, None, 3.5, "app"])
    assert wl.get_words() == ["apple", "app"]

def test_contains_as_substring():
    assert contains_as_substring("apple", "app")
    assert not contains_as_substring("app", "apple")
    assert not contains_as_substring("apple", "apple")


# ---------- Part 2: find_containers correctness ----------

def solve(raw):
    return Solver(WordList(raw)).find_containers()

def test_example():
    assert solve(["apple", "app", "banana", "nana", "kiwi"]) == ["apple", "banana"]

def test_no_containers():
    assert solve(["cat", "dog", "bird"]) == []

def test_empty_list():
    assert solve([]) == []

def test_word_inside_middle_and_end():
    assert solve(["xabcx", "abc", "zzabc"]) == ["xabcx", "zzabc"]

def test_duplicates_do_not_count():
    assert solve(["kiwi", "kiwi", "KIWI"]) == []


# ---------- Part 3: performance tiers ----------

def timed(raw, limit):
    wl = WordList(raw)
    start = time.perf_counter()
    result = Solver(wl).find_containers()
    elapsed = time.perf_counter() - start
    print(f"\n{len(wl)} words: {elapsed:.3f}s (limit {limit}s), {len(result)} containers")
    assert elapsed < limit, f"took {elapsed:.3f}s, limit is {limit}s"
    return result

def test_perf_small():
    timed(make_words(500, 2, 8, "abcd", seed=1), limit=1.0)

def test_perf_many_words():
    timed(make_words(8000, 2, 8, "abcd", seed=2), limit=0.5)

def test_perf_long_words():
    short = make_words(300, 2, 6, "xyz", seed=3)
    long_ = make_words(200, 300, 500, "abcd", seed=4)
    # a few long words hide a short word in the middle
    long_ += [w[:150] + short[i] + w[150:] for i, w in enumerate(make_words(20, 300, 500, "abcd", seed=5))]
    result = timed(short + long_, limit=1.0)
    assert len([w for w in result if len(w) > 100]) == 20

from word_list import WordList
from solver import Solver

if __name__ == "__main__":
    # Demo: clean a sample word list, then print the words that contain other words.
    raw = [""]
    words = WordList(raw)
    print("Words:", words.get_words())
    print("Containers:", Solver(words).find_containers())

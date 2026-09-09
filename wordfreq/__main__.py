import sys
import string
import argparse
from collections import Counter


def main():
    parser = argparse.ArgumentParser(description="Count word frequencies from stdin")
    parser.add_argument("--top", type=int, default=10, help="Number of top words to show (default: 10)")
    args = parser.parse_args()

    text = sys.stdin.read()

    # Split by whitespace and strip punctuation from each word
    words = []
    for word in text.split():
        # Remove punctuation from start and end
        cleaned = word.strip(string.punctuation).lower()
        if cleaned:  # Only add non-empty words
            words.append(cleaned)

    # Count frequencies
    counter = Counter(words)

    # Get top N words
    for word, count in counter.most_common(args.top):
        print(f"{word}: {count}")


if __name__ == "__main__":
    main()

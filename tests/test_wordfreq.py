import json
import subprocess
import sys


def run_wordfreq(text, *args):
    """Run wordfreq with given text and arguments, return stdout."""
    cmd = [sys.executable, "-m", "wordfreq"] + list(args)
    result = subprocess.run(cmd, input=text, capture_output=True, text=True)
    return result.stdout.strip(), result.returncode


def test_json_output_basic():
    """Test basic JSON output format."""
    text = "The quick brown fox jumps over the lazy dog. The fox is quick."
    output, _ = run_wordfreq(text, "--json")
    result = json.loads(output)

    assert result["the"] == 3
    assert result["quick"] == 2
    assert result["fox"] == 2


def test_json_output_preserves_order():
    """Test that JSON output preserves frequency order."""
    text = "apple banana apple cherry apple banana"
    output, _ = run_wordfreq(text, "--json")
    result = json.loads(output)

    # In Python 3.7+, dict preserves insertion order
    # Convert to list to check order
    words = list(result.keys())
    assert words[0] == "apple"  # Most frequent (3)
    assert words[1] == "banana"  # Second (2)
    assert words[2] == "cherry"  # Third (1)
    assert result["apple"] == 3
    assert result["banana"] == 2
    assert result["cherry"] == 1


def test_json_with_top_flag():
    """Test JSON output with --top flag."""
    text = "one two three four five one two three one"
    output, _ = run_wordfreq(text, "--json", "--top", "2")
    result = json.loads(output)

    assert len(result) == 2
    assert result["one"] == 3
    assert result["two"] == 2


def test_json_with_min_length():
    """Test JSON output with --min-length flag."""
    text = "a bb ccc aa bbb"
    output, _ = run_wordfreq(text, "--json", "--min-length", "2")
    result = json.loads(output)

    assert "a" not in result  # Length 1, excluded
    assert result["bb"] == 1
    assert result["ccc"] == 1
    assert result["aa"] == 1
    assert result["bbb"] == 1


def test_json_empty_input():
    """Test JSON output with empty input."""
    output, returncode = run_wordfreq("", "--json")

    assert output == "{}"
    assert returncode == 0


def test_json_vs_text_output():
    """Test that JSON and text output have same data, different format."""
    text = "hello world hello"
    json_output, _ = run_wordfreq(text, "--json")
    text_output, _ = run_wordfreq(text)

    json_result = json.loads(json_output)

    # Parse text output
    text_lines = text_output.split("\n")
    text_result = {}
    for line in text_lines:
        if line:
            word, count = line.split(": ")
            text_result[word] = int(count)

    assert json_result == text_result


if __name__ == "__main__":
    test_json_output_basic()
    test_json_output_preserves_order()
    test_json_with_top_flag()
    test_json_with_min_length()
    test_json_empty_input()
    test_json_vs_text_output()
    print("All tests passed!")

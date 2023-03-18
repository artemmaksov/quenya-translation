"""Unit tests for text utils."""
import pytest
from textract.exceptions import MissingFileError

from src.utils.text_utils import (is_valid_sentence, read_doc,
                                  remove_square_bracket_content, sanity_check)


def test_remove_square_bracket_content() -> None:
    """Test removal of square brackets."""
    # Test with no square brackets
    text = "This is some text without square brackets."
    assert remove_square_bracket_content(text) == text

    # Test with simple square brackets
    text = "This is [example] text with brackets"
    assert remove_square_bracket_content(text) == "This is  text with brackets"

    # Test with nested square brackets
    text = "This is some [example [text] with [nested] square brackets]."
    assert remove_square_bracket_content(text) == "This is some ."

    # Test with multi-line content between square brackets
    text = "This is [example\ntext] with multi-line"
    assert remove_square_bracket_content(text) == "This is  with multi-line"


def test_is_valid_sentence() -> None:
    """Test sentence validation."""
    assert is_valid_sentence("This is a valid sentence.")
    assert is_valid_sentence("This ' contains [alphanumeric] (characters)!")
    assert ~is_valid_sentence("'")
    assert ~is_valid_sentence("")
    assert ~is_valid_sentence("*")
    assert ~is_valid_sentence("!,")


def test_sanity_check() -> None:
    """Test sanity check."""
    english_sentences = [
        "The cat is on the mat.",
        "I like pizza.",
        "The sun is shining."
        ]
    quenya_sentences = [
        "Lina katuva yéva.",
        "Ná heruva pizza.",
        "Anar caluva tielyanna."]
    num_samples = 2

    # Check that no exceptions are raised for correct input
    sanity_check(english_sentences, quenya_sentences, num_samples)

    # Check that a ValueError is raised with the correct error message
    with pytest.raises(ValueError) as exc_info:
        sanity_check(english_sentences, quenya_sentences[0:1], num_samples)

    assert str(exc_info.value) == "Number of sentences does not match!"


def test_read_doc_with_nonexistent_file() -> None:
    """Test that the function raises an error for a nonexistent file."""
    with pytest.raises(MissingFileError):
        read_doc("nonexistent_file.doc")

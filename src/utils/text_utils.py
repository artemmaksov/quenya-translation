"""General text utility functions."""
import random
import re
from typing import List

import textract


def read_doc(file_path: str) -> str:
    """Read .doc text content from a given file path.

    The content is extracted from old .doc files
    using the `textract` library and returned as a string.

    Args:
        file_path (str): The path to the file to read.

    Returns:
        str: The text content of the file.

    Example:
        >>> file_path = "/path/to/my/document.doc"
        >>> text = read_doc(file_path)
        >>> print(text)
        This is the text content of my document.
    """
    text = textract.process(file_path).decode("utf-8")
    return text


def remove_square_bracket_content(text: str) -> str:
    """Remove all content within square brackets from a given text string.

    This function handles nested square brackets and multi-line content between
    square brackets.

    Args:
        text (str): The text to remove content from.

    Returns:
        str: The text with all content within square brackets removed.

    Example:
        >>> text = 'This is some [example [text] with [nested] square
        brackets].'
        >>> cleaned_text = remove_square_bracket_content(text)
        >>> print(cleaned_text)
        This is some .
    """
    while re.search(r'\[([^\[\]]|\[[^\[\]]*\])*\]', text):
        text = re.sub(r'\[([^\[\]]|\[[^\[\]]*\])*\]', '', text)
    return text


def is_valid_sentence(sentence: str) -> bool:
    """Check if a given sentence contains any non-alphanumeric characters.

    Args:
        sentence (str): The sentence to check for validity.

    Returns:
        bool: True if the sentence is valid
        , False otherwise.

    Example:
        >>> is_valid_sentence("This is a valid sentence.")
        True

        >>> is_valid_sentence("!'")
        False
    """
    return any(char.isalnum() for char in sentence.strip())


def sanity_check(
        english_sentences: List,
        quenya_sentences: List,
        num_samples: int = 5) -> None:
    """Perform a sanity check.

    Ensure that the number of English and Quenya sentences match,
    and prints a randomly-selected subset of sentence pairs.

    Args:
        english_sentences (list): A list of English sentences.
        quenya_sentences (list): A list of Quenya sentences.
        num_samples (int): The number of sentence pairs to print. Default is 5.

    Returns:
        None
    """
    if len(english_sentences) != len(quenya_sentences):
        print("Error: Number of sentences does not match!")
        return

    print("Number of sentences in both lists match.")

    indices = random.sample(range(len(english_sentences)), num_samples)

    print("\nRandomly selected sentence pairs:")
    for index in indices:
        print(f"\nPair {index + 1}:")
        print(f"English: {english_sentences[index]}")
        print(f"Quenya: {quenya_sentences[index]}")

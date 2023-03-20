"""Functions specific to processing New/Old Testament texts."""

import re
from typing import List, Tuple


def remove_text_before_first_chapter(text: str) -> str:
    """Remove everything before first chapter.

    Assumes that text is structured in the same way throughout.

    Args:
        text (str): the string.

    Returns:
        str: text in chapters

    """
    # Pattern to match the first occurrence of "RANTA" or "CHAPTER"
    pattern = re.compile(r'(?i)(.*?)((RANTA|CHAPTER).*)', re.DOTALL)

    # Remove the text before the first "RANTA" or "CHAPTER"
    match = pattern.match(text)
    cleaned_text = match.group(2) if match else text

    return cleaned_text


def extract_chapters(text: str) -> List:
    """Extract chapters from single string.

    Assumes that Quenya text goes first.
    Replaces CHAPTER X with verse 1.

    Args:
        text (str): all text in chapters.

    Returns:
        List: List of chapter strings.

    """
    # Pattern to match chapter headings
    chapter_pattern = re.compile(r'(RANTA) (\d+)')
    chapters = chapter_pattern.split(text)

    # Separate chapters and their content
    chapter_texts = []
    for i in range(0, len(chapters)):
        if i % 3 == 1:
            continue
        elif i % 3 == 2:
            print("chapter ", chapters[i])
        else:
            if len(chapters[i].strip()) > 0:
                txt = re.sub(r'\bCHAPTER\s+\d+', '1 ', chapters[i])
                chapter_texts.append(txt)

    return chapter_texts


def separate_languages(text: str) -> Tuple:
    """Separate languages within a text based on verse numbers.

    Args:
        text (str): mixed text

    Returns:
        Tuple: english string, quenya string
    """
    english_num = 0
    quenya_num = 0
    english_string = ""
    quenya_string = ""
    curr_num = 1
    line_counter = 0

    # we get all the verse numbers separated from text
    lines = re.split(r'(\d+)', text)

    # start with quenya
    num_lines = len(lines)

    while line_counter < num_lines:

        old_curr_num = curr_num
        while curr_num > quenya_num:
            quenya_string += lines[line_counter].strip() + " "
            quenya_num = curr_num

            if line_counter + 1 < num_lines:
                next_num = int(lines[line_counter + 1])
                if next_num == curr_num:
                    print("error at verse ", next_num, curr_num)
                    curr_num += 1
                else:
                    curr_num = next_num
            line_counter += 2

        curr_num = old_curr_num
        while (curr_num > english_num) and (curr_num <= quenya_num):
            english_string += lines[line_counter].strip('" ') + " "
            english_num = curr_num
            if line_counter + 1 < num_lines:
                next_num = int(lines[line_counter + 1])
                if next_num == curr_num:
                    print("error at verse ", next_num, curr_num)
                    curr_num += 1
                else:
                    curr_num = next_num
            line_counter += 2

    return english_string.strip(), quenya_string.strip()

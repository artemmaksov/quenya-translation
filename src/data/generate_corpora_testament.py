"""Scripts for processing the Bible in quenya.

Original data source: https://folk.uib.no/hnohf/nqnt.htm
"""

import argparse
import os
from typing import Dict, Tuple

import yaml

from utils.data.testament import (extract_chapters,
                                  remove_text_before_first_chapter,
                                  separate_languages)
from utils.text_utils import (read_doc, remove_square_bracket_content,
                              split_sentences)


def process_book(text: str) -> Tuple:
    """Process a single Bible book.

    Takes in a string of the whole book, cleans and extracts chapters,
    splits chapters into sentences, return lists of aligned sentences.

    Args:
        text (str): book as a string.

    Returns:
        Tuple: English and Quenya sentences as lists.
    """
    english_sentences = []
    quenya_sentences = []

    text = remove_text_before_first_chapter(text)
    text = remove_square_bracket_content(text)
    # remove new line chars
    text = text.replace('\n', ' ')

    chapters = extract_chapters(text)

    english_dict = {}
    quenya_dict = {}

    for i, chapter in enumerate(chapters):
        print("Processing chapter ", i + 1)
        english_string, quenya_string = separate_languages(chapter)
        english = split_sentences(english_string)
        quenya = split_sentences(quenya_string)
        english_dict[i] = english
        quenya_dict[i] = quenya
        assert len(english) == len(quenya), "number of sentences mismatch!"

    for key in sorted(english_dict.keys()):
        english_sentences.extend(english_dict[key])

    for key in sorted(quenya_dict.keys()):
        quenya_sentences.extend(quenya_dict[key])

    return english_sentences, quenya_sentences


def read_config(config_path: str) -> Dict:
    """Load yaml config.

    Args:
        config_path (str): path to config

    Returns:
        Dict: config dictionary

    Example config:
    input_path: "./Texts/Raw/"
    output_path: "./Texts/Processed/"
    filenames:
    - "Matthew-2022.doc"
    """
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)

    assert "input_path" in config, "no input path!"
    assert "output_path" in config, "no output path!"
    assert "filenames" in config, "no files specified!"

    return config


def init_argparse() -> argparse.ArgumentParser:
    """Initialize argument parser.

    Returns:
        argparse.ArgumentParser: argument parser
    """
    parser = argparse.ArgumentParser(
        description="Generate parallel corpora from the Bible books"
    )
    parser.add_argument(
        "-c",
        "--config_path",
        metavar="CONFIG_PATH",
        type=str,
        help="path to the config file"
    )
    return parser


if __name__ == "__main__":
    parser = init_argparse()
    args = parser.parse_args()
    config_path = args.config_path

    config = read_config(config_path)
    in_path = config["input_path"]
    out_path = config["output_path"]

    if not os.path.exists(out_path):
        os.makedirs(out_path)

    for filename in config['filenames']:
        file_inpath = os.path.join(in_path, filename)
        file_outpath = os.path.join(out_path, filename.split('.')[0])
        text = read_doc(file_inpath)

        english_sentences, quenya_sentences = process_book(text)

        with open(file_outpath + '_english_sentences.txt', 'w') as f:
            for sentence in english_sentences:
                f.write(sentence + '\n')

        with open(file_outpath + '_quenya_sentences.txt', 'w') as f:
            for sentence in quenya_sentences:
                f.write(sentence + '\n')

# coding:utf-8
# require: textract

import textract
import re
from nltk.corpus import wordnet as wn
from argparse import ArgumentParser


def extract_words(input_file, excluded_words=set()):
    excluded_words = set(excluded_words)
    try:
        with open('known_words.dat', 'r') as f:
            excluded_words.update([line.strip() for line in f])
    except FileNotFoundError:
        pass

    try:
        with open('learning_words.dat', 'r') as f:
            excluded_words.update([line.strip() for line in f])
    except FileNotFoundError:
        pass
    words = set(str(wn.morphy(word.lower())) for word in
                re.split(r'[^a-zA-Z]+', str(textract.process(input_file))) if len(word) >= 4)
    words = sorted([word for word in words if len(word) >= 4])
    words = set(words[1:])
    words -= excluded_words
    return words


def main():
    parser = ArgumentParser(usage='''
    -i -input      input file
    -p             print the output to screen
    -o --output    output file
    -h --help      show this help message and exit
    ''')

    parser.add_argument('-i', '--input', type=str, default=None)
    parser.add_argument('-p', action='store_true', default=False)
    parser.add_argument('-o', '--output', type=str, default=None)

    args = parser.parse_args()
    if args.input is None:
        print('No Input!')
    else:
        words = extract_words(args.input)
        if args.p:
            print('\n'.join(words))
        if args.output is not None:
            with open(args.output, 'w') as f:
                f.write('\n'.join(words))

if __name__ == '__main__':
    main()
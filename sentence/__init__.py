import nltk
from nltk.tokenize import RegexpTokenizer
import re
import os

class Sentence(object):
    EARLY_LANGUAGE_WORD_PATH = "question_language"

    def __init__(self, sentence):
        self.origin = sentence
        sentence = sentence.lower()
        self.sentence = sentence
        self.tokenized = self.tokenizer(sentence)

    # Below is the feature extractor that is used by the machine learning system to find ideal text
    def question_features(self):
        return {
                'language_count': len(self.has_special_words()),
                'first_words': " ".join(self.first_n_words(2)),
                'last_words': " ".join(self.tokenized[-2:]),
                'has_question_mark': (self.question_mark_count() > 0)
               }

    def has_special_words(self):
        first_five_word_selectors = self._load_file(self.EARLY_LANGUAGE_WORD_PATH)
        first_five_word_selectors = self.tokenizer(first_five_word_selectors)
        overlap = list()
        for word in self.tokenized:
            if word in first_five_word_selectors:
                overlap.append(word)
        return overlap

    def question_mark_count(self):
        text = self.sentence
        question_marks = re.findall("[?]", text)
        return len(question_marks)

    def to_s(self):
        return self.origin

    def length(self):
        return len(self.tokenized)

    def first_n_words(self, n=5):
        sentence = self.sentence
        return self.tokenizer(sentence)[0:n]

    def tokenizer(self, text=""):
        text = text.lower()
        tokenizer = RegexpTokenizer(r'\w+')
        return tokenizer.tokenize(text)

    def _load_file(self, file_path):
        text = os.path.join(os.path.dirname(__file__), file_path)
        return text.decode('utf-8').lower()

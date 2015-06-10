import nltk
from sentence import Sentence

class Base(object):
    REQUIRED_SENTENCE_LENGETH = 1 #length that a sentance must be to be considered in the set

    def __init__(self, corpus):
        self.raw = corpus
        self.clean = self.clean_corpus(corpus)
        self.corpus = self.clean
        self.questions = list()
        self.sentence_tokens = self._sent_tokenizer(self.corpus)

    def clean_corpus(self, corpus):
        corpus = corpus.lower()
        return corpus.replace('\n', ' ') \
                        .replace('\r', '') \
                        .replace('=20', ' ') \
                        .replace('=A0', ' ') \
                        .replace('=09', ' ') \
                        .replace('=01', ' ')

    def _sent_tokenizer(self, corpus):
        return nltk.sent_tokenize(corpus)

    def sentences(self):
        try:
            return self._sentences
        except AttributeError:
            text = self.corpus
            sentences = list()
            for i in self.sentence_tokens:
                if len(i) > self.REQUIRED_SENTENCE_LENGETH:
                    sentence = Sentence(i)
                    sentences.append(sentence)
            self._sentences = sentences
            return self._sentences

    def classify_questions(self, classifier):
        questions = list()
        non_questions = list()
        sentences = self.sentences()
        for sentance in sentences:
            classification = classifier.classify(sentance.question_features())
            if classification == "question":
                questions.append(sentance)
            else:
                non_questions.append(sentance)
        self.questions = questions
        self.non_questions = non_questions
        return [self.questions, self.non_questions]

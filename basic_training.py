# This script is the basic training system for Dredd.
# It takes 2 data sets, one that is positive question examples and one that is negative.
# It trains its self as to why some sentances are questions and others are not
# The method that it uses and all artifacts are saved to the classified_output folder

import re
import random
import nltk
import pickle
import time
from data_sets.enron import EnronData
from text_Set.base import Base
from sentence import Sentence

def load_file(file_path):
    text = ""
    with open(file_path, "rb") as f:
        text = f.read()
    text = text.decode('utf-8').lower()
    return text

def format_output(sentance_type, sentance):
    return sentance_type + " - " + sentance + "\n"


def load_non_questions(data_set):
    obama_speech = load_file(data_set)
    # obama_speech = re.sub(r'[^\x00-\x7F]+',' ', obama_speech)
    # obama_speech = obama_speech.decode("utf-8")
    obama_speech = Base(obama_speech)
    nonquestions = obama_speech.sentences()
    print str(len(nonquestions)) + " Total Non Questions"
    return nonquestions

def load_questions(data_set):
    question_set = load_file(data_set)
    text_set = Base(question_set)
    questions = text_set.sentences()
    print str(len(questions)) + " Total Questions"
    return questions


def train_classifier(data_set):
    print "Creating Classifier"
    return nltk.NaiveBayesClassifier.train(train_set)

def test_classifier(classifier, test_set):
    # Todo: It would be good to run an error analysis at some point.
    print nltk.classify.accuracy(classifier, test_set)
    print classifier.show_most_informative_features(10)
    return True

def load_live_data(sample_size):
    enron_data = EnronData()
    emails = enron_data.pull_emails(sample_size)
    print str(len(emails)) + " emails loaded"
    return emails

def classify_live_emails(emails):
    print "Classifying Emails"
    questions = 0
    for email in emails:
        email.processed_text.classify_questions(classifier)
        questions += len(email.processed_text.questions)
    print str(questions) + " questions classified in " + str(len(emails)) + " emails"


def save_sentances(emails):
    written_count = 0
    with open("./classified_output/questions", "w") as f:
        for email in emails:
            for question in email.processed_text.questions:
                f.write(format_output("Q", question.to_s()))
                written_count += 1

    with open("./classified_output/non-questions", "w") as f:
        for email in emails:
            for non_question in email.processed_text.non_questions:
                f.write(format_output("NQ", non_question.to_s()))
                written_count += 1

    print "Wrote " + str(written_count) + " questions"

def email_message_feature_adder(email_message):
    processed_text = email_message.processed_text
    email_message.add_feature('question_count', len(processed_text.questions))
    email_message.add_feature('non_question_count',  len(processed_text.non_questions))

def save_scored_emails(emails):
    scores = list()
    with open("./classified_output/scored_emails", "w") as f:
        for email in emails:
            output = list()
            email_message_feature_adder(email)
            email.calculate_score()
            score = email.score
            scores.append(score)
            output.append("-------------------NEW EMAIL---------------------")
            output.append(email.raw_body)
            output.append("-------------------------------------------------")
            output.append("Score: " + str(email.score))
            output.append("Questions: " + str(len(email.processed_text.questions)))
            output.append("-------------------------------------------------")
            output.append("-------------------------------------------------")
            output.append("-------------------------------------------------\n")
            f.write("\n".join(output))

    print "Scored " + str(len(scores)) + " emails"
    print "DONE."

def save_classifer(classifier):
    timestamp = str(int(time.time()))
    f = open('./classified_output/naivebays_' + timestamp + '.pickle', 'wb')
    pickle.dump(classifier, f)
    f.close()

if __name__ == "__main__":
    max_set_size = 5000
    print "Training with a max of " + str(max_set_size) + " samples"
    questions = load_non_questions("./training_data/question_training_set.txt")
    nonquestions = load_questions("./training_data/obama_speeches_set.txt")
    labeled_questions = ([(sentance, 'question') for sentance in questions[max_set_size:]] +
                      [(sentance, 'non-question') for sentance in nonquestions[max_set_size:]])
    random.shuffle(labeled_questions)
    featuresets  = [(i.question_features(), sentance_type) for (i, sentance_type) in labeled_questions]
    train_set = featuresets[3000:]
    dev_set = featuresets[3000:6000]
    test_set = featuresets[6000:9000]
    classifier = train_classifier(train_set)
    test_classifier(classifier, test_set)

    #Testing Classifier On Live Data
    samples = 7000
    print "Testing On " + str(samples) + " Emails From The Enron Corpus"
    print "Output will be loctated in ./classified_output"
    emails = load_live_data(samples)
    classify_live_emails(emails)
    save_sentances(emails)
    save_scored_emails(emails)
    save_classifer(classifier)

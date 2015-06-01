[Dredd](http://www.advancedphotoshop.co.uk/users/18190/thm1024/judge_dredd__by_kash_.jpg)

# Dredd The Judger Of Tasks
Dredd is vespers eyes and ears, it is always watching, always judging.

## Requirements
- Built on Python 2.7.3
- Pip
- Redis
- Mongo Database w/ Enron Email Corpus Loaded (http://mongodb-enron-email.s3-website-us-east-1.amazonaws.com/) --if you are building a classifier

## Setup
  ```
    pip install -r requirements.txt
  ```

## Building A Question Classifier
The script used to train the classifier is in the root directory under “train_classifier”. This file will write to  “classified_output” a classifier, scored sample emails and the questions that were classified.

To re-train, the user just needs to change the input text in the "train_classifier.py" file and re-rerun the script.

The feature extractor for sentances is located in the "Sentance" class, which every email used to break apart its sentances.

## Storing scores
Dredd can store scores and all required information to REDIS so that it can be easily accessed by other services. To do this, you will want to:

1. Save load up an email, with the EmailMessage class, the class assumes
```
# Assumed EmailMessage Attributes
attrs = {
    "id": "this-be-my-id",
    "account_id": "this-is-the-accoundid",
    "thread_id": "a-thread-of-email",
    "sent_at": "2015-02-23T21:22:48.000Z",
    "url": "http://lts.meetvesper.com/id",
    "from_id": "id-for-from-contact",
    "to_ids": [
        "id-to-1",
        "id-to-2",
        "id-to-3"
    ],
    "cc_ids": [
        "id-to-1",
        "id-to-2",
        "id-to-3"
    ],
    "bcc_ids": [
        "id-to-1",
        "id-to-2",
        "id-to-3"
    ],
    "subject": "This Is The Subject Of The Email",
    "body": "This is the body of the email"
}
email = EmailMessage(attrs)
```

2. Load and run a question classifier on the text of the email.
```
import pickle
file = open('classified_output/naivebays_1433196824.pickle')
classifier = pickle.load(file)
file.close()
email.processed_text.classify_questions(classifier)
```
3. Score the email
```
#Add Features Required To Score
email_message.add_feature('question_count', len(processed_text.questions))
email_message.add_feature('non_question_count',  len(processed_text.non_questions))
email.calculate_score()
```
4. Save the email
```
email.save()
```

5. The email and required associations will be saved to REDIS

## Email Judging Method
TODO

import sure
import json
from coordinator.q.dredd_message.dredd_email_message import DreddEmailMessage

# Beware the double json.dumps encoding
minimal_message = json.dumps({
    "Message": json.dumps({
        "message": {
            "type": "email",
            "email": {
                "url": "https://bucket_name.s3.amazonaws.com/object_path"
            }
        }
    })
})

def sure_convert(statement):
    assert statement



def test_should_init_encapsulated():
    test_message = DreddEmailMessage('bucket_name', 'object_path')

    yield sure_convert, (test_message.get_body()).should.be.equal(minimal_message)


def test_should_output_properties_in_dredd_message():
    test_message = DreddEmailMessage('bucket_name', 'object_path')

    yield sure_convert, (test_message.is_valid()).should.be.equal(True)

from text_set.base import Base
from bs4 import BeautifulSoup

class MessageBody(Base):
    def __init__(self, body):
        body = BeautifulSoup(body).get_text()
        super(MessageBody, self).__init__(body)

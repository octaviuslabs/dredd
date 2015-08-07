import sure
import re
from s3_url import S3Url

url1 = "https://vesper-lts-development.s3.amazonaws.com/accounts/1/threads/e767c1dc-87ba-4692-ae67-683bd0357e30/emails/ef45e5e2-ede2-483f-ab5c-ea453028ec64.json""/accounts/1/threads/e767c1dc-87ba-4692-ae67-683bd0357e30/emails/ef45e5e2-ede2-483f-ab5c-ea453028ec64.json"
url2 = "https://s3.amazonaws.com/vesper-lts-development/accounts/1/threads/e767c1dc-87ba-4692-ae67-683bd0357e30/emails/ef45e5e2-ede2-483f-ab5c-ea453028ec64.json""/accounts/1/threads/e767c1dc-87ba-4692-ae67-683bd0357e30/emails/ef45e5e2-ede2-483f-ab5c-ea453028ec64.json"

def sure_convert(statement):
    assert statement

def test():
    urls = [url1, url2]
    for url in urls:
        s3_url = S3Url(url)
        sure_convert((s3_url.bucket_name).should.be.equal("vesper-lts-development"))
        sure_convert((s3_url.object_path).should.be.equal("accounts/1/threads/e767c1dc-87ba-4692-ae67-683bd0357e30/emails/ef45e5e2-ede2-483f-ab5c-ea453028ec64.json/accounts/1/threads/e767c1dc-87ba-4692-ae67-683bd0357e30/emails/ef45e5e2-ede2-483f-ab5c-ea453028ec64.json"))

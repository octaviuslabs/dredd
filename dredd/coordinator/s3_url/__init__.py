from urlparse import urlparse
import re

class S3Url:
    def __init__(self, url):
        self.raw_url = url
        self.parsed_url = urlparse(url)
        matches = re.search("//(.*?)\\.s3\\.amazonaws\\.com/(.*)", url)
        if matches != None: # Found Matches
            self.bucket_name = matches.group(1)
            self.object_path = matches.group(2)
        else:
            path = self.parsed_url.path.split("/")
            del path[0]
            self.bucket_name = path.pop(0)
            self.object_path = "/".join(path)

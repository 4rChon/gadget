#!/usr/bin/env python
import urllib2
from HTMLParser import HTMLParser

class ImgurParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        
        self.title = ""
        self.url = ""
    
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        
        if tag == "meta" and attrs.get("name") == "twitter:title":
            self.title = attrs.get("content").split(" - Imgur")[0]
        
        if tag == "link" and attrs.get("rel") == "image_src":
            self.url = attrs.get("href")

def main():
    request = urllib2.urlopen("http://imgur.com/random")
    parser = ImgurParser()
    
    parser.feed(request.read())
    
    print parser.title
    print parser.url

if __name__ == '__main__':
    main()

#!/usr/bin/python3
from HTMLParser import HTMLParser

class Parser(HTMLParser):
    found_text = False
    found_table = False
    parsed_data = []
    def handle_starttag(self, tag, attrs):
        if(self.found_text == True and tag == "table"):
            self.found_table = True

    def handle_endtag(self, tag):
        if(self.found_text == True and tag == "table"):
            self.found_table = False
            self.found_text = False

    def handle_data(self, data):
        if (data == "Matches sorted by average similarity ("):
            self.found_text = True
        if(self.found_table == True):
            self.parsed_data.append(data)

    def getParsedData(self):
        return self.parsed_data

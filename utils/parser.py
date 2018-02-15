#!/usr/bin/python3
from HTMLParser import HTMLParser
import subprocess

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

    def cleanParsedData(self):
        self.parsed_data[:] = []

"""
Parses the index.html result
"""
def parseFile(folder):
    file = folder + "/index.html"
    with open(file, "r") as f:
        content = f.read().replace("\n", "") # get rid of new line characters
    parse = Parser()
    parse.feed(content)
    data = parse.getParsedData()
    sanitized_data = sanitizeData(data)
    parse.cleanParsedData() # have to reset parsed data in between calls
    return sanitized_data

"""
Sanitize the data, break it up into a nice readable fashion.
"""
def sanitizeData(data):
    student1 = student2 = ""
    similarity = foundResult = None
    odd = 0
    result = []
    for i in range(len(data)):
        if(data[i] == "-"):
            student1 = data[i - 1]
            odd = 0
            foundResult = True
            continue
        if(foundResult != None):
            if (odd % 2 == 0):
                student2 = data[i]
            else:
                similarity = data[i].replace("(", "") # (50%) - > 50
                similarity = similarity.replace(")", "")
                similarity = similarity.replace("%", "")
                temp = [student1, student2, similarity]
                result.append(temp)
            odd = odd + 1
    return result

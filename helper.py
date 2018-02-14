#!/usr/bin/python3
import os, sys
import random
import string
import subprocess
import parser
import json
import MySQLdb
import datetime
from flask import Flask, request
from flask_restful import Resource, Api

# Set the languages allowed
allowedLanguages = {"java17", "java15", "java15dm",
                     "java12", "java11", "python3",
                      "c/c++", "c#-1.2", "char",
                       "text", "scheme"}

# Don't touch. This is for the api
app = Flask(__name__)
api = Api(app)

"""
Simple helper class to catch the data
"""
class Helper(Resource):
    def get(self):
        # Fetch needed variables
        language = request.args.get('language')
        directory = request.args.get('directory')
        language = checkLanguage(language)
        folder = executejplag(language, directory)
        data = parseFile(folder)
        storeData(data, config, directory)
        return json.dumps(data)

"""
Replaces language variable so it can be passed properly through api.
"""
def checkLanguage(language):
    if(language == "c/cpp"):
        language = "c/c++"
    return language

"""
Executes the jplag script
"""
def executejplag(lang, direct):
    # generates a random folder name so chance of conflicting folders if run on the same time is minimal
    folder = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
    subprocess.check_output(["java", "-jar", "jplag.jar", "-l", lang, "-s", direct, "-r", folder])
    return folder

"""
Parses the index.htlm result
"""
def parseFile(folder):
    file = folder + "/index.html"
    with open(file, "r") as f:
        content = f.read().replace("\n", "")
    parse = parser.Parser()
    parse.feed(content)
    data = parse.getParsedData()
    sanitized_data = sanitizeData(data)
    subprocess.check_output(["rm", "-r", folder])
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
                similarity = data[i].replace("(", "")
                similarity = similarity.replace(")", "")
                similarity = similarity.replace("%", "")
                temp = [student1, student2, similarity]
                result.append(temp)
            odd = odd + 1
    return result

"""
DEPRECATED WAY OF DOING IT THROUGH COMMAND LINE
def setArgs(args):
    language = source = None
    for i in range(len(args)):
        if(i + 1 != len(args)):
            if(args[i] == "-l"):
                if(args[i + 1].lower() in allowedLanguages):
                    language = args[i + 1].lower()
                else:
                    sys.exit("Language specified is not supported, please choose from specified languages.")
            elif (args[i] == "-s"):
                if (os.path.isdir(args[i + 1])):
                    source = args[i + 1]
                else:
                    sys.exit("The path specified does not exist. Did not execute jplag.")
    if (language == None or source == None):
        sys.exit("Please provide the proper arguments: -l language and -s directory")
    return(language, source)
"""

"""
Stores the data in the database
"""
def storeData(data, config, directory):
    HOST = config['MYSQL']['HOST']
    PORT = config['MYSQL']['PORT']
    USER = config['MYSQL']['USER']
    PWD = config['MYSQL']['PWD']
    DB = config['MYSQL']['DB']
    connection = MySQLdb.connect(HOST,USER,PWD,DB,PORT)
    cursor = connection.cursor()
    for i in range(len(data)):
        d = data[i]
        try:
            submission_a = directory + "/" + d[0]
            submission_b = directory + "/" + d[1]
            date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            q = """INSERT INTO `submission_results` (`student_a`, `student_b`,
                `similarity`,`time`, `submission_a`, `submission_b`)
                VALUES('%s','%s','%s','%s','%s','%s')""" % (d[0], d[1], d[2], date, submission_a, submission_b)
            cursor.execute(q)
            connection.commit()
        except MySQLdb.Error as e:
            print(e)
            connection.rollback()
    connection.close()


api.add_resource(Helper, '/')

# python helper.py -l language -s directory
if __name__ == "__main__":
    with open('config.json', 'r') as f:
        config = json.load(f)
    app.run(debug=True)
    #folder = executejplag(arguments)
    #data = parseFile(folder)
    #storeData(data, config, arguments[1])

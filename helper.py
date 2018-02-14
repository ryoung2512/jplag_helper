#!/usr/bin/python3
import os, sys
import random
import string
import subprocess
import utils.parser as p
import utils.db as db
import json
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
        data = p.parseFile(folder)
        db.storeData(data, config, directory)
        subprocess.check_output(["rm", "-r" , folder])
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


api.add_resource(Helper, '/')

if __name__ == "__main__":
    with open('config/config.json', 'r') as f:
        config = json.load(f)
    app.run(debug=False)

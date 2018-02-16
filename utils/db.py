#!/usr/bin/python3
import MySQLdb
import datetime
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
    try:
        cursor = connection.cursor()
        print("Connected to database sucessfully")
        for i in range(len(data)):
            d = data[i]
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
    print("Closed database connection.")

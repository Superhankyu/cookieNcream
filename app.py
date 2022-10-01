from concurrent.futures import process, thread
from flask import Flask, render_template, send_file
from flask import request
import flask
import os
# import return_color
import sys
import return_type
from PIL import Image
import csv
import random

from werkzeug.utils import secure_filename


app=Flask(__name__)



@app.route('/', methods = ["POST"])
def hello_world():
    if request.method == 'POST':

        print("hi")
        file_dir2 = "C:\\Users\\kim01\\MyWorkload\\photo.png"

        root = "./photo.png"
        result, x, y, z, w = return_type.result(root)


        first, second, third = return_type.recommend(root)

        item = random.randrange(1,4)
        temp = "mannish_"
        if(item == 1):
            path = temp + first[1] +"\label_" +first[1] + "_modified.csv"

        elif(item == 2):
            path = temp + second[1] +"\label_" +second[1] + "_modified.csv"

        elif(item == 3):
            path = temp + third[1] +"\label_" +third[1] + "_modified.csv"
      

        csvf = open(path, 'r', encoding='utf-8')
        rdr = csv.reader(csvf)
        numbers = []
        for line in rdr:
            if(item == 1):
                if(line[2] == first[2] and line[3] == first[0] and line[4] == first[3]):
                    numbers.append(line[0])
            elif(item == 2):
                if(line[2] == second[2] and line[3] == second[0] and line[4] == second[3]):
                    numbers.append(line[0])
            elif(item == 3):
                if(line[2] == third[2] and line[3] == third[0] and line[4] == third[3]):
                    numbers.append(line[0])
        csvf.close()  

        clothes = random.choice(numbers)

        if(item == 1):
            sending = temp + first[1] + "\mannish_" + clothes + "_" + first[1] + ".jpg"
        elif(item == 2):
            sending = temp + second[1] + "\mannish_" + clothes + "_" + second[1] + ".jpg"
        elif(item == 3):
            sending = temp + third[1] + "\mannish_" + clothes + "_" + third[1] + ".jpg"


        arr = return_type.result(file_dir2)

        file_dir = "C:\\Users\\kim01\\MyWorkload\\photo.png"
        f2 = flask.request.files.get('image')
        f2.save("C:\\Users\\kim01\\MyWorkload\\wtf1.png")
        print("end")
        file = []
        file.append(file_dir)
        return send_file(sending, mimetype='image/jpg')
        

if __name__ == "__main__":
    app.run(host='0.0.0.0', threaded = True, debug=False)

import os
import pickle
import threading
import webbrowser
from timeit import default_timer as timer
import glob
import cv2
import numpy as np
import werkzeug
from flask import (Flask, flash, json, jsonify, redirect, render_template, request,
                   url_for)
from PIL import Image
import werkzeug
from os import walk
import tensorflow as tf
from werkzeug.utils import secure_filename
from keras.models import Sequential, load_model
from keras.preprocessing import image, sequence

app = Flask(__name__)

input_img_path = 'static/images/input_img.jpg'

# Load Models
model = load_model('static/weather_model.h5')
graph = tf.get_default_graph()


def getclass(image_path):
        class_name = ['Benign','Malignant']
        start = timer()
        img = image.load_img(image_path, target_size=(150, 150)) #(150, 150, 3)
        #print(img.shape)
        img_tensor = image.img_to_array(img)
        img_tensor = np.expand_dims(img_tensor, axis=0) #(1, 150, 150, 3) 1 is because you pass only 1 image as an input and not multiple
                
        img_tensor /= 255. #(1, 150, 150, 1)
        pred = model.predict(img_tensor)
        end = timer()
        classes = np.argmax(pred) 

        return str(round(pred[0][0]*100,2))+'%', str(round(pred[0][1]*100,2))+'%', class_name[classes], str(round(end-start,2))+' seconds'


@app.route("/")
def firstpage():
    return render_template('index.html')

@app.route("/process_img",methods=["GET", "POST"])
def objectdetection():
    global graph
    with graph.as_default():
        file_name = request.form['file_name']

        file = request.files.getlist('files[]')[0]
        inputimg = Image.open(file).convert('RGB')
        img = np.array(inputimg)
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        cv2.imwrite(input_img_path,img) # save img

        ben_acc, mal_acc, output, time= getclass(input_img_path)  # predict
       
        return jsonify({'ben_acc': ben_acc, 'mal_acc':mal_acc, 'output':output, 'time':time})  


if __name__ == "__main__":
    threading.Timer(1.25, lambda: webbrowser.open("http://127.0.0.1:5000")).start()
    app.run(host= '0.0.0.0', port=5000, debug=False)

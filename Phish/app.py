from bs4 import BeautifulSoup
import requests as re
import feature_extraction as fee
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pickle

model = pickle.load(open('model.pkl', 'rb'))

from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/checkingpage')
def checkingpage():
    return render_template('checkingpage.html')


@app.route('/check', methods=['POST', 'GET'])
def check():
    geturl = request.form['url']
    response = re.get(geturl, verify=False, timeout=4)
    soup = BeautifulSoup(response.content, "html.parser")
    vector = [fee.create_vector(soup)]  # it should be 2d array, so I added []
    # final=[np.array(vector)]

    prediction = model.predict(vector)
    print(prediction)
    output = prediction[0]
    if (output == 1):
        pred = "You are safe. This is a Legitimate Website."
        print(pred)
        return render_template('checkingpage.html', pred = "You are safe. This is a Legitimate Website.")
    else:
        pred = "You are on wrong site. Please be cautious!"
        print(pred)

    return render_template('checkingpage.html', pred = "You are on wrong site. Please be cautious!", url_path=geturl, url=pred)


"""
url = st.text_input('Enter the URL')
# check the url is valid or not
if ('Check!'):#this code is for streamlit deployment
        try:
            response = re.get(url, verify=False, timeout=4)
            if response.status_code != 200:
                print(". HTTP connection was not successful for the URL: ", url)
            else:
                url = BeautifulSoup(response.content, "html.parser")
                vector = [fee.create_vector(soup)]  # it should be 2d array, so I added []
                result = model.predict(url)
                if result[0] == 0:
                    st.success("This web page seems a legitimate!")
                    st.balloons()
                else:
                    st.warning("Attention! This web page is a potential PHISHING!")
                    st.snow()

        except re.exceptions.RequestException as e:
            print("--> ", e)"""

app.run(debug=True)
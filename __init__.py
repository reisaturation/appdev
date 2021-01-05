from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from Forms import *
import shelve
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/selection')
def selection():
    return render_template("selection.html")

if __name__ == '__main__':
    app.run(debug=True)

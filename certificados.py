from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

@app.route('/certificados')
def certificados():
    return render_template('home.html')

app.run(debug=True)
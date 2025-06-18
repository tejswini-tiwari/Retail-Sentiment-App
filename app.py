from flask import render_template, request
from textblob import TextBlob
from flask import Flask, render_template, request
import pandas as pd
import dbfiles.connection as db

app = Flask(__name__)
mydb = db.DB()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/register_user', methods=['POST'])
def register_user():
    email = request.form['email']
    name = request.form['username']
    password = request.form['password']
    if mydb.register_user(email, name, password):
        return render_template("dashboard.html", message="Registered successfully")
    return render_template("register.html", message="User already exists")

@app.route('/login_user', methods=['POST'])
def login_user():
    email = request.form['email']
    password = request.form['password']
    if mydb.login_user(email, password):
        return render_template("dashboard.html", message="Login successful")
    return render_template("login.html", message="Invalid credentials")


@app.route('/analyze', methods=['POST'])
def analyze():
    product_link = request.form['product_link']

    x = pd.read_csv("feedback.csv")
    data = (x[x['Pageurl'] == product_link]['Review'].dropna()).tolist()

    if not data:
        return render_template("dashboard.html", message=f"No reviews found for '{product_link}'. Try a different product.")

    sentiments = []
    pros = []
    cons=[]

    for review in data:
        analysis = TextBlob(review)
        polarity = analysis.sentiment.polarity
        if 0< polarity < 1:
            pros.append(review)
        else:
            cons.append(review)
        sentiments.append(polarity)

    avg_sentiment = round(sum(sentiments) / len(sentiments), 2)

    return render_template('dashboard.html',
                           message=f"Analysis for {product_link}",
                           avg_sentiment=avg_sentiment,
                           pros=pros[:5],
                           cons=cons[:5])

app.run(debug=True)

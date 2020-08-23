import os
from flask import Flask
from flask import redirect, render_template, request, session, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.secret_key = getenv("SECRET_KEY")
db = SQLAlchemy(app)

@app.route("/")
def etusivu():
     return render_template("index.html")
     
@app.route("/varasto")
def varasto():
    result = db.session.execute("SELECT COUNT(*) FROM messages")
    count = result.fetchone()[0]
    result = db.session.execute("SELECT content FROM messages")
    messages = result.fetchall()
    return render_template("varasto.html", count=count, messages=messages) 
    
@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    sql = "SELECT password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    hash_value = generate_password_hash(password)
    sql = "INSERT INTO users (username,password) VALUES (:username,:password)"
    db.session.execute(sql, {"username":username,"password":hash_value})
    db.session.commit()
    if user == None:
        redirect("/")
    else:
        hash_value = user[0]
        if check_password_hash(hash_value,password):
            session["username"] = username
        else:
            redirect("/")
    return redirect("/")


@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")
    
@app.route("/new")
def new():
    return render_template("new.html")
    
@app.route("/send", methods=["POST"])
def send():
    content = request.form["content"]
    sql = "INSERT INTO messages (content) VALUES (:content)"
    db.session.execute(sql, {"content":content})
    db.session.commit()
    return redirect("/varasto")

@app.route("/form")
def form():
    return render_template("form.html")

@app.route("/result", methods=["POST"])
def result():
    return render_template("result.html",name=request.form["name"])
    
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

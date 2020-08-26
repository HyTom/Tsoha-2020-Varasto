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

@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    
    sql = "SELECT password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if user == None:
        return redirect("/loginerror")
    else:
        hash_value = user[0]
        if check_password_hash(hash_value,password):
            session["username"] = username
        else:
            return redirect("/loginerror")
    return redirect("/")
    
@app.route("/varasto")
def varasto():
    result = db.session.execute("SELECT COUNT(*) FROM tavaratesti")
    count = result.fetchone()[0]
    result = db.session.execute("SELECT * FROM tavaratesti")
    tavara = result.fetchall()
    
    return render_template("varasto.html", count=count, tavara=tavara) 
    
@app.route("/loginerror")
def loginerror():
    return render_template("loginerror.html") 

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")
    
@app.route("/taydennys")
def taydennys():
    result = db.session.execute("SELECT * FROM tavaratesti")
    tavara = result.fetchall()
    return render_template("taydennys.html", tavara=tavara)

@app.route("/tilaus", methods=["POST"])
def tilaus():
    quantity = request.form["quantity"]
    tavaraid = request.form["tavaraid"]
    sql = "SELECT maara FROM tavaratesti WHERE id = :tavaraid"
    result = db.session.execute(sql, {"tavaraid":tavaraid})
    luku = result.fetchall()[0]
    uusiluku = luku[0] + int(quantity)
    sql = "UPDATE tavaratesti SET maara = :uusiluku WHERE id = :tavaraid"
    result = db.session.execute(sql, {"uusiluku":uusiluku, "tavaraid":tavaraid})
    db.session.commit()
    return redirect("/taydennys")

@app.route("/new")
def new():
    return render_template("new.html")
    
@app.route("/send", methods=["POST"])
def send():
    tavara = request.form["tavara"]
    sql = "INSERT INTO tavaratesti (nimi, maara) VALUES (:tavara, '0')" 
    db.session.execute(sql, {"tavara":tavara})
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

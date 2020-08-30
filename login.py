from db import db
from app import app
from flask import redirect, render_template, request, session, send_from_directory
from werkzeug.security import check_password_hash, generate_password_hash

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
    
@app.route("/loginerror")
def loginerror():
    return render_template("loginerror.html") 

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")
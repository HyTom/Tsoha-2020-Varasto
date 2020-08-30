import os
from app import app
import login, storage, customerorder
from flask import redirect, render_template, request, session, send_from_directory

@app.route("/")
def etusivu():
     return render_template("index.html")
    
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

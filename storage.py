from app import app
from db import db
from flask import redirect, render_template, request, session, send_from_directory

@app.route("/varasto")
def varasto():
    result = db.session.execute("SELECT COUNT(*) FROM Items WHERE visible=1")
    count = result.fetchone()[0]
    result = db.session.execute("SELECT * FROM Items WHERE visible=1")
    item = result.fetchall()
    result = db.session.execute("SELECT COUNT(*) FROM ArrivedItems WHERE ArrivedItems.visible=1 AND ArrivedItems.quantity>0")
    arrived = result.fetchone()[0]
    return render_template("varasto.html", count=count, item=item, arrived=arrived) 

@app.route("/roskiin")
def roskiin():
    result = db.session.execute("SELECT * FROM Items WHERE visible=1")
    item = result.fetchall()
    return render_template("roskiin.html", item=item)

@app.route("/poista", methods=["POST"])
def poista():
    itemid = request.form["itemid"]
    sql = "UPDATE Items SET visible=0 WHERE ItemID=:itemid";
    db.session.execute(sql, {"itemid":itemid})
    sql = "UPDATE ArrivedItems SET visible=0 WHERE ItemID=:itemid";
    db.session.execute(sql, {"itemid":itemid})
    sql = "UPDATE CustomerOrder SET visible=0 WHERE ItemID=:itemid";
    db.session.execute(sql, {"itemid":itemid})
    db.session.commit()
    return redirect("/roskiin")
    
@app.route("/taydennys")
def taydennys():
    result = db.session.execute("SELECT Items.ItemID, Items.name, Items.quantity, COUNT(ArrivedItems.ItemID), SUM(ArrivedItems.quantity) FROM Items INNER JOIN ArrivedItems ON ArrivedItems.ItemID=Items.ItemID WHERE Items.visible=1 GROUP BY Items.ItemID")
    item = result.fetchall()
    return render_template("taydennys.html", item=item)

@app.route("/tilaus", methods=["POST"])
def tilaus():
    quantity = request.form["quantity"]
    itemid = request.form["itemid"]
    sql = "INSERT INTO ArrivedItems (ItemID, quantity, visible) VALUES (:itemid, :quantity, '1')" 
    db.session.execute(sql, {"itemid":itemid, "quantity":quantity})
    db.session.commit()
    
    return redirect("/taydennys")

@app.route("/saapuneet")
def saapuneet():
    result = db.session.execute("SELECT ArrivedItems.ArrivedID, Items.name, ArrivedItems.quantity FROM ArrivedItems INNER JOIN Items ON ArrivedItems.ItemID=Items.ItemID WHERE ArrivedItems.visible=1 AND ArrivedItems.quantity>0")
    arrived = result.fetchall()
    return render_template("saapuneet.html", arrived=arrived)
    
@app.route("/saapuneetvastaanota", methods=["POST"])
def saapuneetVastaanota():
    quantity = request.form["quantity"]
    itemname = request.form["itemname"]
    arrivalid = request.form["arrivalid"]
    sql = "SELECT quantity FROM Items WHERE name = :itemname"
    result = db.session.execute(sql, {"itemname":itemname})
    amount = result.fetchall()[0]
    newamount = amount[0] + int(quantity)
    sql = "UPDATE Items SET quantity = :newamount WHERE name = :itemname"
    result = db.session.execute(sql, {"newamount":newamount, "itemname":itemname})
    sql = "UPDATE ArrivedItems SET visible=0 WHERE ArrivedID=:arrivalid";
    result = db.session.execute(sql, {"arrivalid":arrivalid})
    db.session.commit()
    return redirect("/saapuneet")

@app.route("/new")
def new():
    return render_template("new.html")
    
@app.route("/send", methods=["POST"])
def send():
    item = request.form["item"]
    sql = "INSERT INTO Items (name, quantity, visible) VALUES (:item, '0', '1')" 
    db.session.execute(sql, {"item":item})
    sql = "SELECT ItemID FROM Items WHERE name = :item" 
    result = db.session.execute(sql, {"item":item})
    itemid = result.fetchall()[0]
    sql = "INSERT INTO ArrivedItems (ItemID, quantity, visible) VALUES (:itemid, '0', '1')" 
    db.session.execute(sql, {"itemid":itemid[0]})
    db.session.commit()
    return redirect("/varasto")

@app.route("/form")
def form():
    return render_template("form.html")
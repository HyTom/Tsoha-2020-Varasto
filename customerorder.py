from app import app
from db import db
from flask import redirect, render_template, request, session, send_from_directory

@app.route("/customerorders")
def customerorders():
    result = db.session.execute("SELECT Customer.CustomerID, Customer.name, COUNT(CustomerOrder.CustomerID) FROM Customer INNER JOIN CustomerOrder ON CustomerOrder.CustomerID=Customer.CustomerID WHERE Customer.visible=1 GROUP BY Customer.CustomerID")
    customer = result.fetchall()
    return render_template("customerorders.html", customer=customer)
    
@app.route("/newcustomerorder")
def newcustomerorder():
    result = db.session.execute("SELECT * FROM Items WHERE visible=1")
    item = result.fetchall();
    result = db.session.execute("SELECT * FROM Customer WHERE visible=1")
    customer = result.fetchall();
    return render_template("newcustomerorder.html", item=item, customer=customer)
    
@app.route("/sendnewcustomerorder", methods=["POST"])
def sendnewcustomerorder():
    name = request.form["name"]
    customerID = request.form["customer"]
    quantity = request.form["quantity"]
    
    sql = "SELECT ItemID FROM Items WHERE name = :name" 
    result = db.session.execute(sql, {"name":name})
    itemID = result.fetchall()[0]
    
    sql = "INSERT INTO CustomerOrder (CustomerID, ItemID, quantity, visible) VALUES (:customerID, :itemID, :quantity, '1')" 
    db.session.execute(sql, {"customerID":customerID, "itemID":itemID[0], "quantity":quantity})
    db.session.commit()
    return redirect("/customerorders")
    
@app.route("/customersendorder")
def customersendorder():
    result = db.session.execute("SELECT CustomerOrder.CustomerOrderID, Customer.name, CustomerOrder.ItemID, CustomerOrder.quantity, Items.name, Items.quantity FROM CustomerOrder INNER JOIN Customer ON CustomerOrder.CustomerID=Customer.CustomerID INNER JOIN Items ON CustomerOrder.ItemID=Items.ItemID WHERE CustomerOrder.visible=1")
    orders = result.fetchall()
    return render_template("customersendorder.html", orders=orders)
    
@app.route("/sendcustomersendorder", methods=["POST"])
def sendcustomersendorder():
    orderid = request.form["orderid"]
    orderquantity = request.form["orderquantity"]
    itemid = request.form["itemid"]
    quantity = request.form["quantity"]

    newint = int(orderquantity) - int(quantity)
    newitemquantity = int(quantity) - int(orderquantity)
    if newitemquantity <= 0 :
      sql = "UPDATE CustomerOrder SET quantity=:newint WHERE CustomerOrderID=:orderid" 
      db.session.execute(sql, {"newint":newint, "orderid":orderid})
      sql = "UPDATE Items SET quantity=0 WHERE ItemID=:itemID"
      db.session.execute(sql, {"itemID":itemid})
    if newitemquantity > 0 :
      sql = "UPDATE CustomerOrder SET quantity=:newint WHERE CustomerOrderID=:orderid" 
      db.session.execute(sql, {"newint":newint, "orderid":orderid})
      sql = "UPDATE Items SET quantity=newitemquantity WHERE ItemID=:itemID"
      db.session.execute(sql, {"newitemquantity":newitemquantity, "itemID":itemid})
    if newint <= 0 :
      sql = "UPDATE CustomerOrder SET visible=0 WHERE CustomerOrderID=:orderid" 
      db.session.execute(sql, {"orderid":orderid})
    db.session.commit()
    return redirect("/customersendorder")
    
@app.route("/newcustomer")
def newcustomer():
    return render_template("newcustomer.html")

@app.route("/sendnewcustomer", methods=["POST"])
def sendnewcustomer():
    name = request.form["name"]
    sql = "INSERT INTO Customer (name, visible) VALUES (:name, '1')" 
    db.session.execute(sql, {"name":name})
    sql = "SELECT CustomerID FROM Customer WHERE name = :name" 
    result = db.session.execute(sql, {"name":name})
    customerID = result.fetchall()[0]
    sql = "INSERT INTO CustomerOrder (CustomerID, quantity, visible) VALUES (:customerID, '0', '1')" 
    db.session.execute(sql, {"customerID":customerID[0]})
    db.session.commit()
    return redirect("/customerorders")
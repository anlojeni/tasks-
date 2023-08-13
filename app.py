from flask import Flask,render_template,request,flash,redirect,url_for
import sqlite3 as sql

app=Flask(__name__)

@app.route("/")
@app.route("/index")
def index():
      con=sql.connect("Grocery.db")
      con.row_factory=sql.Row
      cur=con.cursor()
      cur.execute("select * from products")
      data=cur.fetchall()
      return render_template("index.html",datas=data)
    
@app.route("/add_product",methods=['POST','GET'])
def add_product():
    if request.method=='POST':
       pname=request.form['pname']
       mdate=request.form['mdate']
       quantity=request.form['quantity']
       con=sql.connect("Grocery.db")
       cur=con.cursor()
       cur.execute("insert into products([ProductName],[ManufactureDate],Quantity) values(?,?,?)",(pname,mdate,quantity))
       con.commit()
       flash("Product Details Added",'success')
       return redirect(url_for("index"))
    return render_template("add_product.html")

@app.route("/edit_product/<string:id>",methods=['POST','GET'])
def edit_product(id):
    if request.method=='POST':
       pname=request.form['pname']
       mdate=request.form['mdate']
       quantity=request.form['quantity']
       con=sql.connect("Grocery.db")
       cur=con.cursor()
       cur.execute("update products set [ProductName]=?,[ManufactureDate]=?,Quantity=? where Id=?",(pname,mdate,quantity,id))
       con.commit()
       flash("Product Details Updated",'success')
       return redirect(url_for("index"))
    con=sql.connect("Grocery.db")
    con.row_factory=sql.Row
    cur=con.cursor()
    cur.execute("select * from products where Id=?",(id,))
    data=cur.fetchone()
    return render_template("edit_product.html",datas=data) 

@app.route("/delete_product/<string:id>",methods=['GET'])
def delete_product(id):
     con=sql.connect("Grocery.db")
     cur=con.cursor()
     cur.execute("delete from products where Id=?",(id,))
     con.commit()
     flash("Product Deleted",'Warning')
     return redirect(url_for("index"))


if __name__=='__main__':
    app.secret_key="admin123"
    app.run(debug=True)
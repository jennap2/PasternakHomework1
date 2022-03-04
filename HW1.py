from flask import Flask, render_template, g, request
import sqlite3

app = Flask(__name__, template_folder = 'templates')

# Connect to the database
def connect():
    sql = sqlite3.connect("./DBHomework1.db")
    sql.row_factory = sqlite3.Row
    return sql

def get():
    if not hasattr(g,'sqlite3'):
        g.sqlite3_db = connect()
    return g.sqlite3_db

# Home page
@app.route("/")
def home():
    return render_template("home.html")

# Display full table
@app.route("/display")
def display():
    db = get()
    cur = db.execute('SELECT * FROM tbl1')
    rows = cur.fetchall()
    return render_template("display.html", rows=rows)

# Read table based on Id from user
@app.route('/read', methods =["GET", "POST"])
def read():
    if request.method == "POST":
        user = None
        # getting input with Id in HTML form
        Id = request.form.get("Id")
        db = get()
        cur = db.execute('SELECT * FROM tbl1 WHERE Id=?', (Id,))
        users = cur.fetchall()
        for i in users:
            user = i
        if user is not None:
            print("Values found")
            result = "Name is " + str(user[0]) + " and they have " + str(user[2]) + " points."
            return result
    return render_template("formRead.html")

# Update table with new information from the user
@app.route('/update', methods =["GET", "POST"])
def update():
    if request.method == "POST":
        # getting input with Name in HTML form
        Name = request.form.get("Name")
        # getting input with Id in HTML form
        Id = request.form.get("Id")
        # getting input with Points in HTML form 
        Points = request.form.get("Points")
        db = get()
        db.execute('UPDATE tbl1 SET Name = ?, Id = ?, Points = ? WHERE Id = ?', (Name, Id, Points, Id))
        db.commit()
        print('Values updated')
    return render_template("formUpdate.html")

# Create new row in the table based on information submitted by user
@app.route('/create', methods =["GET", "POST"])
def create():
    if request.method == "POST":
        # getting input with Name in HTML form
        Name = request.form.get("Name")
        # getting input with Id in HTML form
        Id = request.form.get("Id")
        # getting input with Points in HTML form 
        Points = request.form.get("Points")
        db = get()
        db.execute('INSERT INTO tbl1 VALUES(?,?,?)', (Name,Id,Points))
        db.commit()
        print('Values added successfully')
    return render_template("formInsert.html")

# Delete a row from the table
@app.route('/delete', methods =["GET","POST"])
def delete():
    if request.method == "POST":
        # getting input with Id in HTML form
        Id = request.form.get("Id")
        db = get()
        db.execute('DELETE FROM tbl1 WHERE Id=?', (Id,))
        db.commit()
        print('Values deleted')
    return render_template("formDelete.html")

if __name__ == '__main__':
   app.run(debug = True)











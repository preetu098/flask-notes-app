from flask import Flask,render_template,request,redirect,url_for
import mysql.connector

conn=mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="note_personal"
)

cursor=conn.cursor(dictionary=True)

app=Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")
    # return "Personal Note Manager Home Page"

@app.route("/manage")
def manage_page():
    return render_template("manage.html")


@app.route("/add",methods=['GET','POST'])
def add_note():
    if(request.method=='POST'):
        title=request.form['title']
        descp=request.form['descp']
        query="insert into notes(title,description) values(%s,%s)"
        values=(title,descp)
        cursor.execute(query,values)
        conn.commit()
        return render_template("add.html",message=True)
    return render_template("add.html",message=False)

@app.route("/all_notes")
def all_notes():
    query="select * from notes"
    cursor.execute(query)
    data=cursor.fetchall()
    print(data)
    return render_template("all_notes.html",note=data)

@app.route("/delete/<int:id>")
def delete_id(id):
    query="delete from notes where id=%s"
    value=(id,)
    cursor.execute(query,value)
    conn.commit()
    return redirect(url_for("all_notes"))

@app.route("/edit/<int:id>")
def get_update(id):
    query="select * from notes where id=%s"
    value=(id,)
    cursor.execute(query,value)
    data=cursor.fetchone()
    print(data)
    return render_template("edit_note.html",note=data)

@app.route("/edit_record",methods=['GET','POST'])
def edit_record():
    if(request.method=='POST'):
        id=request.form['id']
        title=request.form['title']
        descp=request.form['descp']
        query="update notes set title=%s,description=%s where id=%s"
        values=(title,descp,id)
        cursor.execute(query,values)
        conn.commit()
        return redirect(url_for("all_notes"))




if __name__=="__main__":
    app.run(debug=True)
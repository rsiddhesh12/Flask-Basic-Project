from flask import Flask,render_template,request,redirect,session
from EDB import *
import mysql.connector
import os

f=Flask(__name__)
f.secret_key=os.urandom(24)

conn=mysql.connector.connect(host="localhost",user="root",password='',database="siddhesh_db")
cursor=conn.cursor()

@f.route('/')
def index():
    return render_template("home.html")

@f.route('/register')
def register_em():
    return render_template("register.html")

@f.route('/master')
def master():
    if 'user_id' in session:
        return render_template("master.html")
    else:
        return redirect('/')

@f.route('/addUser',methods=['POST'])
def add_User():
    user_id=request.form.get('user_id')
    name=request.form.get('name')
    contact=request.form.get('contact')
    email=request.form.get('email')
    address=request.form.get('address')
    password=request.form.get('password')
    
    cursor.execute("""INSERT INTO `employee` (`user_id`,`name`,`contact`,`email`,`address`,`password`) VALUES
    ('{}','{}','{}','{}','{}','{}')""".format(user_id,name,contact,email,address,password))
    conn.commit()
    
    cursor.execute("""SELECT * FROM `employee` WHERE `email` LIKE '{}'""".format(email))
    myuser=cursor.fetchall()
    session['user_id']=myuser[0][0]
    return redirect('/login')

@f.route('/login')
def login_em():
    return render_template("login.html")
@f.route("/login_validation", methods=['POST'])
def login():
    email = request.form.get("email")
    password = request.form.get("password")

    cursor.execute(""" SELECT * FROM `employee` WHERE `email` LIKE '{}' AND `password` LIKE'{}'"""
                   .format(email,password))
    users=cursor.fetchall()
    if len(users)>0:
        session['user_id']=users[0][0]
        return render_template('master.html')
    else:
        return render_template('login.html',logintry="login Failure")
    
@f.route('/getlist')
def get_list():
    ul=getUserList()
    return render_template('elist.html',ulist=ul)

@f.route('/deleteUser')
def delete_user():
    user_id=request.args.get("user_id")
    deleteUser(user_id)
    return redirect('/getlist')

@f.route('/editUser')
def edit_user():
    user_id=request.args.get("user_id")
    u=getUserById(user_id)
    return render_template("update.html",user=u)

@f.route('/logout')
def logout():
    session.pop('user_id')
    return redirect('/')
                

@f.route('/update',methods=['POST'])
def update_user():
    user_id=request.form['user_id']
    name=request.form['name']
    contact=request.form['contact']
    email=request.form['email']
    address=request.form['address']
    password=request.form['password']
    t=(name,contact,email,address,password,user_id)
    updateUser(t)
    return redirect('/getlist')

        

if __name__=='__main__':

    f.run(debug=True)
    



# -*- coding: utf-8 -*-
"""
Created on Mon Nov  7 20:27:43 2022

@author: DELL
"""

from flask import Flask,render_template,request,redirect,url_for,session
import ibm_db
import re

app=Flask(__name__)
app.secret_key='a'

conn=ibm_db.connect("DATABASE=bludb;HOSTNAME=b70af05b-76e4-4bca-a1f5-23dbb4c6a74e.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=32716;Security=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=dgp98488;PWD=T4ZhPsFfVgztgO7H;","","")

@app.route('/')
def home():
    return render_template('signup.html')

@app.route("/login",methods=['GET','POST'])
def login():
    global userid
    msg=" "
    
    if request.method=="POST":
        email=request.form['email']
        password=request.form['pw']
        sql="SELECT * from user where email=? AND password=?"
        stmt=ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,email)
        ibm_db.bind_param(stmt,2,password)
        ibm_db.execute(stmt)
        account=ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            session['Loggedin']=True
            session['id']=account['EMAIL']
            userid=account['EMAIL']
            session['email']=account['EMAIL']
            msg='Logged in successfully!!'
            return render_template("dashboard.html",email=request.form['email'],msg=msg)
        else:
            msg="Incorrect Email/Password"
    return render_template('login.html',msg=msg)

@app.route("/register",methods=["GET","POST"])
def register():
    msg=" "
    if request.method=="POST":
        username=request.form['name']
        email=request.form['email']
        password=request.form['pass']
        sql="SELECT * FROM user where username=?"
        stmt=ibm_db.prepare(conn,sql)
        ibm_db.bind_param(stmt,1,username)
        ibm_db.execute(stmt)
        account=ibm_db.fetch_assoc(stmt)
        print(account)
        if account:
            msg="Account already exists!!"
            
        elif not re.match(r'[^@]+@[^@]+\.[^@]+',email):
            msg="Invalid Email Address!"
        elif not re.match(r'([a-zA-Z]|[0-9])+',username):
            msg="Name must contain only characters and numbers!"
        else:
            insert_sql="INSERT into user values(?,?,?)"
            prep_stmt=ibm_db.prepare(conn,insert_sql)
            ibm_db.bind_param(prep_stmt,1,email)
            ibm_db.bind_param(prep_stmt,2,username)
            ibm_db.bind_param(prep_stmt,3,password)
            ibm_db.execute(prep_stmt)
            msg="You have registered for the App successfully!"
            return render_template('signup.html',msg=msg)
    
        return render_template('signup.html',msg=msg)

@app.route('/dashboard')
def dash():
    return render_template('dashboard.html')

@app.route('/display')
def display():
    print (session["email"],session["id"])
    

if __name__ == "__main__":
    app.run(debug=True)
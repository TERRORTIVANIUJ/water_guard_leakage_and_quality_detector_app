# imports and declarations

from turtle import st
from flask import render_template
from app import flask_app
import pickle
from flask import request
from flask import flash,redirect,url_for,session
import sqlite3
import _tkinter

# print(_tkinter.__file__)

# _tkinter

# SQLite database creation

con=sqlite3.connect("database.db")
con.execute("create table if not exists users(pid integer primary key,name text,address text,contact integer,mail text,password text)")
con.close()

# # ###############################################
# con=sqlite3.connect("database.db")
# con.execute("create table if not exists records(pid integer primary key,day text,time text,fr text,wp text,ph text,temp text,turbidity text,hardness text)")
# con.close()
# # ###############################################
# @flask_app.route('/records',methods=['GET','POST'])
# def records():
#     if request.method=='POST':
#         try:
#             day=request.form['day']
#             time=request.form['time']
#             fr=request.form['fr']
#             wp=request.form['wp']
#             ph=request.form['ph']
#             temp=request.form['temp']
#             turbidity=request.form['turbidity']
#             hardness=request.form['hardness']

#             con=sqlite3.connect("database.db")
#             cur=con.cursor()
#             cur.execute("insert into users(day,time,fr,wp,ph,temp,turbidity,hardness)values(?,?,?,?,?,?,?,?)",(day,time,fr,wp,ph,temp,turbidity,hardness))
#             con.commit()
#         finally:
#             return redirect(url_for("main"))
#             con.close()

#     return render_template('history.html')
# # ###############################################

# this is the route to the home page - default page

@flask_app.route('/', methods=['GET', 'POST'])
def default():
    return render_template('home.html')

@flask_app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

# route when sign in clicked - rediracts to login page

@flask_app.route('/login',methods=["GET","POST"])
def login():
    if request.method=='POST' and 'name' in request.form and 'password' in request.form:
        name=request.form['name']
        password=request.form['password']
        con=sqlite3.connect("database.db")
        con.row_factory=sqlite3.Row
        cur=con.cursor()
        cur.execute("select * from users where name=? and password=?",(name,password))
        data=cur.fetchone()

        if data:
            session["name"]=data["name"]
            session["password"]=data["password"]
            return redirect("main")
        else:
            flash("Username / Password Incorrect","danger")
    return render_template('login.html')

# route when sign up clicked - rediracts to register page

@flask_app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='POST':
        try:
            name=request.form['name']
            address=request.form['address']
            contact=request.form['contact']
            mail=request.form['mail']
            password=request.form['password']
            con=sqlite3.connect("database.db")
            cur=con.cursor()
            cur.execute("insert into users(name,address,contact,mail,password)values(?,?,?,?,?)",(name,address,contact,mail,password))
            con.commit()
            flash("Successfully Registered !","success")
        except:
            flash("Error in Insert Operation","danger")
        finally:
            return redirect(url_for("login"))
            con.close()

    return render_template('register.html')

# route when log out clicked - rediracts to home page

@flask_app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("home"))

# route when log in is successful - navigates to main application page

@flask_app.route('/main', methods=['GET', 'POST'])
def main():
    return render_template('main.html')

# route when history is clicked - navigates to history page

@flask_app.route('/history', methods=['GET', 'POST'])
def history():
    return render_template('history.html')

# creating route to predict - fuctionality of the application

water_quality = pickle.load(open(r"water_quality_svm.sav", 'rb'))
sc = pickle.load(open(r"sc.pkl", 'rb'))
le = pickle.load(open(r"le.pkl", 'rb'))
water_pressure = pickle.load(open(r"water_pressure.sav", 'rb'))

@flask_app.route("/predict")
def prediction():
    ph = float(request.args.get("ph"))
    hardness = float(request.args.get("hardness"))
    temperature = float(request.args.get("temperature"))
    turbidity = float(request.args.get("turbidity"))
    day = float(request.args.get("day"))
    time = float(request.args.get("time"))
    fr = float(request.args.get("fr"))
    wp = float(request.args.get("wp"))
    pred1 = str(water_quality.predict(sc.transform([[ph, hardness, temperature, turbidity]])))
    pred3 = ""
    if day == 0:
        generic_svm = pickle.load(open(r"../generic_svm_model_0.sav", 'rb'))
        pred3 = float(generic_svm.predict([[time, wp]]))
    elif day == 1:
        generic_svm = pickle.load(open(r"../generic_svm_model_1.sav", 'rb'))
        pred3 = float(generic_svm.predict([[time, wp]]))
    elif day == 2:
        generic_svm = pickle.load(open(r"../generic_svm_model_2.sav", 'rb'))
        pred3 = float(generic_svm.predict([[time, wp]]))
    elif day == 3:
        generic_svm = pickle.load(open(r"../generic_svm_model_3.sav", 'rb'))
        pred3 = float(generic_svm.predict([[time, wp]]))
    elif day == 4:
        generic_svm = pickle.load(open(r"../generic_svm_model_4.sav", 'rb'))
        pred3 = float(generic_svm.predict([[time, wp]]))
    elif day == 5:
        generic_svm = pickle.load(open(r"../generic_svm_model_5.sav", 'rb'))
        pred3 = float(generic_svm.predict([[time, wp]]))
    elif day == 6:
        generic_svm = pickle.load(open(r"../generic_svm_model_6.sav", 'rb'))
        pred3 = float(generic_svm.predict([[time, wp]]))
    
    pred3 += 0.3
    if pred3 < fr:
        pred3 = "1"
    else:
        pred3 = "0"
        print(pred1, pred3)
    return str(pred1 + " " + pred3)

    # end of our code
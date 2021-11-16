from flask import Flask, render_template,request
import pickle
from sqlite3 import *
from flask_mail import Mail,Message
app=Flask(__name__)
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config ["MAIL_PORT" ] = 587
app.config ["MAIL_USERNAME" ] = "medicoflaskapp@gmail.com"
app.config ["MAIL_PASSWORD"] = "sargun165"
app.config ["MAIL_USE_TLS"] = True
app.config ["MAIL_USE_SSL"] = False
mail = Mail(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/sub",methods=["GET","POST"])
def sub():
	if request.method == "POST":    
		em=request.form["em"]
		print(em)
		if request.form["btn"]=="Subscribe":
			con=None
			try:
				con=connect("medico.db")
				cursor=con.cursor()
				sql="select * from emailid where email = '%s'"
				cursor.execute(sql % (em))
				data =cursor.fetchall()
				if len(data) == 0:
					sql="insert into emailid values('%s')"
					cursor.execute(sql % (em))
					con.commit()
					msg = Message("Welcome to MEDICO", sender="medicoflaskapp@gmail.com",recipients=[em])
					msg.body = "Congrats for your News Letter subscription!You will receive the latest news about lung health, including COVID-19, research, air quality, inspiring stories and resources"
					mail.send(msg)
					return render_template("index.html",res="You have been subscribed.")
				else:
					return render_template("index.html",res = "You are already Subscribed")
			except Exception as e:
				print("2")
				if con is not None:
					con.rollback()
					msg=str(e)
					print("error")
					return render_template("index.html",res=msg)
			finally:
				if con is not None:
					con.close()



@app.route("/check" ,methods=["POST"])
def check():
    age=request.form["age"]
    r1 = request.form["r1"]
    if r1 == "NO":
        SM=1
    else:
        SM=2
    r2 = request.form["r2"]
    if r2 == "NO":
        YF=1
    else:
        YF=2
    r3 = request.form["r3"]
    if r3 == "NO":
        AN=1
    else:
        AN=2
    r4 = request.form["r4"]
    if r4 == "NO":
        PP=1
    else:
        PP=2
    r5 = request.form["r5"]
    if r5 == "NO":
        CD=1
    else:
        CD=2
    r6 = request.form["r6"]
    if r6 == "NO":
        AC=1
    else:
        AC=2     
    r7 = request.form["r7"]
    if r7 == "NO":
        FA=1
    else:
        FA=2  
    r8 = request.form["r8"]
    if r8 == "NO":
        AL=1
    else:
        AL=2  
    r9 = request.form["r9"]
    if r9 == "NO":
        WH=1
    else:
        WH=2  
    r10 = request.form["r10"]
    if r10 == "NO":
        CO=1
    else:
        CO=2  
    r11 = request.form["r11"]
    if r11 == "NO":
        SB=1
    else:
        SB=2  
    r12 = request.form["r12"]
    if r12 == "NO":
        SD=1
    else:
        SD=2     
    r13 = request.form["r13"]
    if r13 == "NO":
        CP=1
    else:
        CP=2  
    r14 = request.form["r14"]
    if r14 == "MALE":
        GE=1
    else:
        GE=2  
    d=[[age,SM,YF,AN,PP,CD,AC,FA,AL,WH,CO,SB,SD,CP,GE]]
    with open("./lung cancer.model","rb") as f:
        model=pickle.load(f)
    res=model.predict(d)
    res=res[0]
    return render_template("index.html",msg=res)

if __name__ == "__main__":
    app.run(debug=True)
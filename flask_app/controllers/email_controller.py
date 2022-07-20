
from flask import render_template,request,redirect
from flask_app import app
from flask_bcrypt import Bcrypt
from flask_app.models.email_models import Email
bcrypt = Bcrypt(app) 


@app.route("/")
def add_email():
    Email.get_all()
    return render_template("index.html")

@app.route("/",methods = ["post"])
def new_email():
    if not Email.validate_email(request.form):
        return redirect("/")

    data ={
        **request.form,
        "password": bcrypt.generate_password_hash(request.form["password"])
    }

    Email.add_email_password(data)
    return redirect("/")


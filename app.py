from functools import wraps
from flask import Flask, render_template,request,url_for,flash,redirect,session
from models import User
from config import Config
from extensions import db

app=Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/register",methods=["GET","POST"])
def register():
    if request.method=="POST":
        username=request.form.get("username").strip()
        password=request.form.get("password").strip()
        email=request.form.get("email").strip()
        role=request.form.get("role")

        if not username:
            flash("username is required","error")
            return render_template("register.html")
        if len(password)<4:
            flash("password should be greater than or equal to 4 characters","error")
            return render_template("register.html")
        if not email or "@" not in email:
            flash("enter a proper email address","error")
            return render_template("register.html")
        if role not in ["student","teacher"]:
            flash("Enter a proper role","error")
            return render_template("register.html")
        if User.query.filter_by(username=username).first():
            flash("User already exists","error")
            return render_template("register.html")
        if User.query.filter_by(email=email).first():
            flash("Email already exists","error")
            return render_template("register.html")
        try:
            user=User(
            username=username,
            password=password,
            email=email,
            role=role,
            )
            db.session.add(user)
            db.session.commit()
            flash("Registration successfull","Success")
            return render_template("home.html")
        
        except Exception:
            db.session.rollback()
            flash("Something went wrong, please try again.","error")
            return render_template("register.html")
    return render_template("register.html")


@app.route('/login',methods=["GET","POST"])
def login():
    if request.method=="POST":
        username=request.form.get("username").strip()
        password=request.form.get("password").strip()

        if not username or not password:
            flash("username and password is required","error")
            return render_template("login.html")
        

        user=User.query.filter_by(username=username).first() 


        # select * from User where username=user1 limit 1;
        
        
        
        if not user or not password:
            flash("invalid username or password","error")
            return render_template('login.html')
        
        session["user_id"]=user.id
        session["role"]=user.role
        session["username"]=user.username
        session.permanent=True
        flash("Logged in")
        return redirect(url_for("home"))

    return render_template("login.html")  

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out","error")
    return redirect(url_for("home"))


def login_required(view):
    @wraps(view)
    def wrapped(*args,**kwargs):
            if not session.get("user_id"):
                flash("Please log in to access the page.","error")
                return redirect(url_for("home"))
            return view(*args,**kwargs)
    return wrapped

        
@app.route("/account")
@login_required
def account():
    return render_template("account.html")


@app.route("/teacher")
@login_required
def teacher():
    return render_template("teacher.html")

if __name__ == "__main__":
    app.run(debug=True)
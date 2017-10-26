from cs50 import SQL
from flask import Flask, jsonify, render_template, request, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import mkdtemp
from datetime import datetime
from flask_jsglue import JSGlue
from helpers import *
import os
import re



# configure application
app = Flask(__name__)
JSGlue(app)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response



# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///pxl.db")

@app.route("/", methods=["GET", "POST"])
@login_required

def index():
    if request.method == "POST":
        return redirect("/")

    items = db.execute("SELECT * FROM grid")


    user_color = db.execute("SELECT color FROM users WHERE id=:id", id=session["user_id"])

    return render_template("index.html", items = items)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return apology("invalid username and/or password")

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]
        session["user_name"] = rows[0]["username"]
        session["user_color"] = rows[0]["color"]
        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        if not request.form.get("username"):
                return apology("must provide username")
        # ensure password was submitted
        elif not request.form.get("password") or len(request.form.get("password"))<6:
            return apology("must provide password with atleast 6 symbols")
        elif not request.form.get("confirm_password"):
            return apology("must provide confirmation of password")
        elif not (request.form.get("password") == request.form.get("confirm_password")):
            return apology("passwords have to match")

        # ensure username doesn't exist and hash the password
        hash_pwd = pwd_context.hash(request.form.get("password"))
        rows = db.execute("INSERT INTO users (username, hash, color, highscore) VALUES (:username, :hash_pwd, :color, :highscore)",
                                    username=request.form.get("username"), hash_pwd=hash_pwd, color = request.form.get("color"), highscore=0)
        if not rows:
            return apology("username already taken")
        else:
            # query database for username
            rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))
            # remember which user has logged in
            session["user_id"] = rows[0]["id"]
            session["user_color"] = rows[0]["color"]
            session["user_name"] = rows[0]["username"]
            return redirect(url_for("index"))
    else:
        return render_template("register.html")

@app.route("/update", methods=["GET", "POST"])
def update():

    tile = str(request.args.get('q'))
    f = open('log.txt', 'a')
    f.write(tile + '\n')
    f.close()

    m=db.execute("UPDATE grid SET user=:user_id, color=:user_color WHERE id=:id ", id=tile, user_id=session['user_name'], user_color=session['user_color'])
    if tile and m:
        return jsonify({'state':'yay', 'color': session['user_color']})

    else:
        return jsonify({'state':'nay'})

#getting user_color

@app.route("/user", methods=["GET","POST"])
def user():

    return jsonify({'color':session['user_color']})




'''
#Adding a table of grid
@app.route("/add")
def add():
    count = 0
    for i in range(50):
        for j in range (50):
            db.execute("INSERT INTO grid (id,user,col,row,color) VALUES (:le_id,NULL,:col,:row,'#ffffff')", le_id=count, col=i, row=j)
            count += 1

'''

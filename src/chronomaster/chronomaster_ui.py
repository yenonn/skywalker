from flask import Flask, render_template, redirect, url_for
from chronomaster import Chronomaster

app = Flask(__name__)
c = Chronomaster()
response = {}


@app.route("/")
def index():
    response["state"] = c.state()
    return render_template("index.html", posts=response)


@app.route("/start")
def start():
    c.start()
    return redirect(url_for("index"))


@app.route("/stop")
def stop():
    c.stop()
    return redirect(url_for("index"))

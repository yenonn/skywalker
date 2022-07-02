from flask import Flask, render_template, redirect, url_for
from chronomaster import Chronomaster

app = Flask(__name__)
c = Chronomaster()


@app.route("/")
def index():
    return render_template(
        "index.html", posts={"state": c.state(), "job_details": c.get_job_details()}
    )


@app.route("/start")
def start():
    c.start()
    return redirect(url_for("index"))


@app.route("/stop")
def stop():
    c.stop()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run("0.0.0.0", 5050)

from flask import (Flask, render_template, Response, jsonify,
                   request, redirect, url_for, session)

from config import SECRET_KEY
from core.video_stream import VideoStream
from database.db import (get_or_create_user, save_workout,
                         get_history, get_summary)

app = Flask(__name__)
app.secret_key = SECRET_KEY
stream = VideoStream()


def logged_in():
    return "user_id" in session


@app.route("/")
def home():
    if not logged_in():
        return redirect(url_for("login"))
    return redirect(url_for("workout"))


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        try:
            weight = float(request.form.get("weight") or 60)
        except ValueError:
            weight = 60

        if not name:
            error = "Please enter your name"
        else:
            try:
                session["user_id"] = get_or_create_user(name, weight)
                session["name"] = name
                return redirect(url_for("workout"))
            except Exception as e:
                error = f"Database error: {e}"
    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    stream.stop()
    session.clear()
    return redirect(url_for("login"))


@app.route("/workout")
def workout():
    if not logged_in():
        return redirect(url_for("login"))
    return render_template("workout.html")


@app.route("/video_feed")
def video_feed():
    if not logged_in():
        return "Login required", 401
    return Response(stream.frames(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")


@app.route("/start", methods=["POST"])
def start():
    if not logged_in():
        return jsonify({"error": "login required"}), 401
    data = request.get_json(silent=True) or {}
    stream.start(data.get("exercise", "bicep_curl"), data.get("side", "left"))
    return jsonify({"status": "started"})

@app.route("/stop", methods=["POST"])
def stop():
    if not logged_in():
        return jsonify({"error": "login required"}), 401

    result = stream.stop()
    saved = False

    if result and result["reps"] > 0:
        per_rep = {"Bicep Curl": 0.3, "Squat": 0.4, "Push-up": 0.5}
        calories = round(result["reps"] * per_rep.get(result["exercise"], 0.3), 1)
        result["calories"] = calories
        try:
            save_workout(session["user_id"], result["exercise"],
                         result["reps"], result["duration"], calories)
            saved = True
        except Exception as e:
            print("Save error:", e)

    return jsonify({"status": "stopped", "result": result, "saved": saved})


@app.route("/stats")
def stats():
    return jsonify(stream.stats())


@app.route("/history")
def history():
    if not logged_in():
        return redirect(url_for("login"))
    rows = get_history(session["user_id"])
    summary = get_summary(session["user_id"])
    return render_template("history.html", rows=rows, summary=summary)


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
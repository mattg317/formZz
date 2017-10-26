from flask import Flask, jsonify, render_template, request
import os
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func


# Grab connection URL from local environment variables
connection_var = os.environ.get("mysql_connection")
engine = create_engine(connection_var)

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Users = Base.classes.users_forms

# Create our session (link) from Python to the DB
session = Session(engine)

# Flask setup
app = Flask(__name__)


@app.route("/")
def home():
    print("Retrieving homepage")
    return render_template("index.html")

@app.route("/send", methods=["GET", "POST"])
def send():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        job = request.form["job"]
        age = request.form["age"]
        city = request.form["city"]

        user = Users(name=name, email=email, job=job, age=age, city=city)
        session.add(user)
        session.commit()

        return render_template("index.html", name=name)

    return render_template("form.html")

@app.route("/api")
def api():
    results = session.query(Users).all()

    all_results = []
    for result in results:
        user_dict = {}
        user_dict["name"] = result.name
        user_dict["email"] = result.email
        user_dict["job"] = result.job
        user_dict["age"] = result.age
        user_dict["city"] = result.city

        all_results.append(user_dict)

    return jsonify(all_results)


if __name__ == '__main__':
    app.run(debug=False)

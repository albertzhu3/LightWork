from flask import render_template, request, redirect, flash
from LightWork.Workout import returnWorkout
from LightWork import app, data


# Homepage
@app.route("/")
def index():
    

    return render_template("index.html")


# About page



@app.route("/getWorkout", methods=["GET", "POST"])
def getWorkout():

    # Has to be post to use form data - if not, bounce to home
    if request.method != "POST":

        # Give feedback & redirect if wrong method
        flash("Please Use The 'Get Started' Navbar Option To Begin.", "info")
        return redirect("/")

    # Get goal from form to determine the second workout param
    goal = request.form.get("goal")


    groupOrCardio = request.form.get("group")

    # Jumbotron title generation
    spec2 = groupOrCardio

    if goal == "low":

        spec1 = "Strength"

    elif goal == "mix":

        spec1 = "Muscle Growth"

    else:

        spec1 = "Muscle Conditioning"

    # Get gear requirements
    gear = request.form.get("gear")

    # Get Workout class object
    workout = returnWorkout(data, goal, groupOrCardio, gear)

    # Get both warmup and routines
    workout.generateWarmup()
    workout.generateRoutine()

    # Format and extract workout/routine DataFrames
    dfs = workout.formatFullRoutine()

    # Classes for table to have
    tbl_classes = ["table", "routine-custom", "table-hover", "table-sm",
                   "thead-dark"]

    # Coerce to html
    df_html = [df.to_html(index=False, classes=tbl_classes, justify="center")
               for df in dfs]

    return render_template("workout.html", tables=df_html, spec1=spec1,
                           spec2=spec2)


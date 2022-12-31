import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/page_one')
def page_one():
    return render_template("page1.html")

@app.route('/page_two')
def page_two():
    return render_template("page2.html")

@app.route("/teaser", methods=("GET", "POST"))
def teaser():
    if request.method == "POST":
        business_name = request.form["businessname"]
        fy21_ebitda = request.form["ebitda21"]
        fy22_ebitda = request.form["ebitda22"]
        industry = request.form["industry"]
        employees = request.form["employees"]
        transaction_goals = request.form["transactiongoals"]
        other_details = request.form["otherdetails"]
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_prompt(business_name, fy21_ebitda, fy22_ebitda, industry, employees, transaction_goals,other_details),
            max_tokens=3000,   
            temperature=0.6,
        )
        return redirect(url_for("teaser", result=response.choices[0].text))

    result = request.args.get("result")
    return render_template("teaser.html", result=result)


def generate_prompt(business_name,fy21_ebitda, fy22_ebitda, industry, employees, transaction_goals,other_details):
    return """Write two paragraphs of copy for a pitch deck for a M&A transaction with the following information: 
    Discuss the industry trends.
    business name: {}
    ebitda FY21: {}
    ebitda FY22: {}
    industry: {}
    employees: {}
    transaction goals: {}
    other details: {}

    """.format(
        business_name.capitalize(),
        fy21_ebitda.capitalize(),
        fy22_ebitda.capitalize(),
        industry.capitalize(),
        employees.capitalize(),
        transaction_goals.capitalize(),
        other_details.capitalize()
    )

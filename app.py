import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


@app.route("/", methods=("GET", "POST"))
def index():
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
        return redirect(url_for("index", result=response.choices[0].text))

    result = request.args.get("result")
    return render_template("index.html", result=result)


def generate_prompt(business_name,fy21_ebitda, fy22_ebitda, industry, employees, transaction_goals,other_details):
    return """Write a pitch deck for a M&A transaction with the following information. 
    Discuss the upward trajectory of the company and a good market fit.
    Write it similar to the style below:
    
    style: Business name is a rapidly-growing Cognac brand with a strong market presence and a proprietary blend of high-quality products. The brand's success is evident in its impressive sales growth, with 9L case volume increasing from 8.1k in FY20 to 10.8k in FY21, and projected to reach 10.0k in FY22P. This upward trajectory is a clear indication of the brand's ability to generate profits and create value for all stakeholders.In addition, CRU has a solid market fit within the Cognac industry, with a presence in 21 states and recent expansion into five new markets. The brand's super-premium products have proven popular with consumers, resulting in high sales and customer loyalty. Overall, the business is a strong and attractive acquisition target, with a clear upward trajectory, a solid market fit, and high-quality products. The brand's success and recognition within the industry make it an ideal partner for any potential acquirer looking to enter or expand within the Cognac market.
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

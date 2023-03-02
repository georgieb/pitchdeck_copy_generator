import os

import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")

model_engine = "davinci-003"

def generate_text(prompt):
   completions = openai.Completion.create(
       engine=model_engine,
       prompt=prompt,
       max_tokens=1024,
       n=1,
       stop=None,
       temperature=0.5,
   )

   message = completions.choices[0].text
   return message.strip()

# Request financial due diligence information from the user
business_name = input("Please enter the business name: ")
fy21_ebitda = input("Please enter the FY21 EBITDA: ")
fy22_ebitda = input("Please enter the FY22 EBITDA: ")
industry = input("Please enter the industry: ")
transaction_goals = input("Please enter the transaction goals: ")

# Generate the M&A pitch deck
prompt = f"Generate a M&A pitch deck for a company named {business_name} with FY21 EBITDA of {fy21_ebitda} and FY22 EBITDA of {fy22_ebitda} in the {industry} industry with the following transaction goals: {transaction_goals}"
pitch_deck = generate_text(prompt)

# Print the pitch deck
print(pitch_deck)


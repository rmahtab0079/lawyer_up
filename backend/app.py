from flask import Flask, jsonify
import webbrowser

app = Flask(__name__)


def generate_url(city):
    return "https://www.yellowpages.ca/search/si/1/Employment+Lawyers/" + city 
    
sample_input = {
    "age": 30,
    "employment_length": 3,
    "employment_type": "Sales",
    "similar_employment": "little to none",
    "jurisdiction": "British Columbia",
    "city": "Vancouver",
    "salary": 30000
}

response = {
    "months": 6.27,
    "adjudication": 5000,
    "link": generate_url(sample_input["city"])
}


employment_type = ["Executive level management", "First tier manager or supervisor", "Middle management", "Professional", "Retail / clerical / administrative", "Sales", "Skilled labour", "Technical", "Unskilled labour", "Upper management", "Other"]
employment_availability = ["many but competitive", "many and high demand", "little to none", "some"] 
locations = ["Alberta", "British Columbia", "Manitoba", "New Brunswick", "Newfoundland and Labrador", "Nova Scotia", "Northwest Territories", "Nunavut", "Ontario", "Prince Edward Island", "Quebec", "Saskatchewan", "Yukon", "Canada"]

@app.route("/")
def predict():
    return jsonify(response)


if __name__ == '__main__':
    app.run(debug=True)
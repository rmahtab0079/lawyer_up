from flask import Flask, jsonify, request
import categories

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





"""
sample curl request:

curl --header "Content-Type: application/json" --request POST --data '{                                                                                          ─╯
    "age": 30,
    "employment_length": 3,
    "employment_type": "Sales",
    "similar_employment": "little to none",
    "jurisdiction": "British Columbia",
    "city": "Vancouver",
    "salary": 30000
}' http://127.0.0.1:5000/predict

"""

@app.route("/predict", methods=["POST"])
def json_example():
    req = request.get_json()
    print(req)
    return jsonify(response), 200


if __name__ == '__main__':
    app.run(debug=True)
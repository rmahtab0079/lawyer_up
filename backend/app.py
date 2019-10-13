from flask import Flask, jsonify, request
import categories
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import pendulum
import time


app = Flask(__name__)

# Use a service account
cred = credentials.Certificate('lawyer-up-dubhacks-firebase-adminsdk-bg7wy-142f040934.json')
firebase_admin.initialize_app(cred)
db = firestore.client()


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
sample curl request (predict):

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

@app.route("/")
def welcome():
    return "welcome to lawyer-now api"

@app.route("/predict", methods=["POST"])
def json_example():
    req = request.get_json()
    print(req)
    return jsonify(response), 200


"""
sample curl post request for (store):

curl --header "Content-Type: application/json" --request POST --data '{                                                                                          ─╯
    "modelID": "wrongful-dismissal",
    "conversation": [("bot", "hello"), ("user", "hi how is it going?")],
    "value": 5,
    "comments": "very helpful tool!"
}' http://127.0.0.1:5000/store
"""

@app.route("/store", methods = ["POST"])
def store():
    req = request.get_json()
    metrics = ["modelID", "conversation", "value", "comments"]
    metrics_values = [req.get(metric) for metric in metrics]
    metrics_values.append(time.time())
    
    collection_ref = db.collection(str(metrics_values[0]))
    docs = collection_ref.stream()

    numInDB = 1
    for doc in docs:
        print(u'{} => {}'.format(doc.id, doc.to_dict()))
        numInDB += 1
    
    print(numInDB)
    print(metrics_values)
    
    doc_ref = db.collection(str(metrics_values[0])).document(str(numInDB))
    doc_ref.set({
        u'modelID': metrics_values[0],
        u'conversation': str(metrics_values[1]),
        u'value': metrics_values[2],
        u'comments': metrics_values[3],
        u'timestamp': pendulum.now().to_day_datetime_string()
    })
    
    return "db updated", 200


if __name__ == '__main__':
    app.run()

    

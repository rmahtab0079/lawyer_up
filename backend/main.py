from flask import Flask, jsonify, request
import categories
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import pendulum
import time
from catboost import CatBoost, CatBoostRegressor
import json
import datetime
import re
import glob



app = Flask(__name__)

# Use a service account
cred = credentials.Certificate('lawyer-up-dubhacks-firebase-adminsdk-bg7wy-a410db3409.json')
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
    "salary": 30000,
    "notice_given": 6,
    "severance_amount" : 200
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

@app.route("/", methods = ["GET"])
def welcome():
    #metrics_values = [req.get(metric) for metric in metrics]
    ##ml model inputs: age (years), employment_type, similar_employment
    ##test_data = [metrics_values[2], metrics_values[3], metrics_values[4], metrics_values[5]]
    test_data  = [60,30*12, "Senior Engineer", "Little to none"] 
    param = {'iterations': 50}
    model = CatBoostRegressor(iterations=3, depth=8, learning_rate=1, loss_function='RMSE')
    model.load_model(glob.glob('./data/model_*')[0])
    # make the prediction using the resulting model
    preds_raw_vals = model.predict(test_data)
    return str(preds_raw_vals)

@app.route("/predict", methods=["POST"])
def predict():
    try:
        req = request.get_json()
        print(req)
        metrics = ["modelID", "jurisdiction", "age", "employment_length", "employment_type", "similar_employment", "salary", "city", "notice_given", "severance_amount"]
        metrics_values = [req.get(metric) for metric in metrics]
        print(metrics_values)
        
        ##ml model inputs: age (years), employment_type, similar_employment
        test_data = [metrics_values[2], metrics_values[3], metrics_values[4], metrics_values[5]]
        print(test_data)
        ##test_data  = [60,30*12, "Senior Engineer", "Little to none"] 
        param = {'iterations': 50}
        model = CatBoostRegressor(iterations=3, depth=8, learning_rate=1, loss_function='RMSE')
        model.load_model(glob.glob('./data/model_*')[0])
        # make the prediction using the resulting model
        preds_raw_vals = model.predict(test_data)
        
        response = {
        "months": round(preds_raw_vals, 2),
        "adjudication": round(((metrics_values[metrics.index("salary")]/12) * (preds_raw_vals - metrics_values[metrics.index("notice_given")]) - metrics_values[metrics.index("severance_amount")]), 2),
        "link": generate_url(metrics_values[metrics.index("city")])
        }

        return str(response)
        
    except Exception as e:
        return "sorry I'm still learning I am not sure how to respond to that"




"""
sample curl post request for (store):

curl --header "Content-Type: application/json" --request POST --data '{                                                                                          
    "modelID": "wrongful-dismissal",
    "conversation": [["bot", "hello"], ["user", "hi how is it going?"]],
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
    
    return "db updated"

if __name__ == '__main__':
    app.run()
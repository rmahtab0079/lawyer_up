from catboost import CatBoost
import json
import datetime
import re
import glob


def parse_x(d):
    return [d['age'], d['employment_length'], d['employment_type'], d['similar_employment']]


def parse_y(d):
    return d['adjudication']


# read the dataset
with open('../data/extracted_data.json', 'r') as data_file:
    data = json.load(data_file)['data']

train_data = list(map(parse_x, data))
train_labels = list(map(parse_y, data))
test_data = [35, 7, "Engineer", "Many but competitive"]


param = {'iterations': 5}
model = CatBoost(param)
# train the model
model.fit(X=train_data, y=train_labels, cat_features=[2, 3])

now = re.sub(r'[^0-9a-zA-Z]', '_', str(datetime.datetime.now()).split('.')[0])
model.save_model(f'../data/model_{now}')

model_path = glob.glob('../data/model_*')[0]
new_model = CatBoost(param)
new_model.load_model(model_path)

# make the prediction using the resulting model
preds_raw_vals = new_model.predict(test_data, prediction_type='RawFormulaVal')
print("Raw months:", preds_raw_vals)

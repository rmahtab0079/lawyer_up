from catboost import CatBoostRegressor
import json
import datetime
import re
import glob


def parse_x(d):
    return [d['age'], d['employment_length'], d['employment_type'], d['similar_employment']]


def parse_y(d):
    return d['adjudication']


# read the dataset
with open('../data/mock_data.json', 'r') as data_file:
    data = json.load(data_file)['data']

train_data = list(map(parse_x, data))
train_labels = list(map(parse_y, data))
test_data = [[60, 40 * 12, "Senior Engineer", "Many but competitive"], [60, 2 * 12, 'Senior Engineer', 'Many but competitive']]


param = {'iterations': 50}
model = CatBoostRegressor(iterations=3, depth=8, learning_rate=1, loss_function='RMSE')
# train the model
model.fit(X=train_data, y=train_labels, cat_features=[2, 3])

now = re.sub(r'[^0-9a-zA-Z]', '_', str(datetime.datetime.now()).split('.')[0])
model.save_model(f'../data/model_{now}')
import math

import numpy as np
from scipy.stats import norm
import json

import categories

DATA_POINTS = 1000

with open('../data/extracted_data.json', 'r') as data_file:
    data = json.load(data_file)['data']

age = list(map(lambda x: x['age'], data))
emp_length = list(map(lambda x: x['employment_length'], data))
adjudications = list(map(lambda x: x['adjudication'], data))

μ1, σ1 = norm.fit(age)
μ2, σ2 = norm.fit(emp_length)
μ3, σ3 = norm.fit(adjudications)

age = np.random.normal(μ1, σ1, DATA_POINTS)
emp_length = np.random.normal(μ2, σ2, DATA_POINTS)
emp_type = list(map(
    lambda x: categories.employment_type[int(math.floor(norm.cdf(x, μ2, σ2) * (len(categories.employment_type))))],
    emp_length
))
sim_emp = list(map(
    lambda x: categories.employment_availability[int(math.floor(norm.sf(x, μ1, σ1) * (len(categories.employment_availability))))],
    age
))

data = {"data": []}
for i in range(0, DATA_POINTS):
    data['data'].append({
        "age": age[i],
        "employment_length": emp_length[i],
        "employment_type": emp_type[i],
        "similar_employment": sim_emp[i],
        "adjudication": ((age[i] + emp_length[i]/12) * ((categories.employment_type.index(emp_type[i]) + 1)/(len(categories.employment_type))) * (categories.employment_availability.index(sim_emp[i]) + 1)/len(categories.employment_availability))
    })

with open('../data/fuzzy_data.json', 'w') as output_file:
    json.dump(data, output_file)

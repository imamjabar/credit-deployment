import pickle
import pandas as pd
import numpy as np
import sys
from flask import abort

raw_input = {'person_age': 27,
 'person_income': 47900,
 'person_home_ownership': 'OWN',
 'person_emp_length': 1.0,
 'loan_intent': 'VENTURE',
 'loan_grade': 'C',
 'loan_amnt': 7500,
 'loan_int_rate': 13.47,
 'loan_percent_income': 0.16,
 'cb_person_default_on_file': 'N',
 'cb_person_cred_hist_length': 6}

test_input = {
  'person_age': 24,
 'person_income': 43680,
 'person_home_ownership': 'RENT',
 'person_emp_length': 1.0,
 'loan_intent': 'EDUCATION',
 'loan_grade': 'A',
 'loan_amnt': 10800,
 'loan_int_rate': 5.42,
 'loan_percent_income': 0.25,
 'cb_person_default_on_file': 'N',
 'cb_person_cred_hist_length': 4,
 'person_emp_length_nan': 1.0,
 'loan_int_rate_nan': 5.42,
 'person_home_ownership_MORTGAGE': 0,
 'person_home_ownership_OTHER': 0,
 'person_home_ownership_OWN': 0,
 'person_home_ownership_RENT': 1,
 'loan_intent_DEBTCONSOLIDATION': 0,
 'loan_intent_EDUCATION': 1,
 'loan_intent_HOMEIMPROVEMENT': 0,
 'loan_intent_MEDICAL': 0,
 'loan_intent_PERSONAL': 0,
 'loan_intent_VENTURE': 0,
 'loan_grade_A': 1,
 'loan_grade_B': 0,
 'loan_grade_C': 0,
 'loan_grade_D': 0,
 'loan_grade_E': 0,
 'loan_grade_F': 0,
 'loan_grade_G': 0,
 'cb_person_default_on_file_N': 1,
 'cb_person_default_on_file_Y': 0,
 'person_age_WOE': -0.021,
 'person_income_WOE': 0.223,
 'person_emp_length_WOE': 0.285,
 'loan_amnt_WOE': -0.155,
 'loan_int_rate_WOE': -0.466,
 'loan_percent_income_WOE': -0.431,
 'cb_person_cred_hist_length_WOE': 0.032,
 'loan_status': 0,
 'score_proba': 0.08426437138570665,
 'prediction': 0
}

# WOE dict
with open("model/WOE-1.0.0.pkl", "rb") as f:
  woe_dict = pickle.load(f)

# One Hot Encoder
with open("model/OHE-1.0.0.pkl", "rb") as f:
  encoder = pickle.load(f)

# Column Name for One Hot Encoder
with open("model/COLNAME-1.0.0.pkl", "rb") as f:
  nominal_features = pickle.load(f)

# List of Features for feature selection
with open("model/FEATURES-1.0.0.pkl", "rb") as f:
  features_list = pickle.load(f)

# Model LR - All Features with WOE
with open("model/LR-ALL-WOE-1.0.0.pkl", "rb") as f:
  lr_model = pickle.load(f) 


def print_full(x):
  with pd.option_context('display.max_rows', len(x), 'display.max_columns', None):  # more options can be specified also
    print(x)

def formatting_data(raw_input):
  # Missing Column (Key) Handling as np.nan
  required_columns = ['person_age', 'person_income', 'person_home_ownership', 'person_emp_length', 'loan_intent', 'loan_grade', 
  'loan_amnt', 'loan_int_rate', 'loan_percent_income', 'cb_person_default_on_file', 'cb_person_cred_hist_length']

  for col in required_columns:
    try:
      raw_input[col]
    except KeyError as err:
      # If the categorical column missing: reject request
      if(col == 'person_home_ownership' or col == 'loan_intent' or col == 'loan_grade' or col == 'cb_person_default_on_file'):
        abort(400, {'error': 'categorical column is missing'})
      else:
        raw_input[col] = np.nan #handling as np.nan
  
  categorical_columns = ['person_home_ownership', 'loan_intent', 'loan_grade', 'cb_person_default_on_file']
  val = {
    "person_home_ownership": ['RENT','MORTGAGE','OWN','OTHER'],
    "loan_intent": ['EDUCATION', 'MEDICAL', 'VENTURE','PERSONAL','HOMEIMPROVEMENT','DEBTCONSOLIDATION'],
    "loan_grade": ['A','B','C','D','E','F','G'],
    "cb_person_default_on_file": ['Y','N']
  }
  for col in categorical_columns:
    if(raw_input[col] not in val[col]):
      abort(400, {'error': 'categorical column not match with the exact value'})

  # Outliers Handling: WOE (preprocessing) will handle the outliers
  # Missing Value Handling: Missing values will be mapped to np.nan. After that WOE will handle the nan value
  mapper_replace = {
      "null": np.nan,
      "": np.nan,
      None: np.nan
  }

  # Transform into DataFrame. Turn the dict to list first
  data = pd.DataFrame([raw_input]).replace(mapper_replace)
  
  return data

def preprocess(data):
  # 1. Preprocess WOE for Numerical Features
  # Transform Data
  for feature, woe_info in woe_dict.items():
      #print('feature:', feature)
      data[f'{feature}_WOE'] = pd.cut(data[feature], bins=woe_info['binning'], labels=woe_info['labels'])
      data[f'{feature}_WOE'] = data[f'{feature}_WOE'].values.add_categories('Nan').fillna('Nan') 
      data[f'{feature}_WOE'] = data[f'{feature}_WOE'].replace('Nan', woe_info['nan'])
      data[f'{feature}_WOE'] = data[f'{feature}_WOE'].astype(float)

  # 2. Preprocess One Hot Encoder for Categorical Features
  # Transform using encoder
  data_transformed = encoder.transform(data[nominal_features]).toarray()
  # Get the OHE column name
  column_name = encoder.get_feature_names(nominal_features)
  # Format into DF
  data_one_hot_encoded =  pd.DataFrame(data_transformed, columns= column_name, index=data[nominal_features].index).astype(int)
  # concat the data
  data = pd.concat([data,data_one_hot_encoded], axis=1).reset_index(drop=True)

  return data

def pred(data):
  # Feature Selection
  features = features_list
  # Model Selection
  model = lr_model

  #Predict
  pred_proba = model.predict_proba(data[features])[:, 1]
  threshold = 0.5
  prediction = (pred_proba > threshold).astype(int)

  return { "data": [ { "pred_proba": float(pred_proba[0]), "prediction": int(prediction[0])} ] }


def make_prediction(raw_input):
  data = formatting_data(raw_input)
  data = preprocess(data)
  prediction = pred(data)
  return prediction

if __name__ == "__main__":
  result = make_prediction(raw_input)
  print(result)

  # Try Errorhandling raw_input
  # result = formatting_data(raw_input)
  # print_full(result)
  # print(result)
  
  # Validasi Test 
  #result = pred(pd.DataFrame([test_input]))
  #print(result)
  
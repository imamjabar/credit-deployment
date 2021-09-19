## Live Access:
https://credit-scoring-imam.herokuapp.com/

## API
API PATH: https://credit-scoring-imam.herokuapp.com/predict-api
Using **POST** method, with arguments:

Field | Description | Value
------|-------------|------
person_age | Age. | Integer
person_income | Annual Income. | Integer 
person_home_ownership | Home ownership. | 'RENT', 'MORTGAGE', 'OWN', or 'OTHER'
person_emp_length | Employment length (in years) | Integer
loan_intent | Loan intent. | 'PERSONAL', 'EDUCATION', 'MEDICAL', 'VENTURE', 'HOMEIMPROVEMENT', or 'DEBTCONSOLIDATION'
loan_grade | Loan grade. | 'A', 'B', 'C, 'D', 'E', 'F', or 'G'
loan_amnt | Loan amount. | Integer
loan_int_rate | Interest rate. | Float
loan_percent_income | Percent income. | Float
cb_person_default_on_file | Historical default. | 'Y', or 'N'
cb_person_cred_hist_length | Credit history length. | Integer

For example:

```
{
    "person_age": 27,
    "person_income": 47900,
    "person_home_ownership": "OWN",
    "person_emp_length": 1,
    "loan_intent": "VENTURE",
    "loan_grade": "C",
    "loan_amnt": 7500,
    "loan_int_rate": 13.47,
    "loan_percent_income": 0.16,
    "cb_person_default_on_file": "N",
    "cb_person_cred_hist_length": 6
}
```

## Response API
Field | Description
------|------------
model | The machine learning model.
version | Model version.
score_proba | Probability estimates.
prediction | Predict class labels (0 is non default 1 is default).

```
{
    "model": "LR-ALL-WOE",
    "prediction": 0,
    "score_proba": 0.007841520883857913,
    "version": "1.0.0"
}
```

### Missing Keys handling:
- Missing keys: `person_age`, `person_income`, `person_emp_length`, `loan_amnt`, `loan_int_rate`, `loan_percent_income`, or `cb_person_cred_hist_length` will be mapped to `np.nan`.
- Missing keys: `person_home_ownership`, `loan_intent`, `loan_grade`, or `cb_person_default_on_file` will return **400 Bad Request**.

### Missing Value handling:
- Missing values will be mapped to `np.nan`.

### Handling outliers:
- Weight of Evidence (WOE) will handle the outliers in the preprocessing step.

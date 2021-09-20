## Live Access:
https://credit-scoring-imam.herokuapp.com/

## API Endpoint
- **POST** /predict-api
- Example: https://credit-scoring-imam.herokuapp.com/predict-api
- Description: Predict whether the client will default or not after their loan application.

### Request Headers:
- **Content-Type**: application/json

### Body Params:
Field | Description | Value | Required
------|-------------|-------|---------
person_age | Age. | Integer | Yes
person_income | Annual Income. | Integer | Yes 
person_home_ownership | Home ownership. | 'RENT', 'MORTGAGE', 'OWN', or 'OTHER' | Yes
person_emp_length | Employment length (in years) | Integer | Yes
loan_intent | Loan intent. | 'PERSONAL', 'EDUCATION', 'MEDICAL', 'VENTURE', 'HOMEIMPROVEMENT', or 'DEBTCONSOLIDATION' | Yes
loan_grade | Loan grade. | 'A', 'B', 'C, 'D', 'E', 'F', or 'G' | Yes
loan_amnt | Loan amount. | Integer | Yes
loan_int_rate | Interest rate. | Float | Yes
loan_percent_income | Percent income. | Float (Between 0 and 1) | Yes
cb_person_default_on_file | Historical default. | 'Y', or 'N' | Yes
cb_person_cred_hist_length | Credit history length. | Integer | Yes

### Examples:

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

## Response
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
- Missing values: `person_age`, `person_income`, `person_emp_length`, `loan_amnt`, `loan_int_rate`, `loan_percent_income`, or `cb_person_cred_hist_length` will be mapped to `np.nan`.
- Missing values or random values: `person_home_ownership`, `loan_intent`, `loan_grade`, or `cb_person_default_on_file` will return **400 Bad Request**.

### Handling outliers:
- Weight of Evidence (WOE) will handle the outliers in the preprocessing step.

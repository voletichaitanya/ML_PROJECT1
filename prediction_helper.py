import joblib
import pandas as pd

model_young = joblib.load("artifacts/model_young.joblib")
model_rest = joblib.load("artifacts/model_rest.joblib")
scaler_young = joblib.load("artifacts/scaler_young.joblib")
scaler_rest = joblib.load("artifacts/scaler_rest.joblib")


def preprocess_input(input_dict):
    df_columns = [ 'age', 'region', 'number_of_dependants', 'bmi_category', 'income_lakhs',
       'medical_history', 'insurance_plan', 'genetical_risk', 'gender_Male', 'smoking_status_Occasional',
       'smoking_status_Regular', 'employment_status_Salaried',
       'employment_status_Self-Employed'
    ]

    df = pd.DataFrame(0, columns = df_columns, index=[0] )  # Created empty dataframe
    
    # Numerical values directly storing in df
    df['age'] = input_dict['age']
    df['number_of_dependants'] = input_dict['number_of_dependants']
    df['income_lakhs'] = input_dict['income_lakhs']
    df['genetical_risk'] = input_dict['genetical_risk']
    df['medical_history'] = input_dict['medical_history']

    # Converting categorical data to numerical : Label/Ordinal
    region_encoded = {'Northeast': 0, 'Northwest': 1, 'Southeast': 2, 'Southwest': 3}
    bmi_category_encoded = {'Overweight': 2, 'Underweight': 3, 'Normal' : 0, 'Obesity': 1}
    insurence_plan_encoded = {'Silver':1, 'Bronze':0, 'Gold':2}

    df['region'] = region_encoded.get(input_dict['region'], 1)
    df['bmi_category'] = bmi_category_encoded.get(input_dict['bmi_category'], 1)
    df['insurance_plan'] = insurence_plan_encoded.get(input_dict['insurance_plan'], 1)

    # One hot encoding
    if input_dict['gender'] == 'Male':
        df['gender_Male'] = 1
    if input_dict['smoking_status'] == 'Regular':
        df['smoking_status_Regular'] = 1
    if input_dict['smoking_status'] == 'Occasional':
        df['smoking_status_Occasional'] = 1
    if input_dict['employment_status'] == 'Salaried':
        df['employment_status_Salaried'] = 1
    if input_dict['employment_status'] == 'Self-Employed':
        df['employment_status_Self-Employed'] = 1

    df = handle_scaling(input_dict['age'],df)

    return df


def handle_scaling(age, df):
    if age < 25:
        scaler_object = scaler_young
    else:
        scaler_object = scaler_rest

    cols_to_scale = scaler_object['cols_to_scale']
    scaler = scaler_object['scaler']

    # Leave income_level blank
    df['income_level'] = None
    df['marital_status_Unmarried'] = None

    df[cols_to_scale] = scaler.transform(df[cols_to_scale])

    df.drop(['marital_status_Unmarried', 'income_level'], axis = 1, inplace = True)

    return df


def predict(input_dict):
    processed_data = preprocess_input(input_dict)

    if input_dict['age'] < 25:
        final_premium = model_young.predict(processed_data)
    else:
        final_premium = model_rest.predict(processed_data)

    return final_premium
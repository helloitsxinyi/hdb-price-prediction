from flask import Flask, render_template, request, jsonify, json
import numpy as np
import pandas as pd
import joblib
from dateutil.relativedelta import relativedelta

app = Flask(__name__)
model = joblib.load(open("./training/model.pkl", "rb"))
month_encoder = joblib.load(open("./training/month_encoder.pkl", "rb"))


@app.route('/')
def index():
    return render_template("form.html")

# API endpoint
@app.route("/predict", methods=["POST"])
def result():
    if request.method == "POST":
        # load the json request data first
        input_list = json.loads(request.data)

        # convert to appropriate data format to feed into model
        input_list = list(input_list.values())

        result_df = createResultDataFrame(input_list)

        # use loads to convert string data into json
        result_json = json.loads(result_df.to_json(orient="records"))

        return jsonify(result_json)

# for webpage purposes only
@app.route("/predict_form", methods=["POST"])
def result_form():
    if request.method == "POST":
        input_list = request.form.to_dict()
        input_list = list(input_list.values())
        result_df = createResultDataFrame(input_list)
        return render_template("result.html", prediction=result_df)

@app.route("/pricetrend")
def get_price_trend():
    df_price_trend = getPriceTrendDataFrame()
    price_trend_json = json.loads(df_price_trend.to_json(orient="records"))
    return jsonify(price_trend_json)


def createResultDataFrame(input_list):
    '''
    :param input_list: list of user's inputs. the expected order is:
    flat_type, flat_model, floor_area_sqm, lease_commence_date, storey_range, town, start date, months to predict

    :return: DataFrame comprising rows with months for specified time period (encoded) and columns corresponding to user inputs.
    '''
    start = input_list[-2][:-3]
    months = int(input_list[-1])

    to_predict_df = createPredictDataFrame(input_list, start, months)
    result_arr = ValuePredictor(to_predict_df)
    base = pd.to_datetime(start)
    months_arr = np.array([base + relativedelta(months=+i) for i in range(months+1)])
    result_arr = pd.DataFrame({'date': months_arr, 'predicted_price': result_arr})
    return result_arr

def createPredictDataFrame(input_list, start, months):
    '''
    :param start, months: the start date and number of months to predict according to user inputs.
    :param input_list: list of user's inputs. the expected order is:
    flat_type, flat_model, floor_area_sqm, lease_commence_date, storey_range, town, start date, months to predict

    :return: DataFrame comprising rows with months for specified time period (encoded) and columns corresponding to user inputs.
    '''

    start_encoded = month_encoder.transform([start])[0]
    months_arr = np.arange(start_encoded, start_encoded + months + 1)

    # create df with the encoded month values
    to_predict_df = pd.DataFrame(months_arr, columns=["month_encoded"])
    to_predict_df[['flat_type_cat', 'flat_model_cat', 'floor_area_sqm', 'lease_commence_date', 'storey_range_cat',
               'town_cat']] = np.array(input_list[0:-2], dtype=int)
    return to_predict_df

def ValuePredictor(to_predict_df):
    '''
        :param to_predict_df: DataFrame comprising rows with months for specified time period (encoded), and columns corresponding to user inputs.

        :return: array of prediction results.
    '''
    result_arr = np.round(model.predict(to_predict_df), 2)
    return result_arr

def getPriceTrendDataFrame():
    df = pd.read_csv('./training/SavedData.csv')
    df['price_per_sq_m'] = df['resale_price'] / df['floor_area_sqm']
    df['date'] = pd.to_datetime(df['month'])
    df_price_trend = df.groupby('date').mean().reset_index()[['date', 'price_per_sq_m']]
    df_price_trend['price_per_sq_m'] = df_price_trend['price_per_sq_m'].round(2)
    return df_price_trend

if __name__ == "__main__":
    app.run(debug=True)

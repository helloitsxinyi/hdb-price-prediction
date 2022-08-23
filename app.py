from flask import Flask, request, jsonify, json
import numpy as np
import pandas as pd
import joblib
import urllib
from utils.create_dataframes_and_arrays import *

app = Flask(__name__)

limit = 300000

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

@app.route("/pricetrend")
def get_price_trend():
    df_price_trend = getPriceTrendDataFrame()
    price_trend_json = json.loads(df_price_trend.to_json(orient="records"))
    return jsonify(price_trend_json)


@app.route("/checkupdates")
def get_updates():
    updates, success = check_updates()
    return jsonify({'updates': updates, 'success': success})


def getPriceTrendDataFrame():
    df = pd.read_csv('./data/SavedData.csv')
    df['price_per_sq_m'] = df['resale_price'] / df['floor_area_sqm']
    df['date'] = pd.to_datetime(df['month'])
    df_price_trend = df.groupby('date').mean().reset_index()[['date', 'price_per_sq_m']]
    df_price_trend['price_per_sq_m'] = df_price_trend['price_per_sq_m'].round(2)
    return df_price_trend

def pull_data():
    global limit
    #url = 'https://data.gov.sg/api/action/datastore_search?resource_id=f1765b54-a209-4718-8d38-a39237f502b3&limit=200000&offset=0'
    url = 'https://data.gov.sg/api/action/datastore_search?resource_id=f1765b54-a209-4718-8d38-a39237f502b3&limit='+str(limit)+'&offset=0'
    print(url)
    request = urllib.request.Request(url=url, headers={
        'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11'})
    with urllib.request.urlopen(request) as response:
        res = response.read().decode('utf-8')
        jsondata = json.loads(res)

    latest_data = jsondata['result']['records']
    latest_data_df = pd.DataFrame.from_dict(latest_data)
    try:
        latest_data_df = latest_data_df.sort_values(by=['month','town','street_name'], ascending=True, inplace=False, kind='quicksort', na_position='last', ignore_index=True, key=None)
    except:
        print("SORTTING OF DATA FAILED. TO CHECK THE DATA FORMAT.")
    

    return latest_data_df

def check_updates():
    global limit
    updates, success = False, False
    try:
        pulled_data = pull_data()

        saved_data = pd.read_csv('data/SavedData.csv')
        pulled_data = convert_latest_data_types(pulled_data)

        pulled_data_last = pulled_data.iloc[-1]
        saved_data_last = saved_data.iloc[-1]
        if(pulled_data.shape[0] > saved_data.shape[0]):
            if((limit - pulled_data.shape[0])<50000):
                limit = pulled_data.shape[0]+100000
        print("limit:",limit," ,size:",pulled_data.shape[0])
        # if last entries are equal or date of pulled is earlier than saved, no updates
        if np.array_equal(pulled_data_last, saved_data_last) \
                or (pd.to_datetime(pulled_data_last.month) < pd.to_datetime(saved_data_last.month)):
            updates, success = False, True
        else:
            updates = True
            pulled_data.to_csv('data/SavedData.csv', index=False)
            success = True
    except Exception as e:
        print("Update not successful")
        print(str(e))
        success = False
    return updates, success

def convert_latest_data_types(latest_data):
    '''
        latest_data floor_area_sqm and resale_price values will be in int instead of float,
        while lease_commence_date is in string.

        read_csv automatically converts floor_area_sqm and resale_price int values to floats, and lease_commence_date to int
        so we need to ensure that the pulled data cols are in float & int.
    '''
    latest_data['floor_area_sqm'] = latest_data['floor_area_sqm'].astype(float)
    latest_data['resale_price'] = latest_data['resale_price'].astype(float)
    latest_data['lease_commence_date'] = latest_data['lease_commence_date'].astype(int)
    return latest_data


# for webpage purposes only
@app.route('/')
def index():
    return render_template("form.html")

# for webpage purposes only
@app.route("/predict_form", methods=["POST"])
def result_form():
    if request.method == "POST":
        input_list = request.form.to_dict()
        input_list = list(input_list.values())
        result_df = createResultDataFrame(input_list)
        return render_template("result.html", prediction=result_df)

if __name__ == "__main__":
    app.run(debug=True)

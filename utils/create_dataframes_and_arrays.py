import pandas as pd
from dateutil.relativedelta import relativedelta
from utils.predict_values import *

month_encoder = joblib.load(open(os.getcwd() + "/training_notebooks/month_encoder.pkl", "rb"))

def createResultDataFrame(input_list):
    '''
    :param input_list: list of user's inputs. the expected order is:
    flat_model, flat_type, floor_area_sqm, lease_commence_date, storey_range, town, start date, months to predict

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
    flat_model, flat_type, floor_area_sqm, lease_commence_date, storey_range, town, start date, months to predict

    :return: DataFrame comprising rows with months for specified time period (encoded) and columns corresponding to user inputs.
    '''

    flat_model = int(input_list[0])
    flat_type = int(input_list[1])
    storey = int(input_list[4])
    town = int(input_list[5])
    start_encoded = month_encoder.transform([start])[0]
    months_arr = np.arange(start_encoded, start_encoded + months + 1)

    to_predict_df = pd.DataFrame(months_arr, columns=["month_encoded"])
    to_predict_df[['floor_area_sqm', 'lease_commence_date']] = np.array(input_list[2:4], dtype=int)
    to_predict_df = addTownOneHotDataFrame(town, to_predict_df)
    to_predict_df = addModelOneHotDataFrame(flat_model, to_predict_df)
    to_predict_df = addTypeOneHotDataFrame(flat_type, to_predict_df)
    to_predict_df = addStoreyOneHotDataFrame(storey, to_predict_df)
    to_predict_df = pd.concat([to_predict_df.iloc[:,1::], to_predict_df.iloc[:,0]], axis=1)
    return to_predict_df


def addTownOneHotDataFrame(town, to_predict_df):
    town_arr = [0] * 26
    town_arr[town] = 1
    to_predict_df[['Town_ANG MO KIO',
                   'Town_BEDOK', 'Town_BISHAN', 'Town_BUKIT BATOK', 'Town_BUKIT MERAH',
                   'Town_BUKIT PANJANG', 'Town_BUKIT TIMAH', 'Town_CENTRAL AREA',
                   'Town_CHOA CHU KANG', 'Town_CLEMENTI', 'Town_GEYLANG', 'Town_HOUGANG',
                   'Town_JURONG EAST', 'Town_JURONG WEST', 'Town_KALLANG/WHAMPOA',
                   'Town_MARINE PARADE', 'Town_PASIR RIS', 'Town_PUNGGOL',
                   'Town_QUEENSTOWN', 'Town_SEMBAWANG', 'Town_SENGKANG', 'Town_SERANGOON',
                   'Town_TAMPINES', 'Town_TOA PAYOH', 'Town_WOODLANDS', 'Town_YISHUN']] = town_arr

    return to_predict_df


def addModelOneHotDataFrame(flat_model, to_predict_df):
    flat_model_arr = [0] * 21
    flat_model_arr[flat_model] = 1
    to_predict_df[['Model_2-room', 'Model_3Gen', 'Model_Adjoined flat',
       'Model_Apartment', 'Model_DBSS', 'Model_Improved',
       'Model_Improved-Maisonette', 'Model_Maisonette', 'Model_Model A',
       'Model_Model A-Maisonette', 'Model_Model A2', 'Model_Multi Generation',
       'Model_New Generation', 'Model_Premium Apartment',
       'Model_Premium Apartment Loft', 'Model_Premium Maisonette',
       'Model_Simplified', 'Model_Standard', 'Model_Terrace', 'Model_Type S1',
       'Model_Type S2']] = flat_model_arr

    return to_predict_df

def addTypeOneHotDataFrame(flat_type, to_predict_df):
    flat_type_arr = [0] * 7
    flat_type_arr[flat_type] = 1
    to_predict_df[['Type_1 ROOM', 'Type_2 ROOM', 'Type_3 ROOM',
       'Type_4 ROOM', 'Type_5 ROOM', 'Type_EXECUTIVE', 'Type_MULTI-GENERATION']] = flat_type_arr
    return to_predict_df


def addStoreyOneHotDataFrame(storey, to_predict_df):
    storey_arr = [0] * 17
    storey_arr[storey] = 1
    to_predict_df[['Storey_01 TO 03', 'Storey_04 TO 06', 'Storey_07 TO 09',
       'Storey_10 TO 12', 'Storey_13 TO 15', 'Storey_16 TO 18',
       'Storey_19 TO 21', 'Storey_22 TO 24', 'Storey_25 TO 27',
       'Storey_28 TO 30', 'Storey_31 TO 33', 'Storey_34 TO 36',
       'Storey_37 TO 39', 'Storey_40 TO 42', 'Storey_43 TO 45',
       'Storey_46 TO 48', 'Storey_49 TO 51']] = storey_arr
    return to_predict_df
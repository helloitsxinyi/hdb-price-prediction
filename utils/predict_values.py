import numpy as np
import joblib
import os
from sklearn.preprocessing import PolynomialFeatures

model = joblib.load(open(os.getcwd() + "/training_notebooks/model.pkl", "rb"))

def ValuePredictor(to_predict_df):
    '''
        :param to_predict_df: DataFrame comprising rows with months for specified time period (encoded), and columns corresponding to user inputs.

        :return: array of prediction results.
    '''
    poly = PolynomialFeatures(degree=2, include_bias=False)
    to_predict_transformed = poly.fit_transform(to_predict_df)
    result_arr = np.round(model.predict(to_predict_transformed), 2)
    return result_arr
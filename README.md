# Property price prediction API

## Table of Contents

1. [About](#about)
2. [Setup](#setup)
3. [Label Encoded Values](#label-encoded-values)
4. [Endpoints](#endpoints)

## About
This repo contains files and Jupyter notebooks for the price prediction of HDB resale flats in Singapore.

The data is obtained from `data.gov.sg` (Singapore publicly available data) and we are using a Flask API for price prediction, price trend calculation and checking for data updates.

<hr>

The repo is organized as follows:
- `/data`: All saved data for model training is stored here.
- `/templates`: HTML files for the webpage and form.
- `/training_notebooks`: 
  1. `1_data_extraction.ipynb`: Jupyter notebook for data extraction
     1. This will help us obtain SavedData.csv needed for the second notebook)
     2. This notebook can be used in place of the `/checkupdates` endpoint if desired.

  2. `2_data_preprocessing.ipynb`
     1. Jupyter notebook for data preprocessing and model training

- `/utils`: Contains helper and prediction functions for the various endpoints.

<hr>
2 ways you can view the prediction:

1. Entering values and submitting the form on the main page. 
2. Send in a POST request. See [Endpoints](#endpoints) for sample input and outputs. 


## Setup

1. Create the virtual environment:

Mac:

```
python3 -m venv env
```

Windows:

```
py -m venv env

python -m venv <env name>

```

2. Activate the virtual environment

Mac:

```
source env/bin/activate
```

Windows:

```
<env path>\Scripts\activate


```

3. Install required packages:

Mac:

```
python3 -m pip install -r requirements.txt
```

Windows:

```
py -m pip install -r requirements.txt
```


4. Run Flask app in debugger mode:

Mac:
```
python3 app.py
```

Windows:
```
python app.py 
```

5. **IMPORTANT** Run all cells of the `2_data_preprocessing.ipynb` notebook to obtain the `model.pkl` and `month_encoder.pkl` files. 
These files are required for the price prediction model.


## Endpoints
By default, the app is hosted on http://127.0.0.1:5000/. Loading this URL on a web browser will return a sample form that you can use to test and view the predicted prices (in HTML format).

1. `/predict` (REST POST):
- REST API endpoint for obtaining predicted price result (JSON).
  Request body values correspond to label encoded values. See [Label Encoded Values](#label-encoded-values) for the encoded values.

Sample request body:
```
{
    "flattype": "5", 
    "flatmodel": "7", 
    "floorarea": "152", 
    "lease": "1992", 
    "storey": "1", 
    "town": "21",
    "startdate": "2018-07-01",
    "months": "25"
}
```

This will return an array of objects. The number of objects corresponds to number of months + 1, where the first object corresponds to the start date.

Sample response:
```
[
    {
        "date": 1530403200000,
        "predicted_price": 603055.9
    },
    {
        "date": 1533081600000,
        "predicted_price": 604578.61
    },
    {
        "date": 1535760000000,
        "predicted_price": 606101.31
    },
    {
        "date": 1538352000000,
        "predicted_price": 607624.02
    }
]
```

2. `/pricetrend` (REST GET)
- API endpoint for obtaining average price per sq m of HDB resale flats over the previous months.

Sample response:
```
[
    {
        "date": 1483228800000,
        "price_per_sq_m": 4523.77
    },
    {
        "date": 1485907200000,
        "price_per_sq_m": 4585.07
    },
    {
        "date": 1488326400000,
        "price_per_sq_m": 4624.39
    }
]
```


3. `/checkupdates` (REST GET)
- API endpoint for checking if there are new updates to the api on `data.gov.sg`, and if existing data has been successfully overwritten.

Sample response:
```
{
    "success": true,
    "updates": true
}
```

## Label encoded values
We use label encoding for the request body inputs: `town, flat_model, flat_type, storey`.
The mappings are encoded as follows:

Town:
```
{'ANG MO KIO': 0, 
  'BEDOK': 1, 
  'BISHAN': 2, 
  'BUKIT BATOK': 3, 
  'BUKIT MERAH': 4, 
  'BUKIT PANJANG': 5, 
  'BUKIT TIMAH': 6, 
  'CENTRAL AREA': 7, 
  'CHOA CHU KANG': 8, 
  'CLEMENTI': 9, 
  'GEYLANG': 10, 
  'HOUGANG': 11, 
  'JURONG EAST': 12, 
  'JURONG WEST': 13, 
  'KALLANG/WHAMPOA': 14, 
  'MARINE PARADE': 15, 
  'PASIR RIS': 16, 
  'PUNGGOL': 17, 
  'QUEENSTOWN': 18, 
  'SEMBAWANG': 19, 
  'SENGKANG': 20, 
  'SERANGOON': 21, 
  'TAMPINES': 22, 
  'TOA PAYOH': 23, 
  'WOODLANDS': 24, 
  'YISHUN': 25}
```

Flat model:
```
{'2-room': 0, 
  '3Gen': 1, 
  'Adjoined flat': 2, 
  'Apartment': 3, 
  'DBSS': 4, 
  'Improved': 5, 
  'Improved-Maisonette': 6, 
  'Maisonette': 7, 
  'Model A': 8, 
  'Model A-Maisonette': 9, 
  'Model A2': 10, 
  'Multi Generation': 11, 
  'New Generation': 12, 
  'Premium Apartment': 13, 
  'Premium Apartment Loft': 14, 
  'Premium Maisonette': 15, 
  'Simplified': 16, 
  'Standard': 17, 
  'Terrace': 18, 
  'Type S1': 19, 
  'Type S2': 20}
```

Flat type:
```
{'1 ROOM': 0, 
  '2 ROOM': 1, 
  '3 ROOM': 2, 
  '4 ROOM': 3, 
  '5 ROOM': 4, 
  'EXECUTIVE': 5, 
  'MULTI-GENERATION': 6}
```

Storey:
```
{'01 TO 03': 0, 
  '04 TO 06': 1, 
  '07 TO 09': 2, 
  '10 TO 12': 3, 
  '13 TO 15': 4, 
  '16 TO 18': 5, 
  '19 TO 21': 6, 
  '22 TO 24': 7, 
  '25 TO 27': 8, 
  '28 TO 30': 9, 
  '31 TO 33': 10, 
  '34 TO 36': 11, 
  '37 TO 39': 12, 
  '40 TO 42': 13, 
  '43 TO 45': 14, 
  '46 TO 48': 15, 
  '49 TO 51': 16}
```
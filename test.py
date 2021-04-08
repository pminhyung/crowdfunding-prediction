import pickle
import numpy as np
import pandas as pd

from preprocessing import preprocess_data

test_fname = 'test.xlsx'

test = pd.read_excel(test_fname, engine = 'openpyxl')
test_df = preprocess_data(test)

pretrained_model = pickle.load(open("xgb.dat", "rb"))

y_pred = pretrained_model.predict(test_df)
#predictions = [np.round(value, 2) for value in y_pred]

test_df['predictions'] = y_pred
test_df.to_excel('test_predictions.xlsx', index=False)


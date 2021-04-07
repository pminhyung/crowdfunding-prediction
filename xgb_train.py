from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import sklearn.metrics as mt
from sklearn.model_selection import GridSearchCV

import xgboost
from xgboost import XGBClassifier

import pandas as pd

from scraping import scrap_wadiz, scrap_navernews
from utils import get_cat_success_rate
from preprocessing import preprocess_data

wadiz_fname = scrap_wadiz('wadiz.xlsx')
#naver_fname = scrap_navernews('크라우드펀딩')

wadiz = pd.read_excel(wadiz_fname, engine = 'openpyxl')
#naver = pd.read_excel(naver_fname, engine = 'openpyxl')

df = preprocess_data(wadiz)


X = total.drop(['log_count'], axis=1)
y = total['log_count']

# 학습용/테스트용 데이터 분리


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=100)


# Random Forest Regressor

# rf = RandomForestRegressor(n_estimators = 1000)
#
# rf.fit(X_train, y_train)
#
# print(rf.score(X_train, y_train))
# print(rf.score(X_test, y_test))
#
# y_pred = rf.predict(X_test)
#
# #평가 지표 값들을 계산한다.
# mse = mt.mean_squared_error(y_test, y_pred)
# rmse = np.sqrt(mse)
# r2 = mt.r2_score(y_test, y_pred)
#
# print("MSE:{:.3f}\nRMSE: {:.3f}\nR2: {:.3f}".format(mse,rmse,r2))
#print(mt.accuracy_score( y_pred, y_test))
#print(mt.confusion_matrix(y_pred, y_test))
# feat_imp = pd.DataFrame({'속성명':X.columns, '중요도':rf.feature_importances_}).sort_values('중요도',ascending=False)
# print(feat_imp)

# log transformation한 달성률(log_count)을 예측
# y_pred = rf.predict(X_test)
# # log transformation한 달성률(log_count)을 다시 exp로 원상복귀
# predictions = np.exp(y_pred) - 1

## XGBoost - Classification
xgb_clf = XGBClassifier()
xgb_clf.fit(X_train, y_train)

xgb_acc = xgb_clf.score(X_test, y_test)
print(xgb_acc)

# gridsearch



xgb_params = {'n_estimators':[100,200],
             'learning_rate':[0.1,0.2]}

grid_xgb = GridSearchCV(xgb_clf, param_grid = xgb_params,
               cv= 5, n_jobs=-1)
grid_xgb.fit(X_train, y_train)
grid_score = grid_xgb.score(X_test,y_test)
best_params = grid_xgb.best_params_

print(grid_xgb)
print(best_params)
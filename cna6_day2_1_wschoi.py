# -*- coding: utf-8 -*-
"""CNA6_day2-1_WSChoi.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1YXpxwzosi68ex3JQO4fzof_dZ1iv-COn

---
"""

from google.colab import drive
drive.mount('/content/drive')

"""# <center>영구 자석 동기 모터(PMSM) 부품 온도 예측</center>

컬럼 | 설명 | 컬럼 | 설명
---|---|---|---
id | 고유번호 | motor_speed | 모터 회전속도
ambient | 주변 온도 | coolant | 냉각수 온도
u_q | 전압 q | u_d | 전압 d
i_d | 전류 q | i_q | 전류 d
pm | 특정 부품(rotor) 온도 |

![pmsm](https://ko.tech-zy.com/js/htmledit/kindeditor/attached/20210420/20210420170944_90438.jpg)

# Library
"""

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

import warnings
warnings.filterwarnings(action='ignore')

"""# 데이터셋 업로드"""

# 구글 드라이브 연결하기
# from google.colab import drive
# drive.mount('./MyDrive')

# 구글 드라이브 연결하기
from google.colab import drive
drive.mount('./MyDrive')

"""# Load Dataset"""

train = pd.read_csv("/content/MyDrive/MyDrive/motor_temperature-20211118T021215Z-001/motor_temperature/train.csv")
train.head()

test = pd.read_csv("/content/MyDrive/MyDrive/motor_temperature-20211118T021215Z-001/motor_temperature/test.csv")
test.head()

submission = pd.read_csv("/content/MyDrive/MyDrive/motor_temperature-20211118T021215Z-001/motor_temperature/sample_submission.csv")
submission.head()

"""# 데이터 탐색 (EDA)

### 데이터프레임 크기(세로, 가로)
"""

train.shape

test.shape

"""### 데이터프레임 기본 정보"""

train.info()

"""### 통계정보 요약"""

train.describe()

train.sum()



"""### 중복행 개수"""

train.isnull()

train.duplicated().sum()

test.duplicated()

test.duplicated().sum()

"""### 결측치 개수"""

train.isnull().sum()

test.isnull().sum()

"""## Target 목표 변수 (전기 모터 부품의 온도: pm)"""

train["pm"].describe()

train["pm"].hist()

train["pm"].plot(kind='hist')

sns.displot(x='pm', data=train);

sns.displot(x='pm', kind='kde', data=train);

"""## Pairplot 데이터 분포"""

sns.pairplot(data=train.iloc[:, 1:], diag_kind='hist');

"""## 상관계수 분석"""

train.iloc[ :  , 1:]. corr()

# 상관계수 테이블
df_corr = train.iloc[:, 1:].corr()
df_corr

# Target 변수와 상관계수가 높은 순서대로 정렬
df_corr.loc[ :  ,  ['pm']  ].abs().sort_values(by=['pm'], ascending=False)

# 강제 한글  포트 설치 방법 구글링  https://teddylee777.github.io/colab/colab-korean
# 참고링크 https://datascienceschool.net/01%20python/05.04%20%EC%8B%9C%EB%B3%B8%EC%9D%84%20%EC%82%AC%EC%9A%A9%ED%95%9C%20%EB%8D%B0%EC%9D%B4%ED%84%B0%20%EB%B6%84%ED%8F%AC%20%EC%8B%9C%EA%B0%81%ED%99%94.html
# 그래프링크 http://seaborn.pydata.org/examples/index.html

# 히트맵
plt.figure(figsize=(8, 8))

sns.heatmap(data=df_corr, annot=True, cbar=True,
           linewidths=0.05, linecolor="white", fmt= '.2f')
plt.title('correal'   ,   fontsize=20)

plt.show()



"""## 데이터 분포"""

train.columns[ : ]

for c in train.columns[1:]:
   print(c)

import matplotlib
matplotlib.rcParams['axes.unicode_minus'] = False

for col in train.columns[1:]:
    sns.displot(x=col, data =train)

for col in train.columns[1:]:
    sns.displot(train[col], color ='b')
    plt.show()

"""## Target 구간을 나누고, 구간에 따른 변수 차이 확인"""

bins = [0, 30, 90, 120]

bin_labels = ['L1', 'L2', 'L3']

pd.cut(train['pm'], bins=bins, labels=bin_labels)

train['pm_bin'] = pd.cut(train['pm'], bins=bins, labels=bin_labels)
train['pm_bin'].value_counts()

for col in train.columns[1:-1]:
    sns.displot(x=col, hue='pm_bin', kind='kde', data=train, color ='b')
    plt.show()

"""# Regression 알고리즘

## 단순회귀분석
"""

train

train.columns

# 선형회귀분석할때 머신러닝할때 쓰는 싸이키런  sklearn  ,    
from sklearn.linear_model import LinearRegression

lr_model = LinearRegression()

# X, y 변수 정리

X_train = train.loc[ : , [ 'ambient', 'coolant' , 'i_d' ] ]
y_train = train['pm']

print(X_train.shape, y_train.shape)

# 모델 훈련
lr_model.fit(X_train, y_train)

lr_model.coef_

lr_model.intercept_

# y= 5x - 65

# 모델 예측
y_pred = lr_model.predict(X_train)

y_pred

# 평가 지표 - mean_squared_error
from sklearn.metrics import mean_squared_error
print("평균제곱오차: %0.2f" % mean_squared_error(y_train, y_pred))

submission.to_csv('prediction_020.csv', index=False)

"""## 모델 예측"""

test

# 변수 선택
X_test = test.loc[:, ['ambient']]
# 예측
preds = lr_model.predict(X_test)

len(preds)

"""## Submission 파일 만들기"""

submission.head()

submission['pm'] = preds
submission

submission.to_csv('prediction_001.csv', index=False)

# 저장 파일을 평가 시스템에 제출
# https://newlearn.kr/login   로그인 사내 메일 주소 / 비번은 dbgroup1234









"""## 다중회귀분석"""

train

X_train

# X, y 변수 정리

X_train = train.loc[:, ['ambient', 'coolant' , 'motor_speed']]
y_train = train['pm']

X_test = test.loc[:, ['ambient', 'coolant']]

print(X_train.shape, y_train.shape, X_test.shape)

lr_model = LinearRegression()

# 모델 훈련
lr_model.fit(X_train, y_train)

lr_model.coef_

lr_model.intercept_

# 모델 예측
y_pred = lr_model.predict(X_train)

# 평가 지표 - mean_squared_error
from sklearn.metrics import mean_squared_error
print("평균제곱오차: %0.2f" % mean_squared_error(y_train, y_pred))

"""# 피처 스케일링"""

X_train

from sklearn.preprocessing import MinMaxScaler, StandardScaler

# 스케일링 모델 생성
scaler = MinMaxScaler()
scaler.fit(X_train)
X_train_scaled = X_train.copy()
X_train_scaled.loc[:, :] = scaler.transform(X_train)

X_train_scaled

# 스케일러 모델 훈련
scaler.fit(X_train)

X_train.copy()

scaler.transform(X_train)

# 스케일링 변환
X_train_scaled = X_train.copy()
X_train_scaled.loc[:, :] = scaler.transform(X_train)

X_train_scaled.describe()

# 스케일링 변환
X_test_scaled = X_test.copy()
X_test_scaled.loc[:, :] = scaler.transform(X_test)

X_test_scaled.describe()

X_train['ambient'].plot(kind='box')

X_train['ambient'] >= 20

X_train.loc[X_train['ambient'] >= 20,    : ]

X_train1 = X_train.loc[X_train['ambient'] >= 20,    : ]

scaler = MinMaxScaler()
scaler.fit(X_train1)
X_train1_scaled = X_train1.copy()
X_train1_scaled.loc[:, :] = scaler.transform(X_train)

"""# 홀드아웃 교차 검증

## Train - Test 분할
"""

from sklearn.model_selection import train_test_split
X_tr, X_val, y_tr, y_val = train_test_split(X_train_scaled, y_train, test_size=0.3, random_state=2021)

print(X_tr.shape, y_tr.shape)
print(X_val.shape, y_val.shape)

"""## 과대 적합 (over-fitting)"""

from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

# 1차 다항식으로 변환
polynomial = PolynomialFeatures(degree=1)  

X_tr_poly=polynomial.fit_transform(X_tr)   
X_val_poly=polynomial.fit_transform(X_val)  

print(X_tr_poly.shape, X_val_poly.shape)

pr_model = LinearRegression()
pr_model.fit(X_tr_poly, y_tr)

from sklearn.metrics import mean_squared_error

y_tr_pred = pr_model.predict(X_tr_poly)
train_mse = mean_squared_error(y_tr, y_tr_pred)
print("Train MSE: %.2f" % train_mse)

y_val_pred = pr_model.predict(X_val_poly)
valid_mse = mean_squared_error(y_val, y_val_pred)
print("Valid MSE: %.2f" % valid_mse)

# 3차 다항식으로 변환
polynomial = PolynomialFeatures(degree=3)  

X_tr_poly=polynomial.fit_transform(X_tr)   
X_val_poly=polynomial.fit_transform(X_val)  

print(X_tr_poly.shape, X_val_poly.shape)

pr_model3 = LinearRegression()
pr_model3.fit(X_tr_poly, y_tr)

y_tr_pred3 = pr_model3.predict(X_tr_poly)
train_mse = mean_squared_error(y_tr, y_tr_pred3)
print("Train MSE: %.2f" % train_mse)

y_val_pred3 = pr_model3.predict(X_val_poly)
valid_mse = mean_squared_error(y_val, y_val_pred3)
print("Valid MSE: %.2f" % valid_mse)

# 12차 다항식으로 변환
polynomial = PolynomialFeatures(degree=12)  

X_tr_poly=polynomial.fit_transform(X_tr)   
X_val_poly=polynomial.fit_transform(X_val)  

print(X_tr_poly.shape, X_val_poly.shape)

pr_model12 = LinearRegression()
pr_model12.fit(X_tr_poly, y_tr)

y_tr_pred12 = pr_model12.predict(X_tr_poly)
train_mse = mean_squared_error(y_tr, y_tr_pred12)
print("Train MSE: %.2f" % train_mse)

y_val_pred12 = pr_model12.predict(X_val_poly)
valid_mse = mean_squared_error(y_val, y_val_pred12)
print("Valid MSE: %.2f" % valid_mse)

plt.figure(figsize=(12, 4)) 

plt.subplot(1, 3, 1)
plt.scatter(X_val['ambient'], y_val, label='Targets') # 실제값
plt.scatter(X_val['ambient'], y_val_pred, label='Preds') # 모델 예측값

plt.subplot(1, 3, 2)
plt.scatter(X_val['ambient'], y_val, label='Targets') # 실제값
plt.scatter(X_val['ambient'], y_val_pred3, label='Preds') # 모델 예측값

plt.subplot(1, 3, 3)
plt.scatter(X_val['ambient'], y_val, label='Targets') # 실제값
plt.scatter(X_val['ambient'], y_val_pred12, label='Preds') # 모델 예측값

plt.legend()
plt.show()

"""## L2 규제 - Ridge 모델"""

from sklearn.linear_model import Ridge

ridge = Ridge(alpha=2.5)
ridge.fit(X_tr_poly, y_tr)

y_tr_pred = ridge.predict(X_tr_poly)
train_mse = mean_squared_error(y_tr, y_tr_pred)
print("Train MSE: %.2f" % train_mse)

y_val_pred = ridge.predict(X_val_poly)
valid_mse = mean_squared_error(y_val, y_val_pred)
print("Valid MSE: %.2f" % valid_mse)

"""## L1 규제 - Lasso 모델"""

from sklearn.linear_model import Lasso

lasso = Lasso(alpha=0.5)
lasso.fit(X_tr_poly, y_tr)

y_tr_pred = lasso.predict(X_tr_poly)
train_mse = mean_squared_error(y_tr, y_tr_pred)
print("Train MSE: %.2f" % train_mse)

y_val_pred = lasso.predict(X_val_poly)
valid_mse = mean_squared_error(y_val, y_val_pred)
print("Valid MSE: %.2f" % valid_mse)

"""## L2/L1 규제 - ElasticNet 모델"""

from sklearn.linear_model import ElasticNet

elastic = ElasticNet(alpha=0.01, l1_ratio=0.7)
elastic.fit(X_tr_poly, y_tr)

y_tr_pred = elastic.predict(X_tr_poly)
train_mse = mean_squared_error(y_tr, y_tr_pred)
print("Train MSE: %.2f" % train_mse)

y_val_pred = elastic.predict(X_val_poly)
valid_mse = mean_squared_error(y_val, y_val_pred)
print("Valid MSE: %.2f" % valid_mse)

"""# 비선형 회귀 모델"""

from sklearn.tree import DecisionTreeRegressor

decision_tree = DecisionTreeRegressor(max_depth=3, random_state=2021)
decision_tree.fit(X_tr, y_tr)

y_tr_pred = decision_tree.predict(X_tr)
train_mse = mean_squared_error(y_tr, y_tr_pred)
print("Train MSE: %.2f" % train_mse)

y_val_pred = decision_tree.predict(X_val)
valid_mse = mean_squared_error(y_val, y_val_pred)
print("Valid MSE: %.2f" % valid_mse)

from sklearn.ensemble import RandomForestRegressor

random_forest = RandomForestRegressor(n_estimators=50, max_depth=3, random_state=2021)
random_forest.fit(X_tr, y_tr)

y_tr_pred = random_forest.predict(X_tr)
train_mse = mean_squared_error(y_tr, y_tr_pred)
print("Train MSE: %.2f" % train_mse)

y_val_pred = random_forest.predict(X_val)
valid_mse = mean_squared_error(y_val, y_val_pred)
print("Valid MSE: %.2f" % valid_mse)

# 가장 예측력이 좋은 알고리즘(모델)을 골라주고 그안에서도 튜닝까지 자동으로 해주는 그런건 없지요??ㅎㅎ
# 있어  Grid Search  -- auto ML해줘
from sklearn.ensemble import RandomForestRegressor

random_forest = RandomForestRegressor(n_estimators=100, max_depth=5, random_state=2021)
random_forest.fit(X_tr, y_tr)

y_tr_pred = random_forest.predict(X_tr)
train_mse = mean_squared_error(y_tr, y_tr_pred)
print("Train MSE: %.2f" % train_mse)

y_val_pred = random_forest.predict(X_val)
valid_mse = mean_squared_error(y_val, y_val_pred)
print("Valid MSE: %.2f" % valid_mse)

"""### Feature Importance"""

sns.barplot(y=X_train.columns,
            x=random_forest.feature_importances_,
            estimator=np.mean);

"""# [실습]
모터 부품의 온도를 예측하는 모델을 훈련시키고 예측 결과를 시스템에 제출합니다. (합격 점수: MSE 145 이하)
"""


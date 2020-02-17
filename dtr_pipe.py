mport pandas as pd
import numpy as np

df = pd.read_csv('./data_nas_swabc_sorted.csv')

del df['cpu-clock']
del df['mem-loads']
del df['App']
del df['Size']
del df['Thread']
del df['Run']
del df['block:block_rq_insert']
del df['block:block_rq_complete']
del df['block:block_rq_issue']

df = df.replace("nnn", np.nan).fillna(0)
df = df.astype('float64')

X = df.drop(['runtime'], axis=1)
y = df['runtime']

from sklearn.pipeline import Pipeline
from sklearn.tree import DecisionTreeRegressor
from sklearn.preprocessing import MinMaxScaler

steps = [('scaler', MinMaxScaler()), ('dtr', DecisionTreeRegressor())]
pipeline = Pipeline(steps)

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=30)

from sklearn.model_selection import GridSearchCV
import multiprocessing

parameters = {'dtr__max_depth': np.arange(3, 6), 'dtr__criterion':['mae', 'mse'], 'dtr__min_samples_split':np.arange(2, 50), 'dtr__min_samples_leaf':np.arange(2, 50)}
num_cores = multiprocessing.cpu_count()
num_folds = 5

grid = GridSearchCV(pipeline, param_grid=parameters, cv=num_folds, n_jobs=num_cores)
print("Starting GridSearchCV (n_jobs=" + str(num_cores) + ", cv=" + str(num_folds) + ")...")

grid.fit(X_train, y_train)
print("Score: %3.2f", grid.score(X_test, y_test))
print(grid.best_params_)

y_pred = grid.predict(X_test)

from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

print('Mean Absolute Error:', mean_absolute_error(y_test, y_pred))
print('Mean Squared Error:', mean_squared_error(y_test, y_pred))
print('Root Mean Squared Error:', np.sqrt(mean_squared_error(y_test, y_pred)))

score = r2_score(y_test, y_pred) * 100
print("R2 Score: ", score)

adj_r2_score = 1 - (1-score)*(len(y_test)-1)/(len(y_test)-X_test.shape[1]-1)
print("Adjusted R2 Score: ", adj_r2_score)

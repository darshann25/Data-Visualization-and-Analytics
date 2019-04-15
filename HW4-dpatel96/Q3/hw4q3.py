## Data and Visual Analytics - Homework 4
## Georgia Institute of Technology
## Applying ML algorithms to detect eye state

import numpy as np
import pandas as pd
import time

from sklearn.model_selection import cross_val_score, GridSearchCV, cross_validate, train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.svm import SVC
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, normalize
from sklearn.decomposition import PCA

######################################### Reading and Splitting the Data ###############################################
# XXX
# TODO: Read in all the data. Replace the 'xxx' with the path to the data set.
# XXX
data = pd.read_csv('./eeg_dataset.csv')

# Separate out the x_data and y_data.
x_data = data.loc[:, data.columns != "y"]
y_data = data.loc[:, "y"]

# The random state to use while splitting the data.
random_state = 100

# XXX
# TODO: Split 70% of the data into training and 30% into test sets. Call them x_train, x_test, y_train and y_test.
# Use the train_test_split method in sklearn with the parameter 'shuffle' set to true and the 'random_state' set to 100.
# XXX
x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, test_size=0.30, random_state=100)

# ############################################### Linear Regression ###################################################
# XXX
# TODO: Create a LinearRegression classifier and train it.
# XXX
regr = LinearRegression()
regr.fit(x_train, y_train)
y_pred_test = regr.predict(x_test)
y_pred_train = regr.predict(x_train)

# XXX
# TODO: Test its accuracy (on the training set) using the accuracy_score method.
# TODO: Test its accuracy (on the testing set) using the accuracy_score method.
# Note: Round the output values greater than or equal to 0.5 to 1 and those less than 0.5 to 0. You can use y_predict.round() or any other method.
# XXX
train_accuracy = accuracy_score(y_train, y_pred_train.round())
test_accuracy = accuracy_score(y_test, y_pred_test.round())

print("Training Accuracy for Linear Regression : " + str(train_accuracy))
print("Test Accuracy for Linear Regression : " + str(test_accuracy))


# ############################################### Random Forest Classifier ##############################################
# XXX
# TODO: Create a RandomForestClassifier and train it.
# XXX
clf = RandomForestClassifier(n_estimators=100, max_depth=2, random_state=0)
clf.fit(x_data, y_data)
y_pred_test = clf.predict(x_test)
y_pred_train = clf.predict(x_train)

# XXX
# TODO: Test its accuracy on the training set using the accuracy_score method.
# TODO: Test its accuracy on the test set using the accuracy_score method.
# XXX
train_accuracy = accuracy_score(y_train, y_pred_train.round())
test_accuracy = accuracy_score(y_test, y_pred_test.round())

print("Training Accuracy for Random Forest Classifier : " + str(train_accuracy))
print("Test Accuracy for Random Forest Classifier : " + str(test_accuracy))


# XXX
# TODO: Determine the feature importance as evaluated by the Random Forest Classifier.
#       Sort them in the descending order and print the feature numbers. The report the most important and the least important feature.
#       Mention the features with the exact names, e.g. X11, X1, etc.
#       Hint: There is a direct function available in sklearn to achieve this. Also checkout argsort() function in Python.
# XXX
feat_imp = clf.feature_importances_
print("Feature Importance Indices : " + str(np.argsort(feat_imp, axis=0)))

# XXX
# TODO: Tune the hyper-parameters 'n_estimators' and 'max_depth'.
#       Print the best params, using .best_params_, and print the best score, using .best_score_.
# XXX
scaler = StandardScaler()
scaler.fit(x_train)
x_train = scaler.transform(np.array(x_train))
# y_train = scaler.transform(np.array(y_train))

param_grid = {
    'max_depth': [80, 90, 100],
   'n_estimators': [100, 200, 300]
}
gridClf = GridSearchCV(clf, param_grid, cv=10)
gridClf.fit(x_train, y_train)
print("Best Parameters : " + str(gridClf.best_params_))
print("Best Score : " + str(gridClf.best_score_))

# ############################################ Support Vector Machine ###################################################
# XXX
# TODO: Pre-process the data to standardize or normalize it, otherwise the grid search will take much longer
# TODO: Create a SVC classifier and train it.
# XXX
clf = SVC()
clf.fit(x_train, y_train)
y_pred_test = clf.predict(x_test)
y_pred_train = clf.predict(x_train)

# XXX
# TODO: Test its accuracy on the training set using the accuracy_score method.
# TODO: Test its accuracy on the test set using the accuracy_score method.
# XXX
train_accuracy = accuracy_score(y_train, y_pred_train.round())
test_accuracy = accuracy_score(y_test, y_pred_test.round())

print("Training Accuracy for SVC : " + str(train_accuracy))
print("Test Accuracy for SVC : " + str(test_accuracy))

# XXX
# TODO: Tune the hyper-parameters 'C' and 'kernel' (use rbf and linear).
#       Print the best params, using .best_params_, and print the best score, using .best_score_.
# XXX
param_grid = {
    'kernel': ['linear', 'rbf'],
   'C': [0.0001, 0.1, 100]
}
gridClf = GridSearchCV(clf, param_grid, cv=10)
gridClf.fit(x_train, y_train)
print("Best Parameters : " + str(gridClf.best_params_))
print("Best Score : " + str(gridClf.best_score_))
print("CV Results : \n" + str(gridClf.cv_results_ ))

# ######################################### Principal Component Analysis #################################################
# XXX
# TODO: Perform dimensionality reduction of the data using PCA.
#       Set parameters n_component to 10 and svd_solver to 'full'. Keep other parameters at their default value.
#       Print the following arrays:
#       - Percentage of variance explained by each of the selected components
#       - The singular values corresponding to each of the selected components.
# XXX
pca = PCA(n_components=10)
pca.fit(x_train)
print("Percentage of variance explained by each of the selected components : " + str(pca.explained_variance_ratio_))
print("The singular values corresponding to each of the selected components : " + str(pca.singular_values_))


# -*- coding: utf-8 -*-
"""First Order Theorem Proving.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1yN9qUYv2Pl-70GkwCWdk3jSxR8Nu7QzQ

**Importing libraries**
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error
from sklearn.multioutput import MultiOutputRegressor
import matplotlib.pyplot as plt

"""**Load the dataset**"""

!wget https://archive.ics.uci.edu/static/public/249/first+order+theorem+proving.zip
!unzip first+order+theorem+proving.zip

!tar -xvf ml-prove.tar.gz

# Load the dataset
data = pd.read_csv("ml-prove/all-data-raw.csv", header=None)

data.head()

# Remove redundant features
data = data.drop([5, 21], axis=1)

# Split features and labels
X = data.iloc[:, :-6]
y = data.iloc[:, -6:]

# Normalize features
scaler = StandardScaler()
X = scaler.fit_transform(X)

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

# Create instances of different regression models
regressor_models = [
    LinearRegression(),
    RandomForestRegressor(),
    SVR()
]

# Train and evaluate each regression model
for model in regressor_models:
    # Create an instance of the MultiOutputRegressor
    multioutput_model = MultiOutputRegressor(model)

    # Fit the model with the target variable
    multioutput_model.fit(X_train, y_train)

    # Make predictions on the training set
    y_train_pred = multioutput_model.predict(X_train)

    # Make predictions on the test set
    y_test_pred = multioutput_model.predict(X_test)

    # Calculate evaluation metrics for each output variable
    metrics_train = []
    metrics_test = []

    for i in range(y_train.shape[1]):
        mse_train = mean_squared_error(y_train.iloc[:, i], y_train_pred[:, i])
        mse_test = mean_squared_error(y_test.iloc[:, i], y_test_pred[:, i])

        metrics_train.append(mse_train)
        metrics_test.append(mse_test)

    # Print the evaluation metrics for training set
    print('Training Set Metrics:')
    for i, mse_train in enumerate(metrics_train):
        print(f'Output {i+1} - MSE: {mse_train}')

    # Print the evaluation metrics for test set
    print('\nTest Set Metrics:')
    for i, mse_test in enumerate(metrics_test):
        print(f'Output {i+1} - MSE: {mse_test}')

    # Plot the predicted values vs. true values for the first output variable
    plt.figure(figsize=(8, 6))
    plt.scatter(y_test.iloc[:, 0], y_test_pred[:, 0], color='blue', label='Predicted')
    plt.plot([min(y_test.iloc[:, 0]), max(y_test.iloc[:, 0])], [min(y_test.iloc[:, 0]), max(y_test.iloc[:, 0])], color='red', linestyle='--', label='True')
    plt.xlabel('True Value')
    plt.ylabel('Predicted Value')
    plt.title('Predicted vs. True Values (Output 1)')
    plt.legend()
    plt.show()

    print('---------------------------')

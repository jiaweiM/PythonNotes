import numpy as np
import pandas as pd
import tensorflow as tf

california_housing_dataframe = pd.read_csv("../datasets/california_housing_train.csv", sep=",")
california_housing_dataframe = california_housing_dataframe.reindex(
    np.random.permutation(california_housing_dataframe.index))
california_housing_dataframe['median_house_value'] /= 1000.0
print(california_housing_dataframe.describe())

my_feature = california_housing_dataframe[["total_rooms"]]

feature_columns = [tf.feature_column.numeric_column("total_rooms")]

targets = california_housing_dataframe["median_house_value"]

# Use gradient descent as the optimizer for training the model.
my_optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.0000001)
my_optimizer = tf.contrib.estimator.clip_gradients_by_norm(my_optimizer, 5.0)

# Configure the linear regression model with our feature columns and optimizer.
# Set a learning rate of 0.0000001 for Gradient Descent.
linear_regressor = tf.estimator.LinearRegressor(
    feature_columns=feature_columns,
    optimizer=my_optimizer
)

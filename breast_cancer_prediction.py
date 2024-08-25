# -*- coding: utf-8 -*-
"""Breast_Cancer_Prediction.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/14-yZBRkFBO30nmqDz-0MjrUSx4pSxVKu
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

from google.colab import files

uploaded = files.upload()

df = pd.read_csv('data (1).csv')

df.head(n=5)

group = df.groupby('diagnosis');

group.mean()

print(df.shape)

df.describe()

"""lets check the no of malignant and benign cases"""

group.size()

"""Changing the malignant and benign to 1 and 0 respectively"""

df['diagnosis'] = df['diagnosis'].apply(lambda x: '1' if x == 'M' else '0')

print(df.columns)

"""Setting the id column as index as it is the predefined id is not irrelevant for our data analysis"""

df = df.set_index('id')

df.head()

df['Unnamed: 32'].isna().sum()

len(df['Unnamed: 32'])

"""Since all values of Unnamed : 32 is zero we can delete this column"""

del df['Unnamed: 32']

df.head()

#lets visualize the data by making some density plots

df.plot(kind='density', subplots=True, layout=(5,7), sharex=False, legend=False, fontsize=1)
plt.show()

from sklearn.model_selection import train_test_split

Y = df['diagnosis'].values
X = df.drop('diagnosis', axis=1).values

X_train, X_test, Y_train, Y_test = train_test_split (X, Y, test_size = 0.20, random_state=21)

from sklearn.preprocessing import StandardScaler

# Initialize the scaler
scaler = StandardScaler()

# Fit the scaler on the training data and transform both training and test data
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# applying logistic regression

lr_model = LogisticRegression()
lr_model.fit(X_train_scaled, Y_train)

Y_pred = lr_model.predict(X_test_scaled)

#now checking the accuracy

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report

# Convert the labels to integer type if necessary
Y_test = Y_test.astype(int)
Y_pred = Y_pred.astype(int)

# Accuracy
accuracy = accuracy_score(Y_test, Y_pred)
print(f'Accuracy: {accuracy}')

# Precision
precision = precision_score(Y_test, Y_pred, pos_label=1)
print(f'Precision: {precision}')

# Recall
recall = recall_score(Y_test, Y_pred, pos_label=1)
print(f'Recall: {recall}')

# F1-score
f1 = f1_score(Y_test, Y_pred, pos_label=1)
print(f'F1-score: {f1}')

from sklearn.metrics import confusion_matrix, classification_report

# Confusion Matrix
conf_matrix = confusion_matrix(Y_test, Y_pred)
print(f'Confusion Matrix:\n{conf_matrix}')

# Classification Report
class_report = classification_report(Y_test, Y_pred)
print(f'Classification Report:\n{class_report}')

"""**Learning Curves:** These curves show the training and validation scores as a function of the number of training examples. They help diagnose if a model is underfitting or overfitting."""

from sklearn.model_selection import learning_curve

# Generate learning curves
train_sizes, train_scores, test_scores = learning_curve(lr_model, X_train_scaled, Y_train, cv=5, scoring='accuracy', n_jobs=-1, train_sizes=np.linspace(0.1, 1.0, 10))

# Calculate mean and standard deviation
train_scores_mean = np.mean(train_scores, axis=1)
train_scores_std = np.std(train_scores, axis=1)
test_scores_mean = np.mean(test_scores, axis=1)
test_scores_std = np.std(test_scores, axis=1)

# Plot learning curves
plt.figure(figsize=(8, 6))
plt.fill_between(train_sizes, train_scores_mean - train_scores_std, train_scores_mean + train_scores_std, alpha=0.1, color='blue')
plt.fill_between(train_sizes, test_scores_mean - test_scores_std, test_scores_mean + test_scores_std, alpha=0.1, color='orange')
plt.plot(train_sizes, train_scores_mean, 'o-', color='blue', label='Training score')
plt.plot(train_sizes, test_scores_mean, 'o-', color='orange', label='Cross-validation score')
plt.xlabel('Training Examples')
plt.ylabel('Score')
plt.title('Learning Curves')
plt.legend(loc='best')
plt.show()

"""**ROC Curve :** ROC (Receiver Operating Characteristic) curve is a plot of the true positive rate (TPR) against the false positive rate (FPR) at various threshold settings. It shows the trade-off between sensitivity and specificity.

"""

from sklearn.metrics import roc_curve, roc_auc_score

# Predict probabilities
Y_pred_prob = lr_model.predict_proba(X_test_scaled)[:, 1]

# Calculate ROC curve
fpr, tpr, thresholds = roc_curve(Y_test, Y_pred_prob)
roc_auc = roc_auc_score(Y_test, Y_pred_prob)

# Plot ROC curve
plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, color='blue', label=f'ROC Curve (area = {roc_auc:.2f})')
plt.plot([0, 1], [0, 1], color='gray', linestyle='--')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic (ROC) Curve')
plt.legend(loc='lower right')
plt.show()


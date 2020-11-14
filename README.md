# Analyzing Vegan Trends on Twitter

## Contents
- [/Notebooks](Notebooks)<br>
[One notebook ](Notebooks/csv_postgresql.ipynb) with basic postgres usage and [another ](Notebooks/fraud_prediction.ipynb) with the bulk of the project in walkthrough format
- [streamlit_app.py](streamlit_app.py)<br>
The guts of a streamlit app for fine-tuning the model using prediction threshold
- [helper_functions.py](helper_functions.py)<br>
Functions used in cleaning the data
- [card_fraud_predictions.pdf](card_fraud_predictions.pdf)<br>
The slides for the project presentation
- [app_preview.mov](app_preview.mov)<br>
A video preview of the streamlit app

## Description
This repository contains a working model to predict credit card fraud based on a [Kaggle dataset](https://www.kaggle.com/c/ieee-fraud-detection) provided by the Vesta corporation. The final model produced is an XG Boost classifier model that predicts a binary of 1 for a fraudulent transaction and 0 for valid transaction.

## Features and Target Variables
- Target Variable: Fraud or Valid
- Features: Matched information, timedelta, transaction amount, debit vs. credit, product code, general card information

## Data Used
- [Vesta Corporation Transaction Information](https://www.kaggle.com/c/ieee-fraud-detection)

## Tools Used
- PostgreSQL
- XG Boost
- Logistic Regression
- Random Oversampler
- SMOTE
- Streamlit
- Seaborn
- Matplotlib

## Potential Impact
Vesta Corporation put out this dataset to encourage data scientists to help with the fight against credit card fraud. In 2018, [the worldwide cost of credit card fraud was over $24 billion](https://dataprot.net/statistics/credit-card-fraud-statistics/). With this knowledge, I hope my work, or the work of other data scientists exploring this dataset, will be able to aid in the fight again fraudulent transactions.
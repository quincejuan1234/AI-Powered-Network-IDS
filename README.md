# AI-Powered Network Intrusion Detection System

An AI-driven cybersecurity application that detects malicious network traffic using machine learning models trained on a subset of the CIC-IDS2017 dataset. The system includes an interactive dashboard for threat analysis and is designed for future integration with SIEM and real-time monitoring systems.

## Overview

Cybersecurity threats such as DDoS attacks, brute-force attempts, and network intrusions are increasingly complex and difficult to detect using traditional rule-based systems.

This project implements a machine learning-based intrusion detection system that:
- classifies network traffic as benign or malicious
- detects different types of cyberattacks
- provides evaluation metrics and visualizations
- displays results through an interactive dashboard

The system is designed as both a course project and a foundation for a scalable cybersecurity platform.

## Features

- Machine learning-based intrusion detection
- Model evaluation with accuracy, precision, recall, and F1-score
- Visualizations such as confusion matrix and performance charts
- Interactive dashboard built with Streamlit
- Scalable structure for future extensions
- Future-ready design for SIEM integration and real-time monitoring

## Dataset

This project uses a subset of the CIC-IDS2017 dataset, which contains realistic network traffic data including:
- benign traffic
- DoS and DDoS attacks
- brute-force attacks
- port scanning activity

Note: Due to dataset size, raw data is not included in this repository.

## Tech Stack

- Python 3
- Pandas
- NumPy
- Scikit-learn
- Matplotlib
- Seaborn
- Streamlit
- Joblib

## Project Structure

```text
ai-intrusion-detection-system/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── data/
│   ├── raw/
|   ├── sample/
│   └── processed/
│
├── notebooks/
|   ├── 01_data_exploration.ipynb
|   ├── 02_preprocessing.ipynb
│   └── 03_model_experiments.ipynb
│
├── src/
|   ├── __init__.py
|   ├── config.py
|   ├── features.py
│   ├── preprocess.py
│   ├── train.py
│   ├── evaluate.py
|   ├── utils.py
│   └── predict.py
│
├── app/
│   └── app.py
│
├── models/
│
├── outputs/
│   ├── figures/
│   ├── metrics/
│   └── reports/
|
├── scripts/
|   ├── run_app.py
|   └── run_training.py
|
├── tests/
|   ├── test_features.py
|   ├── test_predict.py
|   └── test_preprocess.py
│
└── docs/
    └── proposal
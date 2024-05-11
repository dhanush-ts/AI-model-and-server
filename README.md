# Namma Niddhi - Credit Score and Risk Evaluation

## Overview
Namma Niddhi is a project developed for Hack Bangalore, aimed at determining credit scores and risk evaluations for businesses. The project utilizes Python, Flask, PyPDF2, and regular expressions to extract financial data from PDF files and calculate credit scores and risk evaluations automatically.

## Features
- *PDF Data Extraction:* The project extracts financial data from PDF files uploaded by users.
- *Credit Risk Evaluation:* Calculates credit risk scores based on extracted financial ratios.
- *Credit Score Calculation:* Calculates credit scores based on financial ratios.
- *Sanctioned Amount Extraction:* Extracts sanctioned amounts and PAN numbers from PDF files.

## Prerequisites
- Python 3.x
- Flask
- PyPDF2
- NumPy

## Installation
1. Clone the repository:
git clone https://github.com/dhanush-ts/namma-niddhi.git

2. Install the required dependencies:
pip install Flask PyPDF2 numpy


## Usage
1. Run the Flask application:
python app.py
2. Access the application through a web browser or using API endpoints.

## API Endpoints

### 1. Calculate Credit
- *URL:* /calculate_credit
- *Method:* POST
- *Parameters:*
- pdf_file: PDF file containing financial data.
- *Returns:*
- credit_risk_score: Calculated credit risk score.
- credit_score: Calculated credit score.

### 2. Sanctioned Amount
- *URL:* /sanction
- *Method:* POST
- *Parameters:*
- pdf_file: PDF file containing financial data.
- *Returns:*
- sanctioned: Sanctioned amount.
- PAN: PAN number.

## Created by
- *Dhanush TS*
- GitHub: [dhanush-ts](https://github.com/dhanush-ts)
- *Team Name:* Xcaliber

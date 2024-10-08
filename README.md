
# Personality Prediction System via CV Analysis

This repository contains a Flask application for predicting personality traits based on the analysis of resumes. The application extracts relevant information from the resumes and uses machine learning models to provide insights into the candidate's personality.

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Files](#files)

## Project Overview

This project aims to automate the analysis of resumes to predict personality traits using AI models. The application is hosted on the cloud and provides a user-friendly web interface for uploading resumes and obtaining predictions.

## Features

- Resume parsing and extraction of details such as education, skills, work experience, etc.
- Personality prediction based on extracted traits.
- CSV outputs for both extracted details and traits.

## Installation

To install and run this Flask application locally, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/khushali02/P15-Personality-PredicKon-System-via-CV-Analysis
   cd P15-Personality-PredicKon-System-via-CV-Analysis
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your environment variables**:
   - Add your API key to the `ai_prediction.py` file. {https://aistudio.google.com/app/apikey}
   

5. **Run the Flask application**:
   ```bash
   python app.py
   ```

6. **Access the application**:
   Open your browser and go to `http://127.0.0.1:5000/`.

## Usage

1. Upload resumes via the web interface.
2. The application will parse the resumes and extract relevant details.
3. Personality predictions are generated based on the extracted details.
4. Results are displayed on the web interface and saved as CSV files.

## Files

- **app.py**: The main Flask application file.
- **ai_prediction.py**: Contains the logic for personality prediction using AI models.
- **prediction.py**: Handles the prediction processes.
- **resume_extraction.py**: Contains functions for extracting details from resumes.
- **requirements.txt**: Lists all Python dependencies required to run the project.
- **uploads/**: Directory to store uploaded resume files.
- ***.csv**: Files generated containing extracted details and personality traits.

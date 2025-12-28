Project Title: Indian Agricultural Data Visualization Platform
Overview
This project develops a comprehensive platform for visualizing and analyzing Indian agricultural data from district and state levels, sourced from ICRISAT-District Level Data. It integrates EDA, SQL queries, Power BI dashboards, and machine learning for forecasting, aiming to support farmers, policymakers, and researchers in optimizing agricultural practices.
Technologies Used

Python (Pandas, Matplotlib, Seaborn, Plotly, Scikit-learn)
SQL (for querying and database management)
Power BI (for interactive dashboards)
Data Source: ICRISAT-District Level Data (cleaned and processed into cleaned_agri_data.csv)

Installation

Clone the repository: git clone <repo-url>
Install dependencies: pip install -r requirements.txt
Load the dataset: Place cleaned_agri_data.csv in the project directory.
Run EDA script: python eda.py
Open Power BI file: agri_dashboard.pbix

Usage

Run SQL queries in your database tool to answer analytical questions.
Use Python scripts for data cleaning, EDA, and ML modeling.
Interact with Power BI dashboard for visualizations.

Project Structure

data/: Contains the dataset.
scripts/: Python scripts for cleaning, EDA, and modeling.
sql/: SQL queries for analysis.
dashboard/: Power BI files.
docs/: Documentation.

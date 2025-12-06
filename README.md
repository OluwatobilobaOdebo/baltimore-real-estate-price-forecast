# 📈 Baltimore County 5-Year Real Estate Price Forecast  
### *Predictive Analytics Dashboard Using Zillow ZHVI Data (Streamlit + Python)*

This project builds an **end-to-end data analytics and machine learning pipeline** to forecast **Baltimore County, MD home prices for the next 5 years**, using Zillow ZHVI time-series data.  
It includes:

- A full **data processing workflow** (raw → cleaned → forecast-ready)
- A **predictive model** using time-series regression
- A **Streamlit dashboard** for interactive exploration
- A **Jupyter notebook** with the complete methodology and analysis
- Clean, modular project structure ideal for real-world analytics work

This project is designed for **home buyers, real estate investors, and agents** looking to understand price trends and expected growth across Baltimore County ZIP codes.

---

## 🗂️ Repository Structure

baltimore-real-estate-price-forecast/
│
├── app/
│ └── streamlit_app.py # Interactive Streamlit dashboard
│
├── data/
│ ├── processed/ # Cleaned & forecast-ready datasets
│ │ ├── bc_yearly_home_values.csv
│ │ ├── forecast_summary.csv
│ │ └── full_timeseries_with_forecast.csv
│ └── raw/ # (Ignored by Git; contains large ZHVI dataset)
│
├── notebooks/
│ └── 01_baltimore_real_estate_modeling.ipynb
│
├── reports/
│ └── figures/ # Exported charts
│
├── requirements.txt
├── LICENSE
└── README.md

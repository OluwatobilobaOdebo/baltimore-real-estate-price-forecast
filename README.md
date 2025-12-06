# Baltimore County 5-Year Real Estate Price Forecast  
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

## Project Overview

This end-to-end analytics solution:

1. **Transforms Zillow ZHVI time-series data** for Baltimore County ZIP codes  
2. **Builds a simple yet effective forecasting model**  
   - Last-value projection  
   - 5-year price forecast  
   - 5-year percent change  
   - Annualized rate of return (CAGR)
3. **Generates ZIP-level KPIs**  
4. **Visualizes price history + forecast** through an interactive Streamlit dashboard  

---

##  Features

### ** Explore Home Price Trends by ZIP Code**
Interactive dropdown to select any Baltimore County ZIP code.

### ** Key Real-Estate KPIs**
For each ZIP:
- Current median price  
- Forecasted median price (5 years out)  
- 5-year growth (%)  
- Annualized growth rate (CAGR)  

### ** Interactive Trend Charts**
- Clean historical ZHVI price trends  
- Forecasts overlayed for clear visibility  

### ** Fully Reproducible Notebook**
Includes:
- Data cleaning  
- Feature engineering  
- Forecasting computation  
- Visualizations  

### ** Modular, Professional Code Structure**
Easily extendable for:
- ARIMA/LSTM forecasting  
- County-level models  
- Additional real estate KPIs  
- Tableau dashboards  

---

## Dataset Description

### **Source**  
**Zillow Home Value Index (ZHVI)**  
https://www.zillow.com/research/data/

### **Dataset Characteristics**
- Monthly median home values by ZIP code  
- Includes many Maryland ZIPs  
- Raw file size is ~110 MB (excluded via `.gitignore`)  
- Contains time series from early 2000s → present

### **Filtered Dataset**
This project extracts only **Baltimore County ZIP codes**, reshapes them into long format, and aggregates yearly trends.

---


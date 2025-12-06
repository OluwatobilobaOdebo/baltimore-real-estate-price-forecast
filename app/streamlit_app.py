import pathlib
from typing import Tuple

import altair as alt
import pandas as pd
import streamlit as st


# ------------------------------------------------------------
#  Page + Global Config
# ------------------------------------------------------------
st.set_page_config(
    page_title="Baltimore County 5-Year Real Estate Price Forecast",
    layout="wide",
)


PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA_PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"


# ------------------------------------------------------------
#  Data Loading
# ------------------------------------------------------------
@st.cache_data(show_spinner=True)
def load_data() -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Load processed time series + summary data for the dashboard.

    Returns
    -------
    ts : DataFrame
        Long-format time series with columns:
        Zip, Date, MedianValue, Type (Historical/Forecast)
    summary : DataFrame
        Per-ZIP summary with KPIs:
        Zip, CurrentValue, Forecast5Yr, GrowthPct5Yr, CAGR
    """
    ts_path = DATA_PROCESSED_DIR / "full_timeseries_with_forecast.csv"
    summary_path = DATA_PROCESSED_DIR / "forecast_summary.csv"

    ts = pd.read_csv(ts_path, parse_dates=["Date"])
    summary = pd.read_csv(summary_path)

    # Basic sanity checks / cleaning
    ts["Zip"] = ts["Zip"].astype(str)
    summary["Zip"] = summary["Zip"].astype(str)

    return ts, summary


# ------------------------------------------------------------
#  UI Sections
# ------------------------------------------------------------
def render_header() -> None:
    st.title("Baltimore County 5-Year Real Estate Price Prediction Dashboard")

    st.markdown(
        """
        This dashboard uses historical **Zillow Home Value Index (ZHVI)** data to model and 
        forecast typical home values in **Baltimore County, MD** for the next 5 years.

        **Personas:** Home buyers, real estate investors, and real estate agents.  
        **KPIs:** Current median price, forecasted median price in 5 years, 5-year % growth, annualized growth (CAGR).
        """
    )


def render_sidebar(zip_options) -> str:
    st.sidebar.header("Filters")

    selected_zip = st.sidebar.selectbox(
        "Select ZIP Code",
        options=zip_options,
        index=0,
    )

    return selected_zip


def render_kpis(zip_code: str, summary_row: pd.Series) -> None:
    st.subheader(f"Key Metrics – ZIP {zip_code}")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Current Median Value",
        f"${summary_row['CurrentValue']:,.0f}",
    )

    col2.metric(
        "Forecasted Value in 5 Years",
        f"${summary_row['Forecast5Yr']:,.0f}",
    )

    col3.metric(
        "5-Year Growth",
        f"{summary_row['GrowthPct5Yr']:.1f}%",
        delta=f"{summary_row['GrowthPct5Yr']:.1f}%"
    )

    col4.metric(
        "Annualized Growth (CAGR)",
        f"{summary_row['CAGR']:.1f}%",
    )


def render_trend_chart(zip_ts: pd.DataFrame) -> None:
    st.subheader("Historical Trend and 5-Year Forecast")

    hist_df = zip_ts[zip_ts["Type"] == "Historical"].copy()
    fc_df = zip_ts[zip_ts["Type"] == "Forecast"].copy()

    if hist_df.empty and fc_df.empty:
        st.info("No time series data available for this ZIP.")
        return

    base = alt.Chart().encode(
        x=alt.X("Date:T", title="Year"),
        y=alt.Y("MedianValue:Q", title="Typical Home Value ($)"),
        tooltip=[
            alt.Tooltip("year(Date):O", title="Year"),
            alt.Tooltip("MedianValue:Q", title="Value", format="$.0f"),
            alt.Tooltip("Type:N"),
        ],
    )

    hist_line = base.mark_line(color="#1f77b4", strokeWidth=2).encode(
        alt.Color("Type:N", scale=None)
    ).transform_filter(
        alt.datum.Type == "Historical"
    ).transform_calculate(
        Type="'Historical'"
    )

    fc_line = base.mark_line(color="#ff7f0e", strokeDash=[4, 4], strokeWidth=2).encode(
        alt.Color("Type:N", scale=None)
    ).transform_filter(
        alt.datum.Type == "Forecast"
    ).transform_calculate(
        Type="'Forecast'"
    )

    # We pass the full dataset once and then filter inside the charts
    chart = (hist_line + fc_line).properties(height=400)

    st.altair_chart(chart.transform_calculate(), use_container_width=True)


def render_trend_chart_simple(zip_ts: pd.DataFrame) -> None:
    """Simpler version of the Altair chart using explicit data (more robust)."""
    st.subheader("Historical Trend and 5-Year Forecast")

    hist_df = zip_ts[zip_ts["Type"] == "Historical"].copy()
    fc_df = zip_ts[zip_ts["Type"] == "Forecast"].copy()

    if hist_df.empty:
        st.info("No historical data available for this ZIP.")
        return

    # Historical line
    hist_line = (
        alt.Chart(hist_df)
        .mark_line(color="#1f77b4", strokeWidth=2)
        .encode(
            x=alt.X("Date:T", title="Year"),
            y=alt.Y("MedianValue:Q", title="Typical Home Value ($)"),
            tooltip=[
                alt.Tooltip("year(Date):O", title="Year"),
                alt.Tooltip("MedianValue:Q", title="Value", format="$.0f"),
                alt.Tooltip("Type:N"),
            ],
        )
    )

    # Forecast line (if exists)
    if not fc_df.empty:
        fc_line = (
            alt.Chart(fc_df)
            .mark_line(color="#ff7f0e", strokeDash=[4, 4], strokeWidth=2)
            .encode(
                x="Date:T",
                y="MedianValue:Q",
                tooltip=[
                    alt.Tooltip("year(Date):O", title="Year"),
                    alt.Tooltip("MedianValue:Q", title="Value", format="$.0f"),
                    alt.Tooltip("Type:N"),
                ],
            )
        )
        chart = hist_line + fc_line
    else:
        chart = hist_line

    st.altair_chart(chart.properties(height=400), use_container_width=True)


def render_data_table(zip_ts: pd.DataFrame) -> None:
    with st.expander("Show underlying data"):
        display_df = zip_ts.sort_values("Date").copy()
        display_df["Date"] = display_df["Date"].dt.date
        st.dataframe(display_df, use_container_width=True)


def render_insights(selected_zip: str, zip_ts: pd.DataFrame, summary_row: pd.Series) -> None:
    st.subheader("Automated Insights")

    hist = zip_ts[zip_ts["Type"] == "Historical"].copy()
    if hist.empty:
        st.write("Not enough historical data to generate insights for this ZIP.")
        return

    latest_year = hist["Date"].dt.year.max()
    latest_value = hist[hist["Date"].dt.year == latest_year]["MedianValue"].iloc[0]
    forecast_value = summary_row["Forecast5Yr"]
    growth = summary_row["GrowthPct5Yr"]

    if forecast_value > latest_value:
        st.write(
            f"📈 **ZIP {selected_zip} is expected to appreciate by "
            f"{growth:.1f}% over the next 5 years.**"
        )
    elif forecast_value < latest_value:
        st.write(
            f"📉 **ZIP {selected_zip} is expected to decline by "
            f"{abs(growth):.1f}% over the next 5 years.**"
        )
    else:
        st.write(
            f"⏸ **ZIP {selected_zip} is expected to remain roughly flat over the next 5 years.**"
        )

    st.write(
        "These estimates are based on Zillow ZHVI ZIP-level time-series data and a Prophet "
        "forecasting model trained on historical trends."
    )


# ------------------------------------------------------------
#  Main App
# ------------------------------------------------------------
def main() -> None:
    # Load data
    ts, summary = load_data()

    if ts.empty or summary.empty:
        st.error("Processed data files are empty or missing. "
                 "Please run the modeling notebook to regenerate them.")
        return

    render_header()

    # Sidebar filter
    zip_options = sorted(ts["Zip"].unique().tolist())
    selected_zip = render_sidebar(zip_options)

    # Filter datasets for selected ZIP
    zip_ts = ts[ts["Zip"] == selected_zip].copy()
    zip_summary = summary[summary["Zip"] == selected_zip]

    if zip_summary.empty:
        st.error(f"No summary data found for ZIP {selected_zip}.")
        return

    zip_summary_row = zip_summary.iloc[0]

    # KPIs
    render_kpis(selected_zip, zip_summary_row)

    # Trend chart
    render_trend_chart_simple(zip_ts)

    # Data table
    render_data_table(zip_ts)

    # Insights
    render_insights(selected_zip, zip_ts, zip_summary_row)


if __name__ == "__main__":
    main()

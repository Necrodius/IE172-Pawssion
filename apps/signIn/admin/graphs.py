import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output
from datetime import date
import pandas as pd
import plotly.graph_objects as go

from app import app
from dbconnect import getDataFromDB

# Function to calculate dates when rescues were added based on their age
def calculate_rescue_dates(rescue_ages):
    today = pd.Timestamp(date.today())
    return today - pd.to_timedelta(rescue_ages * 365, unit="d")

# Layout
layout = html.Div(
    [
        html.Div(id="admin-sidebar", style={"width": "250px", "flexShrink": 0}),
        html.Div(
            [
                dbc.Row(
                    dbc.Col(
                        html.H2(
                            "Adoption, Application, and Rescue Trends Over Time",
                            style={"color": "#dba514", "font-weight": "bold"},
                        ),
                        width="auto",
                    ),
                    className="mb-4",
                ),
                dbc.Row(
                    [
                        dbc.Col(html.Label("Select Time Period:"), width=2),
                        dbc.Col(
                            dcc.Dropdown(
                                id="time-filter",
                                options=[
                                    {"label": "Month", "value": "M"},
                                    {"label": "Quarter", "value": "Q"},
                                    {"label": "Year", "value": "Y"},
                                    {"label": "Decade", "value": "10Y"},
                                ],
                                value="M",  # Default to Month
                                clearable=False,
                            ),
                            width=4,
                        ),
                    ],
                    className="mb-4",
                ),
                html.Div(
                    [dcc.Graph(id="trends-graph")],
                    style={"margin-bottom": "20px"},
                ),
            ],
            className="customer-admin-menu",
        ),
    ]
)

# Prepare cumulative totals across all time
def prepare_cumulative_totals(df, date_column, label, all_dates):
    if not df.empty:
        df[label] = 1  # Add a column to represent each record as a count of 1
        df = df.groupby(date_column)[label].sum()  # Daily totals
        df = df.reindex(all_dates, fill_value=0).cumsum().reset_index()
        df.columns = ["date", label]
        return df
    return pd.DataFrame({"date": all_dates, label: 0})

# Callback to load and display the graph
@app.callback(Output("trends-graph", "figure"), Input("time-filter", "value"))
def generate_trends_graph(time_filter):
    today = pd.Timestamp.today()
    
    # Define the full date range across all time
    earliest_date = pd.Timestamp("2000-01-01")  # Arbitrary early start date
    all_dates = pd.date_range(start=earliest_date, end=today)

    # Fetch and process adoption data
    adoption_query = """
        SELECT a.interviewDate AS adoption_date
        FROM Adoption ad
        JOIN Application a ON ad.applicationID = a.applicationID
        WHERE a.interviewDate IS NOT NULL
    """
    adoption_data = getDataFromDB(adoption_query, [], ["adoption_date"])

    # Fetch and process application data
    application_query = "SELECT interviewDate AS application_date FROM Application WHERE interviewDate IS NOT NULL"
    application_data = getDataFromDB(application_query, [], ["application_date"])

    # Fetch and process rescue data
    rescue_query = "SELECT age FROM Rescue"
    rescue_data = getDataFromDB(rescue_query, [], ["age"])
    rescue_dates = calculate_rescue_dates(rescue_data["age"]) if not rescue_data.empty else pd.Series()

    # Prepare DataFrames
    adoption_df = pd.DataFrame({"date": pd.to_datetime(adoption_data["adoption_date"], errors="coerce")}).dropna()
    application_df = pd.DataFrame({"date": pd.to_datetime(application_data["application_date"], errors="coerce")}).dropna()
    rescue_df = pd.DataFrame({"date": rescue_dates}).dropna()

    # Compute cumulative totals for the full date range
    adoption_counts = prepare_cumulative_totals(adoption_df, "date", "Adoptions", all_dates)
    application_counts = prepare_cumulative_totals(application_df, "date", "Applications", all_dates)
    rescue_counts = prepare_cumulative_totals(rescue_df, "date", "Rescues", all_dates)

    # Merge cumulative counts
    full_data = pd.DataFrame({"date": all_dates})
    full_data = full_data.merge(adoption_counts, on="date", how="left")
    full_data = full_data.merge(application_counts, on="date", how="left")
    full_data = full_data.merge(rescue_counts, on="date", how="left")

    # Apply the time filter to the x-axis range (but keep cumulative values)
    if time_filter == "M":
        start_date = today - pd.DateOffset(months=1)
    elif time_filter == "Q":
        start_date = today - pd.DateOffset(months=3)
    elif time_filter == "Y":
        start_date = today - pd.DateOffset(years=1)
    elif time_filter == "10Y":
        start_date = today - pd.DateOffset(years=10)
    
    filtered_data = full_data[full_data["date"] >= start_date]

    # Plot the graph
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=filtered_data["date"], y=filtered_data["Adoptions"], mode="lines", name="Adoptions", line=dict(color="green")))
    fig.add_trace(go.Scatter(x=filtered_data["date"], y=filtered_data["Applications"], mode="lines", name="Applications", line=dict(color="blue")))
    fig.add_trace(go.Scatter(x=filtered_data["date"], y=filtered_data["Rescues"], mode="lines", name="Rescues", line=dict(color="orange")))

    # Dynamically set Y-axis range
    max_y_value = filtered_data[["Adoptions", "Applications", "Rescues"]].max().max()
    fig.update_layout(
        title="Cumulative Trends of Adoptions, Applications, and Rescues",
        xaxis_title="Date",
        yaxis_title="Cumulative Count",
        xaxis=dict(range=[start_date, today], showgrid=True, gridcolor="#ddd"),
        yaxis=dict(range=[0, max_y_value + 1], showgrid=True, gridcolor="#ddd"),
        height=500,
        margin=dict(l=20, r=20, t=40, b=20),
        plot_bgcolor="white",
        legend=dict(x=0, y=1),
    )

    return fig



import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State
from dbconnect import getDataFromDB
from app import app

# Layout
layout = dbc.Container(
    fluid=True,
    children=[
        # Page Header
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        [
                            html.H3("My Adoption Applications", className="mb-0", style={"fontWeight": "bold"}),
                            html.P("Track the progress of your submitted applications here.", className="mb-0"),
                        ],
                        style={
                            "backgroundColor": "#2a9d8f",
                            "padding": "20px",
                            "borderRadius": "10px",
                            "color": "white",
                            "textAlign": "center",
                        },
                    ),
                    width=12,
                ),
            ],
            className="mb-4",
        ),

        # Applications Table Container
        dbc.Row(
            [
                dbc.Col(
                    html.Div(
                        id="applications-table",
                        className="shadow-sm rounded",
                        style={
                            "backgroundColor": "#fff",
                            "padding": "20px",
                            "borderRadius": "10px",
                            "boxShadow": "0 4px 8px rgba(0,0,0,0.1)",
                        },
                    ),
                    width=12,
                )
            ],
            justify="center",
        ),
    ],
    style={
        "padding": "30px",
        "backgroundColor": "#FAF3EB",
        "minHeight": "100vh",
        "fontFamily": "Arial, sans-serif",
    },
)

# Callbacks
@app.callback(
    Output("applications-table", "children"),
    Input("user-session", "data"),
)
def populate_application_history(user_session):
    if not user_session or "userID" not in user_session:
        return dbc.Alert(
            "You must be logged in to view your applications.",
            color="danger",
            className="text-center",
            style={"fontSize": "1.2rem", "marginTop": "20px"},
        )

    user_id = user_session["userID"]

    # Query to get application data
    query = """
        SELECT
            a.applicationID,
            a.interviewDate,
            a.interviewTime,
            a.approval,
            a.adoptedTo,
            r.rescueName
        FROM Application a
        JOIN Rescue r ON a.rescueID = r.rescueID
        WHERE a.userID = %s
        ORDER BY a.applicationID DESC
    """
    params = [user_id]
    columns = ["applicationID", "interviewDate", "interviewTime", "approval", "adoptedTo", "rescueName"]
    applications = getDataFromDB(query, params, columns)

    if applications.empty:
        return dbc.Alert(
            "No applications found.",
            color="warning",
            className="text-center",
            style={"fontSize": "1.2rem", "marginTop": "20px"},
        )

    # Generate table rows
    rows = []
    for _, row in applications.iterrows():
        interview_status = "PENDING"
        if row["approval"] is True:
            interview_status = html.Span("APPROVED", className="badge bg-success")
        elif row["approval"] is False:
            interview_status = html.Span("UNAPPROVED", className="badge bg-danger")

        adoption_status = "PENDING"
        if row["adoptedTo"] == user_id:
            adoption_status = html.Span("GRANTED", className="badge bg-success")
        elif row["adoptedTo"] is not None:
            adoption_status = html.Span("NOT GRANTED", className="badge bg-danger")

        interview_schedule = (
            f"{row['interviewDate']} {row['interviewTime']}" if row["interviewDate"] and row["interviewTime"] else "N/A"
        )

        rows.append(
            html.Tr(
                [
                    html.Td(row["applicationID"], style={"verticalAlign": "middle", "textAlign": "center"}),
                    html.Td(row["interviewDate"] or "N/A", style={"verticalAlign": "middle", "textAlign": "center"}),
                    html.Td(row["rescueName"], style={"verticalAlign": "middle", "textAlign": "center"}),
                    html.Td(interview_schedule, style={"verticalAlign": "middle", "textAlign": "center"}),
                    html.Td(interview_status, style={"verticalAlign": "middle", "textAlign": "center"}),
                    html.Td(adoption_status, style={"verticalAlign": "middle", "textAlign": "center"}),
                ]
            )
        )

    # Return the populated table
    return dbc.Table(
        [
            html.Thead(
                html.Tr(
                    [
                        html.Th("APPLICATION ID", className="text-center"),
                        html.Th("APPLICATION DATE", className="text-center"),
                        html.Th("NAME OF RESCUE", className="text-center"),
                        html.Th("INTERVIEW SCHEDULE", className="text-center"),
                        html.Th("INTERVIEW STATUS", className="text-center"),
                        html.Th("ADOPTION STATUS", className="text-center"),
                    ]
                ),
                style={"backgroundColor": "#2a9d8f", "color": "white"},
            ),
            html.Tbody(rows),
        ],
        bordered=True,
        hover=True,
        responsive=True,
        striped=True,
        style={"fontSize": "0.9rem", "color": "#333", "marginBottom": "20px"},
    )

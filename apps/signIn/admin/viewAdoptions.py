import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, dcc, html, ALL
from dash.exceptions import PreventUpdate
from app import app
from dbconnect import getDataFromDB, modifyDB
import pandas as pd

# Layout
layout = html.Div(
    [
        # Sidebar placeholder
        html.Div(id="admin-sidebar", style={"width": "250px", "flexShrink": 0}),
        
        # Main content
        html.Div(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            html.H3("VIEW ADOPTION APPLICATIONS", style={"color": "#fcbf49", "marginTop": "20px", "fontWeight": "bold"}),
                            width=8
                        ),
                    ],
                    justify="between",
                ),

                # Applications Table
                html.Div(
                    id="applications-table-container",
                    className="shadow-sm rounded",
                    style={
                        "marginTop": "20px",
                        "backgroundColor": "#fff",
                        "padding": "20px",
                        "borderRadius": "10px",
                        "boxShadow": "0 4px 8px rgba(0,0,0,0.1)",
                    },
                ),
            ],
            style={"flexGrow": 1, "padding": "30px", "backgroundColor": "#f8f9fa"},
        ),
    ],
    style={"display": "flex"},
)

# Callback to load and display data
@app.callback(
    Output("applications-table-container", "children"),
    Input("url", "pathname"),
)
def load_applications_table(pathname):
    if pathname != "/adoptionApplications":
        raise PreventUpdate

    # SQL Query to fetch application data
    query = """
        SELECT a.applicationID, a.interviewDate, a.interviewTime, a.approval, a.adoptedTo, 
               r.rescueName, u.firstName, u.lastName, a.userID
        FROM Application a
        JOIN Rescue r ON a.rescueID = r.rescueID
        JOIN Users u ON a.userID = u.userID
    """
    columns = [
        "APPLICATION ID", "interviewDate", "interviewTime", "approval", "adoptedTo", 
        "NAME OF RESCUE", "FIRST NAME", "LAST NAME", "USER ID"
    ]

    # Retrieve data
    applications = getDataFromDB(query, [], columns)

    # Handle empty table
    if applications.empty:
        return dbc.Alert("No adoption applications found.", color="warning", className="text-center")

    # Build rows for the table
    table_rows = []
    for _, row in applications.iterrows():
        # Handle interview status
        if row["approval"] is None:
            interview_status = html.Td(
                dbc.ButtonGroup(
                    [
                        dbc.Button("Approve", color="success", size="sm", id={"type": "approve-button", "index": row["APPLICATION ID"]}),
                        dbc.Button("Reject", color="danger", size="sm", id={"type": "reject-button", "index": row["APPLICATION ID"]}),
                    ],
                    size="sm",
                ),
                style={"textAlign": "center"},
            )
        elif row["approval"] is True:
            interview_status = html.Td("Approved", style={"color": "green", "fontWeight": "bold", "textAlign": "center"})
        else:
            interview_status = html.Td("Rejected", style={"color": "red", "fontWeight": "bold", "textAlign": "center"})

        # Handle application status
        if row["adoptedTo"] == row["USER ID"]:
            application_status = html.Td("Granted", style={"color": "green", "fontWeight": "bold", "textAlign": "center"})
        elif pd.isnull(row["adoptedTo"]):
                application_status = html.Td(
                dbc.ButtonGroup(
                    [
                        dbc.Button("Grant", color="success", size="sm", id={"type": "grant-button", "index": row["APPLICATION ID"]}),
                    ],
                    size="sm",
                ),
                style={"textAlign": "center"},
            )
        else:
            application_status = html.Td("Denied", style={"color": "red", "fontWeight": "bold", "textAlign": "center"})

        # Add row to the table
        table_rows.append(
            html.Tr(
                [
                    html.Td(row["APPLICATION ID"], style={"textAlign": "center"}),
                    html.Td(
                        dbc.Button("View", color="primary", size="sm", href=f"/viewAdoptions/fullview?id={row['APPLICATION ID']}"),
                        style={"textAlign": "center"}
                    ),
                    html.Td(row["interviewDate"], style={"textAlign": "center"}),
                    html.Td(row["NAME OF RESCUE"], style={"textAlign": "center"}),
                    html.Td(f"{row['interviewDate']} {row['interviewTime']}", style={"textAlign": "center"}),
                    interview_status,
                    application_status,
                ]
            )
        )

    # Return the populated table
    return dbc.Table(
        [
            html.Thead(
                html.Tr(
                    [
                        html.Th("APPLICATION ID"),
                        html.Th("VIEW APPLICATION"),
                        html.Th("APPLICATION DATE"),
                        html.Th("NAME OF RESCUE"),
                        html.Th("INTERVIEW SCHEDULE"),
                        html.Th("INTERVIEW STATUS"),
                        html.Th("APPLICATION STATUS"),
                    ],
                    style={"backgroundColor": "#2a9d8f", "color": "white", "textAlign": "center"},
                )
            ),
            html.Tbody(table_rows),
        ],
        bordered=True,
        hover=True,
        striped=True,
        responsive=True,
        className="text-center",
        style={"fontSize": "0.95rem", "color": "#333", "marginTop": "20px"},
    )

# Callback to handle grant and approve/reject actions
@app.callback(
    Output("applications-table-container", "children", allow_duplicate=True),
    Input({"type": "grant-button", "index": ALL}, "n_clicks"),
    Input({"type": "approve-button", "index": ALL}, "n_clicks"),
    Input({"type": "reject-button", "index": ALL}, "n_clicks"),
    State({"type": "grant-button", "index": ALL}, "id"),
    State({"type": "approve-button", "index": ALL}, "id"),
    State({"type": "reject-button", "index": ALL}, "id"),
    prevent_initial_call="both",
)
def update_application_status(grant_clicks, approve_clicks, reject_clicks, grant_ids, approve_ids, reject_ids):
    # Update adoptedTo column for Grant
    for i, n_click in enumerate(grant_clicks):
        if n_click:
            app_id = grant_ids[i]["index"]
            modifyDB(
                "UPDATE Application SET adoptedTo = userID WHERE applicationID = %s",
                [app_id]
            )
            break

    # Update approval column for Approve
    for i, n_click in enumerate(approve_clicks):
        if n_click:
            app_id = approve_ids[i]["index"]
            modifyDB(
                "UPDATE Application SET approval = TRUE WHERE applicationID = %s",
                [app_id]
            )
            break

    # Update approval column for Reject
    for i, n_click in enumerate(reject_clicks):
        if n_click:
            app_id = reject_ids[i]["index"]
            modifyDB(
                "UPDATE Application SET approval = FALSE WHERE applicationID = %s",
                [app_id]
            )
            break

    return load_applications_table("/adoptionApplications")


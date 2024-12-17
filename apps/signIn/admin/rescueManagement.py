from urllib.parse import parse_qs, urlparse

import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, dcc, html, ALL, no_update
from dash.exceptions import PreventUpdate

from app import app
from dbconnect import getDataFromDB, modifyDB

# Layout
layout = html.Div(
    [
        # Sidebar Placeholder
        html.Div(id="admin-sidebar", style={"width": "250px", "flexShrink": 0}),

        # Main Content
        html.Div(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            html.H3(
                                "Rescues Management",
                                style={"color": "#2a9d8f", "marginTop": "20px", "fontWeight": "bold"},
                            ),
                            width=8,
                        ),
                        dbc.Col(
                            dbc.Button(
                                "Add New Rescue",
                                color="success",
                                href="/rescuesManagementProfile?mode=add",
                                className="btn-sm",
                                style={"marginTop": "20px", "textAlign": "right"},
                            ),
                            width=4,
                        ),
                    ],
                    justify="between",
                ),

                # Rescues Table
                html.Div(
                    id="rescues-table-container",
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

# Callback to retrieve and display data
@app.callback(
    Output("rescues-table-container", "children"),
    Input("url", "pathname"),
    prevent_initial_call="initial_duplicate",
)
def load_rescues_table(pathname):
    if pathname != "/rescuesManagement":
        raise PreventUpdate

    # SQL query to fetch rescue data and user full name for adoptedTo
    query = """
        SELECT r.rescueID, r.rescueName, r.category, r.gender, r.age, r.breed, r.medCondition, 
               r.description, r.rescueStatus, 
               COALESCE(CONCAT(u.firstName, ' ', u.middleName, ' ', u.lastName, ' ', COALESCE(u.suffix, '')), 'Not Adopted') AS adoptedTo
        FROM Rescue r
        LEFT JOIN Users u ON r.adoptedTo = u.userID
    """
    columns = [
        "Rescue ID", "Rescue Name", "Category", "Gender", "Age", "Breed", 
        "Medical Condition", "Description", "Rescue Status", "Adopted To"
    ]

    # Retrieve data
    rescues = getDataFromDB(query, [], columns)

    # Handle empty results
    if rescues.empty:
        return dbc.Alert("No rescues found.", color="warning", className="text-center", style={"fontSize": "1.2rem"})

    # Add "Action" buttons: Edit and Delete
    rescues["Actions"] = [
        html.Div(
            [
                dbc.Button(
                    "Edit",
                    color="warning",
                    size="sm",
                    href=f"/rescuesManagementProfile?mode=edit&id={row['Rescue ID']}",
                    className="me-2",
                ),
                dbc.Button(
                    "Delete",
                    color="danger",
                    size="sm",
                    id={"type": "delete-button", "index": row["Rescue ID"]},
                ),
            ],
            className="d-flex justify-content-center",
        )
        for _, row in rescues.iterrows()
    ]

    # Drop the Rescue ID column from the display but retain it for actions
    display_df = rescues.drop(columns=["Rescue ID"])

    # Custom Table Design
    table_header = [
        html.Thead(
            html.Tr(
                [
                    html.Th(col, style={"backgroundColor": "#2a9d8f", "color": "white", "textAlign": "center"})
                    for col in display_df.columns
                ]
            )
        )
    ]

    table_body = [
        html.Tbody(
            [
                html.Tr(
                    [
                        html.Td(
                            row[col], style={"verticalAlign": "middle", "textAlign": "center"}
                        )
                        for col in display_df.columns
                    ]
                )
                for _, row in display_df.iterrows()
            ]
        )
    ]

    table = dbc.Table(
        table_header + table_body,
        bordered=True,
        hover=True,
        striped=True,
        responsive=True,
        className="text-center",
        style={"fontSize": "0.95rem", "color": "#333", "marginTop": "20px", "boxShadow": "0 2px 4px rgba(0,0,0,0.1)"},
    )

    return table


# Callback to handle delete actions
@app.callback(
    Output("rescues-table-container", "children", allow_duplicate=True),
    Input({"type": "delete-button", "index": ALL}, "n_clicks"),
    State({"type": "delete-button", "index": ALL}, "id"),
    prevent_initial_call="both",
)
def delete_rescue(n_clicks, button_ids):
    if not n_clicks or all(n is None for n in n_clicks):
        raise PreventUpdate

    for i, n_click in enumerate(n_clicks):
        if n_click:
            rescue_id = button_ids[i]["index"]

            # Perform the deletion in the database
            sql = "DELETE FROM Rescue WHERE rescueID = %s"
            modifyDB(sql, [rescue_id])
            break

    # Reload the table after deletion
    return load_rescues_table("/rescuesManagement")

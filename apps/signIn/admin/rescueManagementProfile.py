from urllib.parse import parse_qs, urlparse

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State
from dash.exceptions import PreventUpdate

from app import app
from dbconnect import getDataFromDB, modifyDB

# Layout
layout = html.Div(
    [
        # Sidebar placeholder
        html.Div(id="admin-sidebar", style={"width": "250px", "flexShrink": 0}),

        dbc.Alert(id="rescueprofile_alert", is_open=False),  # Alert for feedback messages

        dbc.Container(
            [
                # Header with Back Button
                dbc.Row(
                    [
                        dbc.Col(
                            html.H2(id="rescueprofile_title", style={"color": "#dba514", "font-weight": "bold"}), 
                            width="auto"
                        ),
                        dbc.Col(
                            dbc.Button("Back", color="primary", href="/rescuesManagement"),
                            width="auto",
                            style={"textAlign": "right"},
                        ),
                    ],
                    className="mb-3",
                ),

                # Form Fields
                dbc.Form(
                    [
                        dbc.Row(
                            [
                                # Left Column
                                dbc.Col(
                                    [
                                        dbc.Label("Rescue Name"),
                                        dbc.Input(id="input-rescue-name", type="text", placeholder="Enter Rescue Name", required=True),

                                        dbc.Label("Category"),
                                        dcc.Dropdown(
                                            id="input-category",
                                            options=[{"label": "Dog", "value": "Dog"}, {"label": "Cat", "value": "Cat"}],
                                            placeholder="Select Category",
                                        ),

                                        dbc.Label("Gender"),
                                        dcc.Dropdown(
                                            id="input-gender",
                                            options=[{"label": "Male", "value": "Male"}, {"label": "Female", "value": "Female"}],
                                            placeholder="Select Gender",
                                        ),

                                        dbc.Label("Age"),
                                        dbc.Input(id="input-age", type="number", placeholder="Enter Age (years)"),

                                        dbc.Label("Breed"),
                                        dbc.Input(id="input-breed", type="text", placeholder="Enter Breed"),
                                    ],
                                    width=6,
                                ),
                                # Right Column
                                dbc.Col(
                                    [
                                        dbc.Label("Medical Condition"),
                                        dbc.Textarea(id="input-medCon", placeholder="Describe Medical Condition", rows=2),

                                        dbc.Label("Description"),
                                        dbc.Textarea(id="input-desc", placeholder="Describe Rescue", rows=3),

                                        dbc.Label("Rescue Status"),
                                        dcc.Dropdown(
                                            id="input-status",
                                            options=[
                                                {"label": "In Care", "value": "In Care"},
                                                {"label": "Critical Condition", "value": "Critical Condition"},
                                                {"label": "Passed On", "value": "Passed On"},
                                                {"label": "Adopted", "value": "Adopted"},
                                            ],
                                            placeholder="Select Rescue Status",
                                        ),

                                        dbc.Label("Adopted To"),
                                        dcc.Dropdown(id="input-adopted-to", placeholder="Select User or Available"),

                                        dbc.Label("Image URL"),
                                        dbc.Input(id="input-image", type="url", placeholder="Enter Image URL"),
                                    ],
                                    width=6,
                                ),
                            ],
                            className="mb-4",
                        ),
                        # Submit Button
                        dbc.Button("Save", id="rescueprofile_submit", color="primary", n_clicks=0),
                    ]
                ),

                # Success Modal
                dbc.Modal(
                    [
                        dbc.ModalHeader("Success"),
                        dbc.ModalBody("Rescue details saved successfully."),
                        dbc.ModalFooter(dbc.Button("Back to List", href="/rescuesManagement", color="success")),
                    ],
                    id="rescueprofile_successmodal",
                    centered=True,
                    backdrop="static",
                    is_open=False,
                ),
            ],
            style={"padding": "30px", "backgroundColor": "#fff", "borderRadius": "10px", "boxShadow": "0 4px 8px rgba(0,0,0,0.1)"},
            className="mt-4",
        ),
    ]
)


@app.callback(
    [
        Output("rescueprofile_title", "children"),
        Output("input-rescue-name", "value"),
        Output("input-category", "value"),
        Output("input-gender", "value"),
        Output("input-age", "value"),
        Output("input-breed", "value"),
        Output("input-medCon", "value"),
        Output("input-desc", "value"),
        Output("input-status", "value"),
        Output("input-adopted-to", "options"),
        Output("input-adopted-to", "value"),
        Output("input-image", "value"),
    ],
    Input("url", "search"),
)
def load_rescue_details(query_string):
    parsed_query = parse_qs(urlparse(query_string).query)
    mode = parsed_query.get("mode", ["add"])[0]
    rescue_id = parsed_query.get("id", [None])[0]

    # Fetch Users for 'Adopted To' dropdown
    user_query = "SELECT userID, CONCAT(firstName, ' ', lastName) AS fullName FROM Users"
    users_df = getDataFromDB(user_query, [], ["userID", "fullName"])
    user_options = [{"label": row["fullName"], "value": str(row["userID"])} for _, row in users_df.iterrows()]
    user_options.insert(0, {"label": "Available", "value": "Available"})

    if mode == "edit" and rescue_id:
        sql = """
            SELECT rescueName, category, gender, age, breed, medCondition, description, rescueStatus, adoptedTo, rescuePic
            FROM Rescue WHERE rescueID = %s
        """
        result = getDataFromDB(sql, [rescue_id], ["rescueName", "category", "gender", "age", "breed", "medCondition", 
                                                 "description", "rescueStatus", "adoptedTo", "rescuePic"])
        if not result.empty:
            rescue = result.iloc[0]
            return (
                "Edit Rescue",
                rescue["rescueName"],
                rescue["category"],
                rescue["gender"],
                rescue["age"],
                rescue["breed"],
                rescue["medCondition"],
                rescue["description"],
                rescue["rescueStatus"],
                user_options,
                str(rescue["adoptedTo"]) if rescue["adoptedTo"] else "Available",
                rescue["rescuePic"],
            )
    return ("Add a Rescue", None, None, None, None, None, None, None, None, user_options, "Available", None)


@app.callback(
    [Output("rescueprofile_alert", "is_open"), Output("rescueprofile_successmodal", "is_open")],
    Input("rescueprofile_submit", "n_clicks"),
    [
        State("input-rescue-name", "value"),
        State("input-category", "value"),
        State("input-gender", "value"),
        State("input-age", "value"),
        State("input-breed", "value"),
        State("input-medCon", "value"),
        State("input-desc", "value"),
        State("input-status", "value"),
        State("input-adopted-to", "value"),
        State("input-image", "value"),
        State("url", "search"),
    ],
)
def save_rescue_details(n_clicks, name, category, gender, age, breed, medCon, desc, status, adopted_to, image, query_string):
    if not n_clicks:
        raise PreventUpdate

    if not all([name, category, gender, age, breed, status]):
        return True, False

    adopted_to = None if adopted_to == "Available" else int(adopted_to)

    parsed_query = parse_qs(urlparse(query_string).query)
    mode = parsed_query.get("mode", ["add"])[0]
    rescue_id = parsed_query.get("id", [None])[0]

    try:
        if mode == "edit" and rescue_id:
            sql = """
                UPDATE Rescue SET rescueName=%s, category=%s, gender=%s, age=%s, breed=%s, medCondition=%s,
                                 description=%s, rescueStatus=%s, adoptedTo=%s, rescuePic=%s
                WHERE rescueID=%s
            """
            values = [name, category, gender, age, breed, medCon, desc, status, adopted_to, image, rescue_id]
        else:
            sql = """
                INSERT INTO Rescue (rescueName, category, gender, age, breed, medCondition, description, rescueStatus, adoptedTo, rescuePic)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            values = [name, category, gender, age, breed, medCon, desc, status, adopted_to, image]

        modifyDB(sql, values)
        return False, True
    except Exception as e:
        print("Error:", e)
        return True, False

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State
from dash.exceptions import PreventUpdate
from app import app
from dbconnect import modifyDB

# Layout for the dwelling information form
layout = html.Div(
    [
        # Sidebar
        html.Div(id="customer-sidebar", style={"width": "250px", "flexShrink": 0}),

        # Main Container
        dbc.Container(
            [
                html.H2("UPDATE ACCOUNT", style={"color": "#dba514", "fontWeight": "bold", "textAlign": "center"}),
                html.Hr(),
                html.H4("Dwelling Information", style={"fontWeight": "bold", "textAlign": "center"}),

                # Type of Dwelling Text Field
                dbc.Row(
                    [
                        dbc.Label("Type of Dwelling*", width=3),
                        dbc.Col(
                            dbc.Input(id="dwelling-type-input", placeholder="Enter Type of Dwelling"),
                            width=7,
                        ),
                    ],
                    className="mb-3",
                ),

                # Dwelling Owned Dropdown (Yes/No)
                dbc.Row(
                    [
                        dbc.Label("Dwelling Owned?*", width=3),
                        dbc.Col(
                            dcc.Dropdown(
                                id="ownership-dropdown",
                                options=[
                                    {"label": "Yes", "value": "Yes"},
                                    {"label": "No", "value": "No"},
                                ],
                                placeholder="Select Yes or No",
                            ),
                            width=7,
                        ),
                    ],
                    className="mb-3",
                ),

                # Pets Allowed Dropdown (Yes/No)
                dbc.Row(
                    [
                        dbc.Label("Are Pets Allowed?*", width=3),
                        dbc.Col(
                            dcc.Dropdown(
                                id="pets-allowed-dropdown",
                                options=[
                                    {"label": "Yes", "value": "Yes"},
                                    {"label": "No", "value": "No"},
                                ],
                                placeholder="Select Yes or No",
                            ),
                            width=7,
                        ),
                    ],
                    className="mb-3",
                ),

                # Navigation Buttons Row 1
                html.Div(
                    [
                        dbc.Button("Personal", href="/accountProfile/edit/personal", color="info", className="me-2"),
                        dbc.Button("Dwelling", color="secondary", disabled=True, className="me-2"),
                        dbc.Button("Password", href="/accountProfile/edit/password", color="info", className="me-2"),
                    ],
                    className="d-flex justify-content-center mb-2",
                ),

                # Action Buttons Row 2
                html.Div(
                    [
                        dbc.Button("Done", href="/accountProfile", color="success", className="me-2"),
                        dbc.Button("Update", id="update-button", color="primary"),
                    ],
                    className="d-flex justify-content-center",
                ),

                # Feedback Message
                html.Div(id="dwelling-update-message", className="mt-3", style={"textAlign": "center"}),

                # Hidden Modal for Logout Prompt
                dbc.Modal(
                    [
                        dbc.ModalHeader("Update Complete"),
                        dbc.ModalBody("To apply changes, you must log out."),
                        dbc.ModalFooter(
                            dbc.Button("Log Out", href="/logout", color="danger", id="logout-button")
                        ),
                    ],
                    id="dwelling-logout-modal",
                    centered=True,
                    is_open=False,  # Initially hidden
                ),
            ],
            className="customer-admin-menu",
        )
    ]
)

# Callback: Pre-populate form fields from user session
@app.callback(
    [
        Output("dwelling-type-input", "value"),
        Output("ownership-dropdown", "value"),
        Output("pets-allowed-dropdown", "value"),
    ],
    Input("user-session", "data"),
)
def populate_dwelling_form(user_session):
    """
    Pre-fills the dwelling form using user session data.
    """
    if not user_session:
        raise PreventUpdate

    return (
        user_session.get("dwellingType", ""),
        user_session.get("dwellingOwn", ""),
        user_session.get("petsAllowed", ""),
    )

# Callback: Update dwelling information in the database and open modal
@app.callback(
    [Output("dwelling-update-message", "children"), Output("dwelling-logout-modal", "is_open")],
    Input("update-button", "n_clicks"),
    [
        State("dwelling-type-input", "value"),
        State("ownership-dropdown", "value"),
        State("pets-allowed-dropdown", "value"),
        State("user-session", "data"),
    ],
    prevent_initial_call=True,
)
def update_dwelling_info(n_clicks, dwelling_type, ownership, pets_allowed, user_session):
    """
    Updates dwelling information in the database when 'Update' is clicked and shows a logout modal.
    """
    if not user_session:
        raise PreventUpdate

    user_id = user_session.get("userID")

    sql = """
        UPDATE Users 
        SET dwellingType=%s, dwellingOwn=%s, petsAllowed=%s 
        WHERE userID=%s
    """
    values = (dwelling_type, ownership, pets_allowed, user_id)

    try:
        modifyDB(sql, values)
        return dbc.Alert("Dwelling Information updated successfully!", color="success"), True
    except Exception as e:
        return dbc.Alert(f"Error updating dwelling information: {str(e)}", color="danger"), False

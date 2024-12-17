import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State
from dash.exceptions import PreventUpdate

from app import app
from dbconnect import getDataFromDB, modifyDB

layout = html.Div(
    [
        # Sidebar
        html.Div(id="customer-sidebar", style={"width": "250px", "flexShrink": 0}),

        # Main Container
        dbc.Container(
            [
                # Header
                html.H2("UPDATE ACCOUNT", style={"color": "#dba514", "fontWeight": "bold", "textAlign": "center"}),
                html.Hr(),
                html.H4("Change Your Password", style={"fontWeight": "bold", "textAlign": "center"}),

                # Current Password Input
                dbc.Row(
                    [
                        dbc.Label("Current Password*", html_for="current-password", width=4),
                        dbc.Col(
                            dbc.Input(type="password", id="current-password", placeholder="Enter Current Password", required=True),
                            width=8,
                        ),
                    ],
                    className="mb-3",
                ),

                # New Password Input
                dbc.Row(
                    [
                        dbc.Label("New Password*", html_for="new-password", width=4),
                        dbc.Col(
                            dbc.Input(type="password", id="new-password", placeholder="Enter New Password", required=True),
                            width=8,
                        ),
                    ],
                    className="mb-3",
                ),

                # Confirm Password Input
                dbc.Row(
                    [
                        dbc.Label("Confirm New Password*", html_for="confirm-password", width=4),
                        dbc.Col(
                            dbc.Input(type="password", id="confirm-password", placeholder="Re-enter New Password", required=True),
                            width=8,
                        ),
                    ],
                    className="mb-3",
                ),

                # Navigation Buttons Row 1
                html.Div(
                    [
                        dbc.Button("Personal", href="/accountProfile/edit/personal", color="info", className="me-2"),
                        dbc.Button("Dwelling", href="/accountProfile/edit/dwelling", color="info", className="me-2"),
                        dbc.Button("Password", color="secondary", disabled=True, className="me-2"),
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
                html.Div(id="password-update-message", className="mt-3", style={"textAlign": "center"}),

                # Hidden Modal for Logout Prompt
                dbc.Modal(
                    [
                        dbc.ModalHeader("Update Complete"),
                        dbc.ModalBody("To apply changes, you must log out."),
                        dbc.ModalFooter(
                            dbc.Button("Log Out", href="/logout", color="danger", id="logout-button")
                        ),
                    ],
                    id="password-logout-modal",
                    centered=True,
                    is_open=False,  # Initially hidden
                ),
            ],
            className="customer-admin-menu",
        ),
    ]
)

# Callback: Validate and update password, open modal on success
@app.callback(
    [Output("password-update-message", "children"), Output("password-logout-modal", "is_open")],
    Input("update-button", "n_clicks"),
    [
        State("current-password", "value"),
        State("new-password", "value"),
        State("confirm-password", "value"),
        State("user-session", "data"),
    ],
    prevent_initial_call=True,
)
def update_password(n_clicks, current_password, new_password, confirm_password, user_session):
    """
    Validates the current password, ensures new passwords match, and updates the password in the database.
    Displays a modal prompting logout upon success.
    """
    if not user_session:
        raise PreventUpdate

    user_id = user_session.get("userID")

    # Step 1: Input validation
    if not current_password or not new_password or not confirm_password:
        return dbc.Alert("All fields are required.", color="warning"), False

    if new_password != confirm_password:
        return dbc.Alert("New passwords do not match.", color="danger"), False

    # Step 2: Check current password in database
    sql_validate = "SELECT password FROM Users WHERE userID = %s"
    try:
        result = getDataFromDB(sql_validate, [user_id], ["password"])
        if result.empty:
            return dbc.Alert("User not found.", color="danger"), False

        db_password = result['password'].iloc[0]
        if db_password != current_password:
            return dbc.Alert("Current password is incorrect.", color="danger"), False
    except Exception as e:
        return dbc.Alert(f"An error occurred: {str(e)}", color="danger"), False

    # Step 3: Update the password
    sql_update = "UPDATE Users SET password = %s WHERE userID = %s"
    try:
        modifyDB(sql_update, (new_password, user_id))
        return dbc.Alert("Password updated successfully!", color="success"), True
    except Exception as e:
        return dbc.Alert(f"Failed to update password: {str(e)}", color="danger"), False

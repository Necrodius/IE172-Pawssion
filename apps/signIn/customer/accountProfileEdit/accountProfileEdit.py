import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State
from dash.exceptions import PreventUpdate
from app import app
from dbconnect import modifyDB

# Layout
layout = html.Div(
    [
        # Sidebar
        html.Div(id="customer-sidebar", style={"width": "250px", "flexShrink": 0}),

        # Main Container
        dbc.Container(
            [
                html.H2("UPDATE ACCOUNT", style={"color": "#dba514", "fontWeight": "bold", "textAlign": "center"}),
                html.Hr(),
                html.H4("Personal Information", style={"fontWeight": "bold", "textAlign": "center"}),

                # Form Fields
                dbc.Form(
                    [
                        dbc.Row(
                            [
                                dbc.Col(dbc.Label("Last Name*", html_for="input-last-name"), width=3),
                                dbc.Col(dbc.Input(id="input-last-name", placeholder="Enter Last Name"), width=7),
                            ],
                            className="mb-2",
                        ),
                        dbc.Row(
                            [
                                dbc.Col(dbc.Label("First Name*", html_for="input-first-name"), width=3),
                                dbc.Col(dbc.Input(id="input-first-name", placeholder="Enter First Name"), width=7),
                            ],
                            className="mb-2",
                        ),
                        dbc.Row(
                            [
                                dbc.Col(dbc.Label("Middle Name*", html_for="input-middle-name"), width=3),
                                dbc.Col(dbc.Input(id="input-middle-name", placeholder="Enter Middle Name"), width=7),
                            ],
                            className="mb-2",
                        ),
                        dbc.Row(
                            [
                                dbc.Col(dbc.Label("Suffix", html_for="input-suffix"), width=3),
                                dbc.Col(dbc.Input(id="input-suffix", placeholder="e.g., Jr., III"), width=7),
                            ],
                            className="mb-2",
                        ),
                        dbc.Row(
                            [
                                dbc.Col(dbc.Label("Street Address*", html_for="input-street"), width=3),
                                dbc.Col(dbc.Input(id="input-street", placeholder="Enter Street Address"), width=7),
                            ],
                            className="mb-2",
                        ),
                        dbc.Row(
                            [
                                dbc.Col(dbc.Label("City*", html_for="input-city"), width=3),
                                dbc.Col(dbc.Input(id="input-city", placeholder="Enter City"), width=7),
                            ],
                            className="mb-2",
                        ),
                        dbc.Row(
                            [
                                dbc.Col(dbc.Label("Province*", html_for="input-province"), width=3),
                                dbc.Col(dbc.Input(id="input-province", placeholder="Enter Province"), width=7),
                            ],
                            className="mb-2",
                        ),
                        dbc.Row(
                            [
                                dbc.Col(dbc.Label("Email*", html_for="input-email"), width=3),
                                dbc.Col(dbc.Input(id="input-email", type="email", placeholder="Enter Email"), width=7),
                            ],
                            className="mb-2",
                        ),
                        dbc.Row(
                            [
                                dbc.Col(dbc.Label("Contact No.*", html_for="input-contact"), width=3),
                                dbc.Col(dbc.Input(id="input-contact", placeholder="Enter Contact Number"), width=7),
                            ],
                            className="mb-4",
                        ),
                    ]
                ),

                # Navigation Buttons Row 1
                html.Div(
                    [
                        dbc.Button("Personal", color="secondary", disabled=True, className="me-2"),
                        dbc.Button("Dwelling", href="/accountProfile/edit/dwelling", color="info", className="me-2"),
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
                html.Div(id="personal-update-message", className="mt-3", style={"textAlign": "center"}),

                # Hidden Modal for Logout Prompt
                dbc.Modal(
                    [
                        dbc.ModalHeader("Update Complete"),
                        dbc.ModalBody("To apply changes, you must log out."),
                        dbc.ModalFooter(
                            dbc.Button("Log Out", href="/logout", color="danger", id="logout-button")
                        ),
                    ],
                    id="personal-logout-modal",
                    centered=True,
                    is_open=False,  # Initially hidden
                ),
            ],
            className="customer-admin-menu",
        )
    ]
)


# Callback: Populate form with user session data
@app.callback(
    [
        Output("input-last-name", "value"),
        Output("input-first-name", "value"),
        Output("input-middle-name", "value"),
        Output("input-suffix", "value"),
        Output("input-street", "value"),
        Output("input-city", "value"),
        Output("input-province", "value"),
        Output("input-email", "value"),
        Output("input-contact", "value"),
    ],
    Input("user-session", "data"),
)
def populate_form(user_session):
    """
    Pre-fills the form with user data from session.
    """
    if not user_session:
        raise PreventUpdate

    return (
        user_session.get("lastName", ""),
        user_session.get("firstName", ""),
        user_session.get("middleName", ""),
        user_session.get("suffix", ""),
        user_session.get("street", ""),
        user_session.get("city", ""),
        user_session.get("province", ""),
        user_session.get("emailAddress", ""),
        user_session.get("contactNo", ""),
    )


# Callback: Update personal information in the database and open modal
@app.callback(
    [Output("personal-update-message", "children"), Output("personal-logout-modal", "is_open")],
    Input("update-button", "n_clicks"),
    [
        State("input-last-name", "value"),
        State("input-first-name", "value"),
        State("input-middle-name", "value"),
        State("input-suffix", "value"),
        State("input-street", "value"),
        State("input-city", "value"),
        State("input-province", "value"),
        State("input-email", "value"),
        State("input-contact", "value"),
        State("user-session", "data"),
    ],
    prevent_initial_call=True,
)
def update_personal_info(n_clicks, last_name, first_name, middle_name, suffix, street, city, province, email, contact, user_session):
    """
    Updates personal information in the database and shows a logout modal.
    """
    if not user_session:
        raise PreventUpdate

    user_id = user_session.get("userID")
    sql = """
        UPDATE Users 
        SET lastName=%s, firstName=%s, middleName=%s, suffix=%s, street=%s, city=%s, province=%s, emailAddress=%s, contactNo=%s 
        WHERE userID=%s
    """
    values = (last_name, first_name, middle_name, suffix, street, city, province, email, contact, user_id)

    try:
        modifyDB(sql, values)
        return dbc.Alert("Personal Information updated successfully!", color="success"), True
    except Exception as e:
        return dbc.Alert(f"Error updating personal information: {str(e)}", color="danger"), False

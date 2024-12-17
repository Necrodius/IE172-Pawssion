import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State
from dash.exceptions import PreventUpdate
from dbconnect import getDataFromDB  # or modifyDB if needed
from app import app

# Layout
layout = html.Div(
    [
        dcc.Location(id='signin-redirect', refresh=True),  # For redirecting

        # Sign-in Section
        html.Div(
            [
                # Title and Subtitle
                html.H1(
                    "Welcome Back!",
                    style={
                        "textAlign": "center",
                        "color": "#2a9d8f",
                        "fontWeight": "bold",
                        "fontSize": "3rem",
                        "marginBottom": "10px",
                    },
                ),
                html.P(
                    "Sign in to continue to your account",
                    style={"textAlign": "center", "color": "#555", "fontSize": "1.2rem"},
                ),

                # Input Form
                html.Div(
                    [
                        # Email Input
                        dbc.Label("Email", html_for="signin-email"),
                        dbc.Input(
                            type="email",
                            id="signin-email",
                            placeholder="Enter your email",
                            required=True,
                            className="mb-3",
                        ),

                        # Password Input
                        dbc.Label("Password", html_for="signin-password"),
                        dbc.Input(
                            type="password",
                            id="signin-password",
                            placeholder="Enter your password",
                            required=True,
                            className="mb-3",
                        ),

                        # Sign-In Button
                        html.Div(
                            dbc.Button(
                                "Sign In",
                                id="signin-button",
                                color="success",
                                className="btn-block",
                                style={
                                    "fontWeight": "bold",
                                    "fontSize": "1rem",
                                    "padding": "10px 20px",
                                },
                            ),
                            className="text-center mt-3",
                        ),

                        # "Sign Up" Section beside "Don't have an account?"
                        html.Div(
                            [
                                html.Span(
                                    "Don't have an account? ",
                                    style={
                                        "fontSize": "1rem",
                                        "color": "#555",
                                        "marginRight": "5px",
                                    },
                                ),
                                html.A(
                                    "Sign Up",
                                    href="/register",
                                    style={
                                        "color": "#007bff",
                                        "fontSize": "1rem",
                                        "fontWeight": "bold",
                                        "textDecoration": "none",
                                    },
                                ),
                            ],
                            style={
                                "textAlign": "center",
                                "marginTop": "20px",
                                "display": "flex",
                                "justifyContent": "center",
                                "alignItems": "center",
                            },
                        ),
                    ],
                    className="form-container",
                    style={
                        "maxWidth": "400px",
                        "margin": "auto",
                        "padding": "20px",
                        "backgroundColor": "#fff",
                        "borderRadius": "10px",
                        "boxShadow": "0 4px 8px rgba(0,0,0,0.1)",
                    },
                ),

                # Feedback Message
                html.Div(
                    id="signin-message",
                    style={"marginTop": "20px", "textAlign": "center"},
                ),
            ]
        ),
    ],
    style={
        "paddingTop": "100px",
        "paddingBottom": "100px",
        "paddingLeft": "20px",
        "paddingRight": "20px",
        "backgroundColor": "#FAF3EB",
    },
)

# Callback
@app.callback(
    [
        Output("signin-message", "children"),
        Output("user-session", "data"),
        Output("signin-redirect", "href"),  # Redirect after successful login
    ],
    [Input("signin-button", "n_clicks"), Input("signin-password", "n_submit")],  # Handle Enter key press
    [State("signin-email", "value"), State("signin-password", "value")],
    prevent_initial_call=True,
)
def signin_user(n_clicks, n_submit, email, password):
    if not n_clicks and not n_submit:
        raise PreventUpdate

    if not email or not password:
        return [
            dbc.Alert(
                "Please enter both email and password.",
                color="warning",
                dismissable=True,
                style={"textAlign": "center", "fontSize": "1rem"},
            ),
            dash.no_update,
            dash.no_update,
        ]

    # Query DB for matching user
    sql = "SELECT userID, password, accountType, firstName, lastName, emailAddress FROM Users WHERE emailAddress = %s"
    df_user = getDataFromDB(
        sql,
        [email],
        ["userID", "password", "accountType", "firstName", "lastName", "emailAddress"],
    )

    if df_user.empty:
        return [
            dbc.Alert(
                "Invalid email or password.",
                color="danger",
                dismissable=True,
                style={"textAlign": "center", "fontSize": "1rem"},
            ),
            dash.no_update,
            dash.no_update,
        ]

    stored_password = df_user["password"].iloc[0]
    if stored_password == password:
        # Successful login
        session_data = {
            "userID": df_user["userID"].iloc[0],
            "firstName": df_user["firstName"].iloc[0],
            "lastName": df_user["lastName"].iloc[0],
            "emailAddress": df_user["emailAddress"].iloc[0],
            "accountType": df_user["accountType"].iloc[0],
        }

        return [
            dbc.Alert(
                "Login successful!",
                color="success",
                dismissable=True,
                style={"textAlign": "center", "fontSize": "1rem"},
            ),
            session_data,
            "/",
        ]

    return [
        dbc.Alert(
            "Invalid email or password.",
            color="danger",
            dismissable=True,
            style={"textAlign": "center", "fontSize": "1rem"},
        ),
        dash.no_update,
        dash.no_update,
    ]

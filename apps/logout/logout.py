import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State
from dash.exceptions import PreventUpdate
from dbconnect import getDataFromDB  # or modifyDB if needed
from app import app

# Layout for the logout page
layout = html.Div(
    [
        dcc.Location(id='logout-redirect', refresh=True),  # For handling redirection
        html.Div(
            [
                html.H3("Are you sure you want to log out?", style={"textAlign": "center", "marginTop": "50px"}),

                # Buttons for Cancel and Log Out
                html.Div(
                    [
                        dbc.Button("Cancel", id="logout-cancel", color="secondary", href="/", style={"marginRight": "10px"}),
                        dbc.Button("Log Out", id="logout-confirm", color="danger"),
                    ],
                    style={"textAlign": "center", "marginTop": "20px"}
                ),
                # Loading spinner for logout confirmation
                dcc.Loading(
                    id="loading-logout",
                    type="default",
                    children=html.Div(id="logout-message", style={"textAlign": "center", "marginTop": "20px"})
                )
            ]
        )
    ],
    style={
        "paddingTop": "50px",
        "paddingBottom": "50px",
        "paddingLeft": "20px",
        "paddingRight": "20px",
        "backgroundColor": "#FAF3EB",
        "height": "100vh",
        "display": "flex",
        "justifyContent": "center",
        "alignItems": "center"
    }
)

# Callback to handle the Log Out button
@app.callback(
    [Output("user-session", "data", allow_duplicate=True),
    Output("logout-redirect", "href")],  # Redirect user after logging out
    Input("logout-confirm", "n_clicks"),
    prevent_initial_call=True
)
def handle_logout(n_clicks):
    """
    Clears session data and redirects the user to the home page after logout confirmation.
    """
    if n_clicks:
        return [None, "/"]  # Redirect to the home page
    return dash.no_update
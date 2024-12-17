import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State, ctx
from app import app
from dbconnect import getDataFromDB  # Your database connection module
from dash.exceptions import PreventUpdate

# Layout
layout = html.Div(
    [
        # Separate hidden locations for adopt
        dcc.Location(id='adopt-loc-dog', refresh=True),

        # Header Section
        dbc.Row(
            [
                dbc.Col(
                    html.H1("Meet the DOGS!!!", style={'color': '#2a9d8f'}),  # Header aligned to the left
                    width=8,
                ),
                dbc.Col(
                    dcc.Input(
                        id="search-input",
                        placeholder="Search for a dog...",
                        type="text",
                        className="search-bar",
                        style={'width': '100%'}
                    ),
                    width=4,
                    style={'textAlign': 'right'}
                )
            ],
            className="mb-4"
        ),

        # Dog Cards Section
        dbc.Row(
            id="dog-cards-container",  # Cards will be dynamically generated here
            justify="center",
        ),

        # Modal for Adoption Notice
        dbc.Modal(
            [
                dbc.ModalHeader("Adoption Notice"),
                dbc.ModalBody(
                    "To proceed with the adoption process, please sign in or register."
                ),
                dbc.ModalFooter(
                    [
                        dbc.Button("Cancel", id="adopt-cancel-modal-dog", color="secondary"),
                        dbc.Button("Sign In", href="/signin", color="primary"),
                        dbc.Button("Register", href="/register", color="success"),
                    ]
                ),
            ],
            id="adopt-modal-dogs",
            centered=True,
            is_open=False,
        ),

    ],
    style={
        "paddingTop": "100px",
        "paddingLeft": "50px",
        "paddingRight": "50px",
        "paddingBottom": "100px",
        "backgroundColor": "#FAF3EB"
    }
)

# Callback to fetch dogs on page load and generate cards
@app.callback(
    Output("dog-cards-container", "children"),  # Output expects a single list of children components
    Input("url", "pathname"),
)
def fetch_dogs_data(pathname):
    """
    Fetches all dog records from the Rescue table and dynamically generates cards for each.
    """
    if pathname != "/meettherescues/dogs":
        raise PreventUpdate

    # Query to fetch only dogs from the database
    query = "SELECT rescueID, rescueName, description, rescuePic, gender, age, breed, medCondition FROM Rescue WHERE category = %s"
    values = ('Dog',)
    dfcolumns = ['rescueID', 'rescueName', 'description', 'rescuePic', 'gender', 'age', 'breed', 'medCondition']

    try:
        dogs_data = getDataFromDB(query, values, dfcolumns)  # Fetch data from the database
    except Exception as e:
        return html.P("Error fetching dogs: {}".format(str(e)), style={"textAlign": "center"})

    # If no data is found
    if dogs_data.empty:
        return html.P("No dogs available at the moment.", style={"textAlign": "center"})

    # Generate and return cards directly with full details
    return [
        dbc.Col(
            dbc.Card(
                dbc.CardBody([
                    # Dog Image
                    html.Img(
                        src=dog["rescuePic"],
                        className="dog-image",
                        style={"width": "100%", "height": "250px", "objectFit": "cover", "borderRadius": "8px"}
                    ),
                    # Dog Name
                    html.H5(dog["rescueName"], className="dog-name", style={'textAlign': 'center', 'marginTop': '10px'}),

                    # Full Dog Details
                    html.Div([
                        html.P(f"Gender: {dog['gender']}", style={"fontSize": "14px", "margin": "5px 0"}),
                        html.P(f"Age: {dog['age']} years", style={"fontSize": "14px", "margin": "5px 0"}),
                        html.P(f"Breed: {dog['breed']}", style={"fontSize": "14px", "margin": "5px 0"}),
                        html.P(f"Medical Condition: {dog['medCondition'] or 'None'}", style={"fontSize": "14px", "margin": "5px 0"}),
                        html.P(f"Description: {dog['description']}", style={"fontSize": "14px", "margin": "5px 0"}),
                    ], style={"textAlign": "left"}),

                    # Buttons: Adopt
                    html.Div(
                        dbc.Button(
                            "Adopt",
                            id={"type": "adopt-button", "index": dog["rescueID"]},  # Use dynamic ID
                            color="success",
                            size="sm",
                            n_clicks=0  # Explicitly initialize n_clicks
                        ),
                        style={"textAlign": "center", "marginTop": "10px"}
                    )
                ]),
            ),
            width=3, className="mb-4"
        )
        for dog in dogs_data.to_dict("records")
    ]

# Callback to handle the adopt modal opening
@app.callback(
    [Output("adopt-modal-dogs", "is_open"), Output("adopt-loc-dog", "href")],
    [Input({"type": "adopt-button", "index": dash.ALL}, "n_clicks"),
    Input("adopt-cancel-modal-dog", "n_clicks")],
    [State("user-session", "data"), State("adopt-modal-dogs", "is_open")],
    prevent_initial_call=True
)
def toggle_adopt_modal(adopt_clicks, cancel_click, user_session, is_open):
    """
    Opens the modal when any 'Adopt' button is clicked, and closes it when 'Cancel' is clicked.
    Redirects if the user is logged in.
    """
    triggered_id = ctx.triggered_id

    # Prevent modal opening on page load
    if not any(adopt_clicks) and cancel_click is None:
        raise PreventUpdate

    # If user is logged in => redirect to /adopt
    if user_session:
        return [False, "/adopt"]
    else:
        # Open modal when an "Adopt" button is clicked
        if triggered_id and "adopt-button" in str(triggered_id):
            return [True, dash.no_update]

        # Close modal when "Cancel" button is clicked
        elif triggered_id == "adopt-cancel-modal-dog":
            return [False, dash.no_update]
        
    raise PreventUpdate



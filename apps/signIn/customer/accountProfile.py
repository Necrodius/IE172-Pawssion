import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State
from app import app
from apps.navbars import customerSideNavbar as cSN

# Function to generate a styled dbc.Table
def create_table(data_dict):
    return dbc.Table(
        [
            html.Tbody(
                [
                    html.Tr([
                        html.Th(key, style={"width": "40%", "verticalAlign": "middle", "color": "#2a9d8f"}),
                        html.Td(value, style={"verticalAlign": "middle"})
                    ])
                    for key, value in data_dict.items()
                ]
            )
        ],
        bordered=False,
        hover=False,
        responsive=True,
        striped=False,
        style={"fontSize": "0.95rem", "color": "#333", "marginBottom": "0"},
        className="table-sm"
    )

# Layout
layout = dbc.Container(
    fluid=True,
    children=[
        # Header Row
        dbc.Row(
            dbc.Col(
                html.Div(
                    [
                        html.H2("Account Information", className="text-center mb-3", style={"fontWeight": "bold", "color": "#2a9d8f"}),
                        html.Hr(style={"borderTop": "2px solid #ddd", "marginBottom": "20px"}),
                    ],
                )
            )
        ),

        # Main Content
        dbc.Row(
            [
                # Personal Information and Address Information
                dbc.Col(
                    [
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H4("Personal Information", className="text-secondary mb-3", style={"fontWeight": "bold"}),
                                    html.Div(id="personal-info-table"),
                                    html.H4("Address Information", className="text-secondary mb-3 mt-4", style={"fontWeight": "bold"}),
                                    html.Div(id="address-info-table"),
                                ]
                            ),
                            className="shadow-sm mb-4",
                            style={"borderRadius": "10px", "backgroundColor": "#ffffff"},
                        ),
                    ],
                    width=6,
                ),

                # Contact Information and Dwelling Information
                dbc.Col(
                    [
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H4("Contact Information", className="text-secondary mb-3", style={"fontWeight": "bold"}),
                                    html.Div(id="contact-info-table"),
                                    html.H4("Dwelling Information", className="text-secondary mb-3 mt-4", style={"fontWeight": "bold"}),
                                    html.Div(id="dwelling-info-table"),
                                ]
                            ),
                            className="shadow-sm mb-4",
                            style={"borderRadius": "10px", "backgroundColor": "#ffffff"},
                        ),
                    ],
                    width=6,
                ),
            ],
            className="g-4",  # Adds spacing between columns
        ),

        # Bottom Section for Additional Information
        dbc.Row(
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H4("Other Information", className="text-secondary mb-3", style={"fontWeight": "bold"}),
                            html.Div(id="birth-income-table"),
                        ]
                    ),
                    className="shadow-sm mb-4",
                    style={"borderRadius": "10px", "backgroundColor": "#ffffff"},
                ),
                width=12,
            )
        ),

        # Edit Button at Bottom Center
        dbc.Row(
            dbc.Col(
                dbc.Button(
                    "Edit Account", color="primary", href="/accountProfile/edit/personal", className="px-4"
                ),
                className="text-center",
            )
        ),
    ],
    style={"padding": "30px", "backgroundColor": "#FAF3EB"},
)

# Callback to dynamically update the tables
@app.callback(
    [
        Output("personal-info-table", "children"),
        Output("address-info-table", "children"),
        Output("contact-info-table", "children"),
        Output("birth-income-table", "children"),
        Output("dwelling-info-table", "children"),
    ],
    Input("user-session", "data")
)
def update_user_profile(user_session):
    """
    Updates the account profile page dynamically using user-session data.
    """
    if not user_session:
        # If no session, return placeholders or empty data
        return (
            create_table({"Error": "You are not logged in."}),
            create_table({"Address": "No data available."}),
            create_table({"Contact Info": "No data available."}),
            create_table({"Other Info": "No data available."}),
            create_table({"Dwelling Info": "No data available."}),
        )

    # Extract user information from session data
    personal_info = {
        "Last Name": user_session.get("lastName", "N/A"),
        "First Name": user_session.get("firstName", "N/A"),
        "Middle Name": user_session.get("middleName", "N/A"),
        "Suffix": user_session.get("suffix", "N/A"),
    }

    address_info = {
        "Street Address": user_session.get("street", "N/A"),
        "City/Municipality": user_session.get("city", "N/A"),
        "Province": user_session.get("province", "N/A"),
    }

    contact_info = {
        "Contact Number": user_session.get("contactNo", "N/A"),
        "Email Address": user_session.get("emailAddress", "N/A"),
        "Facebook Link": user_session.get("facebookLink", "N/A"),
        "Instagram Link": user_session.get("instagramLink", "N/A"),
    }

    birth_income_info = {
        "Date of Birth": user_session.get("birthDate", "N/A"),
        "Source of Income": user_session.get("incomeSource", "N/A"),
    }

    dwelling_info = {
        "Type of Dwelling": user_session.get("dwellingType", "N/A"),
        "Dwelling Ownership": "Self-Owned" if user_session.get("dwellingOwn") else "Rented",
        "Are Pets Allowed": "Yes" if user_session.get("petsAllowed") else "No",
    }

    return (
        create_table(personal_info),
        create_table(address_info),
        create_table(contact_info),
        create_table(birth_income_info),
        create_table(dwelling_info),
    )

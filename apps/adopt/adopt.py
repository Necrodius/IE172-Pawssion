import dash
import dash_bootstrap_components as dbc
from dash import html

from app import app

layout = html.Div(
    [
        # Back Navigation Link
        dbc.Row(
            dbc.Col(
                html.A(
                    "← BACK",
                    href="/home",
                    className="text-muted back-link",
                    style={"textDecoration": "none", "fontWeight": "bold", "fontSize": "16px"},
                ),
                width="auto",
            ),
            className="mb-3 mt-2 ps-3",
        ),

        # Title Section
        dbc.Row(
            dbc.Col(
                html.H1(
                    "ADOPTION APPLICATION",
                    className="text-center",
                    style={
                        "color": "#f4a261",
                        "fontWeight": "bold",
                        "marginBottom": "20px",
                    },
                )
            ),
            className="mb-3",
        ),

        # Introductory Card
        dbc.Row(
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.P(
                                "Hi Hooman! Thank you for your interest in giving a furever home to one of our rescues. "
                                "We have a lot of rescue dogs and cats ready for adoption both at the BULACAN SHELTER "
                                "and the BACOLOD SHELTER. Our adoption process is super easy!",
                                className="text-center lead",
                                style={"color": "#444", "marginBottom": "15px"},
                            )
                        ]
                    ),
                    style={
                        "backgroundColor": "#fff3e0",
                        "borderRadius": "10px",
                        "boxShadow": "0 4px 8px rgba(0,0,0,0.1)",
                    },
                ),
                width=10,
                className="mx-auto mb-4",
            ),
        ),

        # Adoption Process Section
        dbc.Row(
            dbc.Col(
                [
                    html.H3("Adoption Process:", className="text-center mb-3", style={"color": "#2a9d8f"}),
                    html.Ol(
                        [
                            html.Li(
                                "Fill out this form and wait to be contacted by the team. Please give us at least 1 WEEK to do our initial screening.",
                                style={"marginBottom": "10px"},
                            ),
                            html.Li(
                                "Go through an interview via Zoom or Facebook Messenger with one of our volunteers.",
                                style={"marginBottom": "10px"},
                            ),
                            html.Li(
                                "Visit the shelter, pay the Adoption Fee (₱1000), and bring home your new best fur friend (once you pass the interview).",
                            ),
                        ],
                        style={
                            "fontSize": "16px",
                            "lineHeight": "1.7",
                            "marginLeft": "20px",
                            "color": "#444",
                        },
                    ),
                ],
                width=10,
                className="mx-auto mb-4",
            ),
        ),

        # Additional Information
        dbc.Row(
            dbc.Col(
                dbc.Alert(
                    [
                        html.P(
                            "Undecided about adopting but want to learn more? Fill out this form, "
                            "and one of our volunteers will reach out to help assess if you’re ready for a rescue.",
                            className="mb-2",
                        ),
                        html.P(
                            "IMPORTANT: Our Shelters are located in BULACAN and BACOLOD. Adopters should be "
                            "willing to travel to our shelters to meet and pick up the rescue they want to adopt."
                        ),
                    ],
                    color="info",
                    style={
                        "borderRadius": "10px",
                        "fontSize": "16px",
                        "lineHeight": "1.7",
                    },
                ),
                width=10,
                className="mx-auto mb-4",
            ),
        ),

        # Adoption Fee
        dbc.Row(
            dbc.Col(
                dbc.Alert(
                    "Starting January 2022, we are implementing a PHP1,000 ADOPTION FEE to support shelter upkeep and the rehabilitation of rescues.",
                    color="warning",
                    className="text-center",
                    style={
                        "borderRadius": "10px",
                        "fontSize": "16px",
                        "fontWeight": "bold",
                    },
                ),
                width=10,
                className="mx-auto mb-4",
            ),
        ),

        # "Get Started" Button
        dbc.Row(
            dbc.Col(
                dbc.Button(
                    "GET STARTED",
                    href="/adopt/adoptionForm",
                    color="success",
                    className="btn-lg",
                    style={
                        "width": "200px",
                        "fontSize": "18px",
                        "fontWeight": "bold",
                        "boxShadow": "0 4px 8px rgba(0,0,0,0.2)",
                    },
                ),
                className="text-center",
            )
        ),
    ],
    style={
        "padding": "50px 20px",
        "backgroundColor": "#FAF3EB",
        "fontFamily": "Arial, sans-serif",
    },
)

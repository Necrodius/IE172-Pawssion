import dash
import dash_bootstrap_components as dbc
from dash import html

from app import app

# Styling for general components
header_style = {"fontWeight": "bold", "fontSize": "2.5rem", "textAlign": "center", "color": "#2a9d8f"}
section_heading_style = {"fontSize": "2rem", "fontWeight": "bold", "marginBottom": "15px", "color": "#264653"}
paragraph_style = {"fontSize": "1.1rem", "lineHeight": "1.8", "color": "#555555", "textAlign": "justify"}

# Layout
layout = html.Div(
    style={"padding": "50px 150px", "backgroundColor": "#FAF3EB", "fontFamily": "Arial, sans-serif"},
    children=[
        # Intro Section
        html.Div(
            [
                html.H2(
                    "50 dogs on death row. To be executed by gunshot. What would you do?",
                    style=header_style
                ),
                html.P(
                    "One brave woman refused to just stand by, and that is how Pawssion Project was born. "
                    "Founded in October 2018 by Malou Perez, Pawssion Project Foundation Inc. is a non-profit "
                    "organization dedicated to the rescue, rehabilitation and rehoming abused, abandoned and neglected animals.",
                    style=paragraph_style,
                ),
                html.P(
                    "Pawssion Project began in Bacolod, armed simply with a lot of hope, courage and the unwavering support of a few good friends. "
                    "After that first pound rescue, numerous reports poured in one after another, leading to the opening of a second shelter in Bulacan in 2019. "
                    "The journey has led Pawssion Project to more than 2000 rescues and over 1000 rehomed animals.",
                    style=paragraph_style,
                ),
                html.Div(
                    html.Img(
                        src="https://placekitten.com/800/400",  # Replace with a relevant image
                        style={"width": "100%", "borderRadius": "10px", "margin": "30px 0"},
                    ),
                    className="text-center",
                ),
            ],
            style={"marginBottom": "50px"},
        ),

        # Call to Action Section
        html.Div(
            [
                html.H3("We Believe in Action", style=section_heading_style),
                html.P(
                    "The problem is far greater than what one organization can solve alone. Dogs continue to be executed in city pounds, "
                    "and the number of strays and neglected pets are rising dramatically. But we believe that WE CAN ALL DO SOMETHING to help improve animal welfare in our country.",
                    style=paragraph_style,
                ),
            ],
            style={"backgroundColor": "#E9F5F3", "padding": "30px", "borderRadius": "10px", "marginBottom": "50px"},
        ),

        # Mission and Vision Section
        html.Div(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.H4("Our Mission", className="card-title", style={"color": "#2a9d8f"}),
                                        html.P(
                                            "To rescue, rehabilitate, and rehome abused, abandoned, and neglected animals.",
                                            className="card-text",
                                            style={"textAlign": "center"},
                                        ),
                                    ]
                                ),
                                className="shadow-sm",
                                style={"backgroundColor": "#ffffff", "borderRadius": "10px"},
                            ),
                            width=6,
                            className="mb-4",
                        ),
                        dbc.Col(
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.H4("Our Vision", className="card-title", style={"color": "#e76f51"}),
                                        html.P(
                                            "To create animal-friendly communities that foster kindness to all living creatures.",
                                            className="card-text",
                                            style={"textAlign": "center"},
                                        ),
                                    ]
                                ),
                                className="shadow-sm",
                                style={"backgroundColor": "#ffffff", "borderRadius": "10px"},
                            ),
                            width=6,
                            className="mb-4",
                        ),
                    ],
                    justify="center",
                ),
            ],
            style={"marginBottom": "50px"},
        ),

        # Visit Us Section
        html.Div(
            [
                html.H3("Come Visit Us!", style=section_heading_style),
                dbc.Row(
                    [
                        dbc.Col(
                            html.Div(
                                [
                                    html.H5("Bacolod Shelter", style={"color": "#2a9d8f", "fontWeight": "bold"}),
                                    html.P("Balay Pawssion, Hacienda Feliza, Brgy. Granada, Bacolod City"),
                                ],
                                style={"padding": "10px"},
                            ),
                            width=6,
                        ),
                        dbc.Col(
                            html.Div(
                                [
                                    html.H5("Bulacan Shelter", style={"color": "#e76f51", "fontWeight": "bold"}),
                                    html.P("1429 Paradise 1, Purok 7 Tungkong Mangga, SJDM, Bulacan"),
                                ],
                                style={"padding": "10px"},
                            ),
                            width=6,
                        ),
                    ],
                    justify="center",
                ),
            ],
            style={"backgroundColor": "#EDEDED", "padding": "30px", "borderRadius": "10px", "marginBottom": "50px"},
        ),

        # Initiatives Section
        html.Div(
            [
                html.H3("Our Initiatives", style=section_heading_style),
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.H5("Stray Feeding", style={"color": "#2a9d8f", "fontWeight": "bold"}),
                                        html.P(
                                            "Feeding strays helps homeless animals survive and inspires kindness in communities.",
                                            style={"textAlign": "justify"},
                                        ),
                                    ]
                                ),
                                className="shadow-sm",
                                style={"borderRadius": "10px", "height": "100%"},
                            ),
                            width=4,
                            className="mb-4",
                        ),
                        dbc.Col(
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.H5("Spay & Neuter", style={"color": "#e76f51", "fontWeight": "bold"}),
                                        html.P(
                                            "Kapon is the real solution to overpopulation. Sponsor a neuter cost today!",
                                            style={"textAlign": "justify"},
                                        ),
                                    ]
                                ),
                                className="shadow-sm",
                                style={"borderRadius": "10px", "height": "100%"},
                            ),
                            width=4,
                            className="mb-4",
                        ),
                        dbc.Col(
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.H5("Relief Drive", style={"color": "#f4a261", "fontWeight": "bold"}),
                                        html.P(
                                            "Spreading kindness during emergencies and calamities is our priority.",
                                            style={"textAlign": "justify"},
                                        ),
                                    ]
                                ),
                                className="shadow-sm",
                                style={"borderRadius": "10px", "height": "100%"},
                            ),
                            width=4,
                            className="mb-4",
                        ),
                    ],
                    justify="center",
                ),
            ],
        ),
    ],
)

import dash
import dash_bootstrap_components as dbc
from dash import html

from app import app

# Link Styling
link_style = {
    "color": "#1f77b4",  # Blue
    "textDecoration": "none",
    "fontWeight": "600",
}
link_hover = "text-decoration: underline;"  # Add hover effect inline via Bootstrap

# Layout
layout = html.Div(
    [
        # Page Header
        html.Div(
            [
                html.H1(
                    "Contact Us",
                    style={
                        "textAlign": "center",
                        "color": "#2a9d8f",
                        "fontWeight": "bold",
                        "marginBottom": "30px",
                    },
                ),
                html.P(
                    "We’re happy to hear from you! Reach out for any inquiries or concerns below.",
                    style={
                        "textAlign": "center",
                        "fontSize": "1.1rem",
                        "color": "#555555",
                    },
                ),
            ],
            style={"marginBottom": "40px"},
        ),

        # Contact Information in Cards
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H5("General Inquiries", className="card-title"),
                                html.P(
                                    "For questions and general inquiries, please email us:",
                                    className="card-text",
                                ),
                                html.A(
                                    "info@pawssionproject.org",
                                    href="mailto:info@pawssionproject.org",
                                    style=link_style,
                                    className="hover-link",
                                ),
                            ]
                        ),
                        className="shadow-sm",
                        style={"borderRadius": "10px", "height": "100%"},
                    ),
                    width=6,
                    className="mb-4",
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H5("Adoption Inquiries", className="card-title"),
                                html.P(
                                    "For adoption-related questions, contact us here:",
                                    className="card-text",
                                ),
                                html.A(
                                    "adoption@pawssionproject.org",
                                    href="mailto:adoption@pawssionproject.org",
                                    style=link_style,
                                    className="hover-link",
                                ),
                            ]
                        ),
                        className="shadow-sm",
                        style={"borderRadius": "10px", "height": "100%"},
                    ),
                    width=6,
                    className="mb-4",
                ),
            ],
            justify="center",
        ),

        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H5("Sponsor-A-Rescue", className="card-title"),
                                html.P(
                                    "For questions about sponsorships, email us here:",
                                    className="card-text",
                                ),
                                html.A(
                                    "sponsorships@pawssionproject.org",
                                    href="mailto:sponsorships@pawssionproject.org",
                                    style=link_style,
                                    className="hover-link",
                                ),
                            ]
                        ),
                        className="shadow-sm",
                        style={"borderRadius": "10px", "height": "100%"},
                    ),
                    width=6,
                    className="mb-4",
                ),
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H5("Partnerships", className="card-title"),
                                html.P(
                                    "For partnership inquiries, email us here:",
                                    className="card-text",
                                ),
                                html.A(
                                    "partners@pawssionproject.org",
                                    href="mailto:partners@pawssionproject.org",
                                    style=link_style,
                                    className="hover-link",
                                ),
                            ]
                        ),
                        className="shadow-sm",
                        style={"borderRadius": "10px", "height": "100%"},
                    ),
                    width=6,
                    className="mb-4",
                ),
            ],
            justify="center",
        ),

        # Urgent Concerns
        html.Div(
            [
                html.P(
                    "For urgent concerns, please send us a message on our Facebook page for faster response:",
                    style={"fontSize": "1.1rem", "color": "#555555", "textAlign": "center"},
                ),
                html.A(
                    "Pawssion Project on Facebook",
                    href="https://www.facebook.com/PawssionProject",
                    target="_blank",
                    style=link_style | {"fontSize": "1.1rem", "textAlign": "center"},
                ),
            ],
            style={
                "textAlign": "center",
                "marginTop": "30px",
                "paddingTop": "20px",
                "borderTop": "1px solid #dddddd",
            },
        ),
    ],
    style={
        "paddingTop": "100px",
        "paddingLeft": "50px",
        "paddingRight": "50px",
        "paddingBottom": "100px",
        "backgroundColor": "#FAF3EB",
        "fontFamily": "Arial, sans-serif",
    },
)

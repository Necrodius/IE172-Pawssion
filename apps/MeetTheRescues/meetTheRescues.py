import dash
import dash_bootstrap_components as dbc
from dash import dcc, html

from app import app

# Layout
layout = html.Div(
    [
        # Header Section
        html.Div(
            [
                html.H1(
                    "Find Your New Bestfur-iend!",
                    style={
                        "textAlign": "center",
                        "color": "#fff",
                        "padding": "20px",
                        "backgroundColor": "#2a9d8f",
                        "borderRadius": "10px",
                        "fontSize": "3rem",
                        "fontWeight": "bold",
                        "boxShadow": "0 4px 8px rgba(0,0,0,0.2)",
                    },
                ),
            ],
            className="mb-5",
        ),

        # Pet Cards Section
        html.Div(
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            [
                                html.Div(
                                    [
                                        dbc.CardImg(
                                            src="https://placedog.net/400/400?random=1",
                                            top=True,
                                            style={
                                                "opacity": "0.5",
                                                "borderRadius": "10px 10px 0 0",
                                                "transition": "opacity 0.3s ease-in-out",
                                            },
                                        ),
                                        dbc.CardImgOverlay(
                                            dbc.CardBody(
                                                [
                                                    html.H4(
                                                        "Dogs",
                                                        className="card-title",
                                                        style={
                                                            "color": "#2a9d8f",
                                                            "fontWeight": "bold",
                                                            "fontSize": "1.8rem",
                                                        },
                                                    ),
                                                    html.P(
                                                        "Dogs thrive on routine, regular exercise, and basic training. "
                                                        "They require patience and dedication but will reward you with "
                                                        "a lifetime of loyalty and companionship.",
                                                        className="card-text",
                                                        style={
                                                            "fontSize": "1rem",
                                                            "lineHeight": "1.6",
                                                        },
                                                    ),
                                                    dbc.Button(
                                                        "Explore Dogs",
                                                        color="success",
                                                        href="/meettherescues/dogs",
                                                        className="class-dog-cat-button",
                                                        style={
                                                            "marginTop": "10px",
                                                            "fontWeight": "bold",
                                                        },
                                                    ),
                                                ]
                                            )
                                        ),
                                    ],
                                    className="hover-card",
                                    style={"position": "relative"},
                                )
                            ],
                            className="shadow-lg mb-4 bg-white rounded hover-effect",
                            style={
                                "transition": "transform 0.3s ease-in-out",
                                "width": "100%",
                            },
                        ),
                        width=5,
                        className="mx-2",
                    ),
                    dbc.Col(
                        dbc.Card(
                            [
                                html.Div(
                                    [
                                        dbc.CardImg(
                                            src="https://placedog.net/400/400?random=2",
                                            top=True,
                                            style={
                                                "opacity": "0.5",
                                                "borderRadius": "10px 10px 0 0",
                                                "transition": "opacity 0.3s ease-in-out",
                                            },
                                        ),
                                        dbc.CardImgOverlay(
                                            dbc.CardBody(
                                                [
                                                    html.H4(
                                                        "Cats",
                                                        className="card-title",
                                                        style={
                                                            "color": "#e76f51",
                                                            "fontWeight": "bold",
                                                            "fontSize": "1.8rem",
                                                        },
                                                    ),
                                                    html.P(
                                                        "Cats are ideal for those seeking a low-maintenance and independent pet. "
                                                        "Once they open up, they'll fill your life with cuddles and joy!",
                                                        className="card-text",
                                                        style={
                                                            "fontSize": "1rem",
                                                            "lineHeight": "1.6",
                                                        },
                                                    ),
                                                    dbc.Button(
                                                        "Explore Cats",
                                                        color="primary",
                                                        href="/meettherescues/cats",
                                                        className="class-dog-cat-button",
                                                        style={
                                                            "marginTop": "10px",
                                                            "fontWeight": "bold",
                                                        },
                                                    ),
                                                ]
                                            )
                                        ),
                                    ],
                                    className="hover-card",
                                    style={"position": "relative"},
                                )
                            ],
                            className="shadow-lg mb-4 bg-white rounded hover-effect",
                            style={
                                "transition": "transform 0.3s ease-in-out",
                                "width": "100%",
                            },
                        ),
                        width=5,
                        className="mx-2",
                    ),
                ],
                justify="center",
            ),
            className="mb-5",
        ),

        # Information Section
        html.Div(
            [
                html.H3(
                    "About Our Rescue Shelter",
                    style={
                        "textAlign": "center",
                        "color": "#2a9d8f",
                        "fontWeight": "bold",
                        "fontSize": "2rem",
                    },
                ),
                html.Hr(
                    style={
                        "width": "50%",
                        "margin": "auto",
                        "marginBottom": "20px",
                        "border": "2px solid #2a9d8f",
                    }
                ),
                html.P(
                    "At our rescue shelter, we provide loving care to pets in need. "
                    "Each year, we help dozens of dogs and cats find their forever homes, "
                    "offering them a second chance at life.",
                    style={
                        "textAlign": "justify",
                        "fontSize": "1.1rem",
                        "lineHeight": "1.8",
                        "color": "#555",
                        "marginBottom": "15px",
                    },
                ),
                html.P(
                    "We pride ourselves on maintaining excellent facilities and ensuring every pet "
                    "receives the care they deserve. Whether you're looking for a playful pup or a cuddly kitten, "
                    "we're here to help you find the perfect companion.",
                    style={
                        "textAlign": "justify",
                        "fontSize": "1.1rem",
                        "lineHeight": "1.8",
                        "color": "#555",
                    },
                ),
                html.Div(
                    html.Img(
                        src="https://www.rd.com/wp-content/uploads/2021/01/GettyImages-1175550351-e1611077603965.jpg",
                        style={
                            "width": "100%",
                            "borderRadius": "10px",
                            "marginTop": "20px",
                            "boxShadow": "0 4px 8px rgba(0,0,0,0.2)",
                        },
                    ),
                    style={"textAlign": "center"},
                ),
            ],
            style={
                "padding": "40px",
                "backgroundColor": "#f1f5f9",
                "borderRadius": "10px",
                "boxShadow": "0 4px 8px rgba(0,0,0,0.1)",
                "maxWidth": "900px",
                "margin": "auto",
            },
        ),
    ],
    style={
        "paddingTop": "50px",
        "paddingLeft": "20px",
        "paddingRight": "20px",
        "paddingBottom": "50px",
        "backgroundColor": "#FAF3EB",
    },
)

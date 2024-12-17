import dash
import dash_bootstrap_components as dbc
from dash import dcc, html

from app import app

# Layout
layout = html.Div(
    [
        # Banner Section
        html.Div(
            [
                html.Div(
                    [
                        html.H1(
                            "Join the Pawssion Project!",
                            style={
                                "fontWeight": "bold",
                                "fontSize": "3rem",
                                "color": "#ffffff",
                                "marginBottom": "20px",
                            },
                        ),
                        html.H3(
                            "Our mission is to rescue.",
                            style={
                                "fontSize": "1.5rem",
                                "color": "#f4f4f4",
                                "marginTop": "10px",
                            },
                        ),
                        html.H3(
                            "Our dream is that one day, we won't have to.",
                            style={
                                "fontSize": "1.5rem",
                                "color": "#f4f4f4",
                                "marginBottom": "30px",
                            },
                        ),
                        dbc.Button(
                            "Help The Cause",
                            color="success",
                            href="/signin",
                            className="home-banner-button",
                            style={
                                "fontSize": "1.2rem",
                                "fontWeight": "600",
                                "padding": "10px 30px",
                                "boxShadow": "0px 4px 6px rgba(0, 0, 0, 0.3)",
                            },
                        ),
                    ],
                    className="text-center",
                    style={
                        "position": "relative",
                        "zIndex": "2",
                        "padding": "50px 20px",
                        "maxWidth": "800px",
                        "margin": "auto",
                    },
                )
            ],
            style={
                "backgroundImage": "linear-gradient(to bottom, rgba(0,0,0,0.4), rgba(0,0,0,0.8)), url('https://pawssionproject.org.ph/wp-content/uploads/2021/07/DSC_2895-scaled.jpg')",
                "backgroundSize": "cover",
                "backgroundPosition": "center",
                "height": "550px",
                "display": "flex",
                "alignItems": "center",
                "justifyContent": "center",
                "position": "relative",
                "textAlign": "center",
                "color": "#ffffff",
            },
        ),

        # Adopt and Donate Section
        html.Div(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Card(
                                [
                                    html.Div(
                                        [
                                            html.Img(
                                                src="https://cdn-icons-png.flaticon.com/512/616/616559.png",
                                                style={
                                                    "width": "80px",
                                                    "height": "80px",
                                                    "margin": "10px auto",
                                                },
                                            ),
                                            html.H2(
                                                "Adopt",
                                                className="text-center mt-3",
                                                style={
                                                    "color": "#2a9d8f",
                                                    "fontWeight": "bold",
                                                },
                                            ),
                                            html.P(
                                                "Many of our adoptables from our Bulacan and Bacolod Shelters have been rescued from death row, local pounds, or abusive environments. By adopting, you give them love and a second chance at life.",
                                                style={
                                                    "textAlign": "center",
                                                    "padding": "0 20px",
                                                    "fontSize": "1rem",
                                                    "color": "#333333",
                                                },
                                            ),
                                        ],
                                        style={"padding": "20px"},
                                    )
                                ],
                                className="shadow",
                                style={
                                    "borderRadius": "10px",
                                    "backgroundColor": "#ffffff",
                                    "textAlign": "center",
                                    "height": "100%",
                                },
                            ),
                            width=6,
                            className="p-4",
                        ),
                        dbc.Col(
                            dbc.Card(
                                [
                                    html.Div(
                                        [
                                            html.Img(
                                                src="https://cdn-icons-png.flaticon.com/512/2331/2331956.png",
                                                style={
                                                    "width": "80px",
                                                    "height": "80px",
                                                    "margin": "10px auto",
                                                },
                                            ),
                                            html.H2(
                                                "Donate",
                                                className="text-center mt-3",
                                                style={
                                                    "color": "#e76f51",
                                                    "fontWeight": "bold",
                                                },
                                            ),
                                            html.P(
                                                "We rely on your generous support to rescue animals in need. Every donation helps save lives, providing food, shelter, and medical care for animals suffering from neglect or abuse.",
                                                style={
                                                    "textAlign": "center",
                                                    "padding": "0 20px",
                                                    "fontSize": "1rem",
                                                    "color": "#f4f4f4",
                                                },
                                            ),
                                            dbc.Button(
                                                "Donate Now",
                                                color="danger",
                                                href="/donate",
                                                style={"marginTop": "10px"},
                                            ),
                                        ],
                                        style={"padding": "20px"},
                                    )
                                ],
                                className="shadow",
                                style={
                                    "borderRadius": "10px",
                                    "backgroundColor": "#2b2b2b",
                                    "textAlign": "center",
                                    "height": "100%",
                                },
                            ),
                            width=6,
                            className="p-4",
                        ),
                    ],
                    justify="center",
                )
            ],
            style={"padding": "60px 30px", "backgroundColor": "#f9f9f9"},
        ),
    ],
    style={"fontFamily": "Arial, sans-serif"},
)

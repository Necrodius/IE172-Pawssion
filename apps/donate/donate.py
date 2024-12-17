import dash
import dash_bootstrap_components as dbc
from dash import html

layout = html.Div(
    [
        # Main container for donation information
        dbc.Container(
            [
                # Heading
                html.H2(
                    "Support Our Mission",
                    style={
                        "textAlign": "center",
                        "color": "#dba514",
                        "fontWeight": "bold",
                        "marginBottom": "20px",
                    },
                ),

                # Explanatory text
                html.P(
                    "Thank you for considering a donation to our cause! "
                    "All donations are processed externally. "
                    "Please scan the QR code below using your preferred payment app.",
                    style={
                        "textAlign": "center",
                        "marginBottom": "20px",
                        "fontSize": "16px",
                        "color": "#333",
                    },
                ),

                # QR Code Image
                html.Div(
                    html.Img(
                        src="/assets/assetsqr_code_example.jpg",  # Replace with the actual path to your QR code image
                        style={
                            "width": "250px",
                            "height": "250px",
                            "margin": "0 auto",
                            "display": "block",
                        },
                    ),
                ),

                # Additional note
                html.P(
                    "If you have any questions about donations, please feel free to contact us at "
                    "info@pawssionproject.org.",
                    style={
                        "textAlign": "center",
                        "marginTop": "20px",
                        "fontSize": "14px",
                        "color": "#555",
                    },
                ),
            ],
            style={
                "paddingTop": "100px",
                "paddingBottom": "100px",
                "backgroundColor": "#FAF3EB",
                "borderRadius": "10px",
                "boxShadow": "0px 4px 10px rgba(0, 0, 0, 0.1)",
            },
        ),
    ],
    style={
        "display": "flex",
        "justifyContent": "center",
        "alignItems": "center",
        "minHeight": "100vh",
        "backgroundColor": "#FFFDF8",
    },
)

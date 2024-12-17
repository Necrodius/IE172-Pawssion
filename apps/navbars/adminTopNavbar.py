import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from app import app

def create_header_admin():
    """
    Top navbar for logged-in 'admin' accounts.
    Plain text greeting: "Hi, {firstName lastName suffix}"
    """
    header = html.Div([
        html.Header([
            dbc.NavLink(
                html.Img(
                    src="assets/PawssionProjectLogo.png",
                    style={'width': '400px', 'maxWidth': '400px', 'height': 'auto', 'margin': '20px 0'}
                ),
                href="/",  # Redirect to homepage "/"
                style={"cursor": "pointer"}
            ),
            dbc.Nav([
                dbc.Nav([
                    html.Div([dbc.Button("Adopt", href="/adopt", className="btn-custom mx-1")]),
                    dbc.NavItem(dbc.NavLink("Donate", href="/donate", style={'color':'black'})),
                    dbc.NavItem(dbc.NavLink("Meet the Rescues", href="/meettherescues", style={'color':'black'})),
                    dbc.NavItem(dbc.NavLink("Our Story", href="/ourstory", style={'color':'black'})),
                    dbc.NavItem(dbc.NavLink("FAQs", href="/faqs", style={'color':'black'})),
                    html.Div([dbc.Button("Log Out", href="/logout", color="dark", style={'margin': '0 10px'})
]),
                ],
                navbar=True,
                style={'justifyContent':'center','display':'flex','padding':'40px'})
            ])
        ], style={
            'position':'fixed',
            'top':'0','left':'0','right':'0',
            'backgroundColor':'#F7EFCF',
            'boxShadow':'0 2px 5px rgba(0,0,0,0.1)',
            'justifyContent':'center',
            'display':'flex',
        })
    ], style={'zIndex':'999'})
    return header
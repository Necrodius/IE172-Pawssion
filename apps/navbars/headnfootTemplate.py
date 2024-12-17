import dash
import dash_bootstrap_components as dbc
from dash import dcc, html

def create_header():
    # The modal for adopt confirmation if not signed in
    adopt_modal = dbc.Modal(
        [
            dbc.ModalHeader("You must be signed in to adopt"),
            dbc.ModalFooter([
                dbc.Button("Register", id="adopt-register", href="/register", color="success", style={'marginRight':'10px'}),
                dbc.Button("Sign In", id="adopt-signin", href="/signin", color="primary"),
            ])
        ],
        id="adopt-modal",
        is_open=False,
    )

    header = html.Div([
        html.Header([
            adopt_modal,
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
                    html.Div([
                        dbc.Button("Adopt", id="adopt-button", className="btn-custom mx-1"),
                    ]),
                    dbc.NavItem(dbc.NavLink("Donate", href="/donate", style={'color':'black'})),
                    dbc.NavItem(dbc.NavLink("Meet the Rescues", href="/meettherescues", style={'color':'black'})),
                    dbc.NavItem(dbc.NavLink("Our Story", href="/ourstory", style={'color':'black'})),
                    dbc.NavItem(dbc.NavLink("FAQs", href="/faqs", style={'color':'black'})),
                    
                    html.Div([
                        dbc.Button("Log In", id="login-button-guest", color='info', href="/signin", style={'margin':'0 10px'})
                    ]),
                    html.Div([
                        dbc.Button("Register", id="register-button-guest", color='warning', href="/register", style={'margin':'0 10px'})
                    ]),
                ],
                navbar=True,
                style={'justifyContent':'center','display':'flex','padding':'40px'})
            ])
        ], style={
            'position':'fixed','top':'0','left':'0','right':'0',
            'backgroundColor':'#F7EFCF','boxShadow':'0 2px 5px rgba(0,0,0,0.1)',
            'justifyContent':'center','display':'flex',
        })
    ], style={'zIndex':'999'})
    return header

def create_footer():
    footer = html.Div([
        html.Footer(
            html.Div([
                html.P("Pawssion Project Foundation Inc.", style={'textAlign':'center'}),
                html.P("Bulacan Shelter: 1429 Paradise 1, Purok 7 Tungkong Mangga, SJDM, Bulacan", style={'textAlign':'center'}),
                html.P("Bacolod Shelter: Balay Pawssion, Google Maps: M2JV+5W, Bacolod, Negros Occidental", style={'textAlign':'center'}),
                html.P("info@pawssionproject.org", style={'textAlign':'center'})
            ], style={
                'padding':'20px',
                'backgroundColor':'#343434',
                'borderTop':'1px solid #dee2e6',
                'color':'white',
            }),
            style={'marginTop':'auto'}
        )
    ], style={'display':'flex','flexDirection':'column','minHeight':'100vh','zIndex':'9'})
    return footer

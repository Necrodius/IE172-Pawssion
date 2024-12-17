import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output
from app import app

def customerSidebar(user_session):
    navlink_style = {'marginRight': '1em'}
    sidebar_layout = html.Div(
        [
            html.Div(
                [
                    html.Img(src="/assets/icons/user (2).png", height="100px"),
                    html.H5(f"{user_session.get('firstName', '')}", style={"fontWeight": "bold"}),
                    html.H6(f"{user_session.get('lastName', '')}, {user_session.get('suffix', '')}", style={"fontWeight": "bold"}),
                    html.P("User")
                ],
                className="navbar-logo"
            ),
            html.Hr(),
            dbc.Nav(
                [
                    dbc.NavLink(
                        [
                            html.Img(
                                id="accountProfile-icon",
                                src="/assets/icons/user-filled.png",
                                height="21px",
                                style={"marginRight": "8px"}
                            ),
                            "Account Profile",
                        ],
                        href="/accountProfile",
                        style=navlink_style,
                        className="customer-admin-sideNavLink",
                        id="accountProfile-link"
                    ),
                    dbc.NavLink(
                        [
                            html.Img(
                                id="adoptionApp-icon",
                                src="/assets/icons/form-filled.png",
                                height="21px",
                                style={"marginRight": "5px"}
                            ),
                            "Adoption Application"
                        ],
                        href="/adoptionApp",
                        style=navlink_style,
                        className="customer-admin-sideNavLink",
                        id="adoptionApp-link"
                    ),
                ],
                vertical=True,
                pills=True,
            ),
        ],
        className="customer-admin-sideNavbar"
    )
    return sidebar_layout


# Define the callback ONCE outside of the function
@app.callback(
    [
        Output("accountProfile-link", "className"),
        Output("adoptionApp-link", "className"),
        Output("accountProfile-icon", "src"),
        Output("adoptionApp-icon", "src"),
    ],
    Input("url", "pathname")
)
def update_active_class_and_icons(pathname):
    active_class = "custom-navlink active"
    inactive_class = "custom-navlink"

    # Default icons
    icons = {
        "accountProfile": "/assets/icons/user-filled.png",
        "adoptionApp": "/assets/icons/form-filled.png",
    }

    # Active icons
    active_icons = {
        "accountProfile": "/assets/icons/user-outline.png",
        "adoptionApp": "/assets/icons/form-outline.png",
    }

    return [
        active_class if pathname.startswith("/accountProfile") else inactive_class,
        active_class if pathname.startswith("/adoptionApp") else inactive_class,
        active_icons["accountProfile"] if pathname.startswith("/accountProfile") else icons["accountProfile"],
        active_icons["adoptionApp"] if pathname.startswith("/adoptionApp") else icons["adoptionApp"],
    ]

# Callback to dynamically render the sidebar based on user session
@app.callback(
    Output("customer-sidebar", "children"),
    Input("user-session", "data")
)
def update_customer_sidebar(user_session):
    return customerSidebar(user_session)
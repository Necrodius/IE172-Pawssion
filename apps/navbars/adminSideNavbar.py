import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output
from app import app

def adminSidebar(user_session):
    navlink_style = {'marginRight': '1em'}
    sidebar_layout = html.Div(
        [
            html.Div(
                [
                    html.Img(src="/assets/icons/user (2).png", height="100px"),
                    html.H5(f"{user_session.get('firstName', '')}", style={"fontWeight": "bold"}),
                    html.H6(f"{user_session.get('lastName', '')}, {user_session.get('suffix', '')}", style={"fontWeight": "bold"}),
                    html.P("Admin")
                ],
                className="navbar-logo"
            ),
            html.Hr(),
            dbc.Nav(
                [
                    dbc.NavLink(
                        [
                            html.Img(id="rescuesManagement-icon", 
                                     src="/assets/icons/user-filled.png", 
                                     height="21px", 
                                     style={"marginRight": "8px"}),
                            "Rescues Management"
                        ],
                        href="/rescuesManagement", style=navlink_style, 
                        className="custom-navlink", id="rescuesManagement-link"
                    ),
                    dbc.NavLink(
                        [
                            html.Img(id="viewAdoptions-icon", 
                                     src="/assets/icons/form-filled.png", 
                                     height="21px", 
                                     style={"marginRight": "5px"}),
                            "Adoption Applications"
                        ],
                        href="/viewAdoptions", style=navlink_style, 
                        className="custom-navlink", id="viewAdoptions-link"
                    ),
                    dbc.NavLink(
                        [
                            html.Img(id="graphs-icon", 
                                     src="/assets/icons/transaction-history-outline.png", 
                                     height="21px", 
                                     style={"marginRight": "5px"}),
                            "Data Graphs"
                        ],
                        href="/graphs", style=navlink_style, 
                        className="custom-navlink", id="graphs-link"
                    ),
                ],
                vertical=True,
                pills=True,
            ),
        ],
        className="customer-admin-sideNavbar"
    )

    return sidebar_layout


# Define the callback *once*, outside the function
@app.callback(
    [
        Output("rescuesManagement-link", "className"),
        Output("viewAdoptions-link", "className"),
        Output("graphs-link", "className"),
        Output("rescuesManagement-icon", "src"),
        Output("viewAdoptions-icon", "src"),
        Output("graphs-icon", "src"),
    ],
    Input("url", "pathname")
)
def update_active_class_and_icons(pathname):
    active_class = "custom-navlink active"
    inactive_class = "custom-navlink"

    # Default icons
    icons = {
        "rescuesManagement": "/assets/icons/user-filled.png",
        "viewAdoptions": "/assets/icons/form-filled.png",
        "graphs": "/assets/icons/transaction-history-filled.png",
    }

    # Active icons
    active_icons = {
        "rescuesManagement": "/assets/icons/user-outline.png",
        "viewAdoptions": "/assets/icons/form-outline.png",
        "graphs": "/assets/icons/transaction-history-outline.png",
    }

    return [
        active_class if pathname.startswith("/rescuesManagement") else inactive_class,
        active_class if pathname.startswith("/viewAdoptions") else inactive_class,
        active_class if pathname.startswith("/graphs") else inactive_class,
        active_icons["rescuesManagement"] if pathname.startswith("/rescuesManagement") else icons["rescuesManagement"],
        active_icons["viewAdoptions"] if pathname.startswith("/viewAdoptions") else icons["viewAdoptions"],
        active_icons["graphs"] if pathname.startswith("/graphs") else icons["graphs"],
    ]

# Callback to dynamically render the sidebar based on user session
@app.callback(
    Output("admin-sidebar", "children"),
    Input("user-session", "data")
)
def update_admin_sidebar(user_session):
    return adminSidebar(user_session)
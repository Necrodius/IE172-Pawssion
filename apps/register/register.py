import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State
from dash.exceptions import PreventUpdate
from dbconnect import modifyDB  # Your DB insertion function
from app import app             # The Dash instance

# Updated dictionary of Philippine regions -> major cities
PH_PROVINCES = {
    "Region I - Ilocos Region": [
        {"label": "Laoag City (Ilocos Norte)", "value": "Laoag City"},
        {"label": "Vigan City (Ilocos Sur)", "value": "Vigan City"},
        {"label": "San Fernando City (La Union)", "value": "San Fernando (La Union)"},
        {"label": "Dagupan City (Pangasinan)", "value": "Dagupan City"}
    ],
    "Region II - Cagayan Valley": [
        {"label": "Tuguegarao City (Cagayan)", "value": "Tuguegarao City"},
        {"label": "Ilagan City (Isabela)", "value": "Ilagan City"},
        {"label": "Cauayan City (Isabela)", "value": "Cauayan City"},
        {"label": "Bayombong (Nueva Vizcaya)", "value": "Bayombong"}
    ],
    "Region III - Central Luzon": [
        {"label": "Angeles City (Pampanga)", "value": "Angeles City"},
        {"label": "San Fernando City (Pampanga)", "value": "San Fernando (Pampanga)"},
        {"label": "Balanga City (Bataan)", "value": "Balanga City"},
        {"label": "Olongapo City (Zambales)", "value": "Olongapo City"}
    ],
    "Region IV-A - CALABARZON": [
        {"label": "Calamba City (Laguna)", "value": "Calamba City"},
        {"label": "Antipolo City (Rizal)", "value": "Antipolo City"},
        {"label": "Batangas City (Batangas)", "value": "Batangas City"},
        {"label": "Lucena City (Quezon)", "value": "Lucena City"}
    ],
    "MIMAROPA Region": [
        {"label": "Puerto Princesa (Palawan)", "value": "Puerto Princesa"},
        {"label": "Calapan City (Oriental Mindoro)", "value": "Calapan City"},
        {"label": "Odiongan (Romblon)", "value": "Odiongan"},
        {"label": "Boac (Marinduque)", "value": "Boac"}
    ],
    "Region V - Bicol Region": [
        {"label": "Legazpi City (Albay)", "value": "Legazpi City"},
        {"label": "Naga City (Camarines Sur)", "value": "Naga City"},
        {"label": "Sorsogon City (Sorsogon)", "value": "Sorsogon City"},
        {"label": "Masbate City (Masbate)", "value": "Masbate City"}
    ],
    "Region VI - Western Visayas": [
        {"label": "Iloilo City (Iloilo)", "value": "Iloilo City"},
        {"label": "Bacolod City (Negros Occidental)", "value": "Bacolod City"},
        {"label": "Roxas City (Capiz)", "value": "Roxas City"},
        {"label": "Kalibo (Aklan)", "value": "Kalibo"}
    ],
    "Region VII - Central Visayas": [
        {"label": "Cebu City (Cebu)", "value": "Cebu City"},
        {"label": "Lapu-Lapu City (Cebu)", "value": "Lapu-Lapu City"},
        {"label": "Tagbilaran City (Bohol)", "value": "Tagbilaran City"},
        {"label": "Dumaguete City (Negros Oriental)", "value": "Dumaguete City"}
    ],
    "Region VIII - Eastern Visayas": [
        {"label": "Tacloban City (Leyte)", "value": "Tacloban City"},
        {"label": "Ormoc City (Leyte)", "value": "Ormoc City"},
        {"label": "Catbalogan City (Samar)", "value": "Catbalogan City"},
        {"label": "Borongan City (Eastern Samar)", "value": "Borongan City"}
    ],
    "Region IX - Zamboanga Peninsula": [
        {"label": "Zamboanga City", "value": "Zamboanga City"},
        {"label": "Dipolog City (Zamboanga del Norte)", "value": "Dipolog City"},
        {"label": "Pagadian City (Zamboanga del Sur)", "value": "Pagadian City"},
        {"label": "Ipil (Zamboanga Sibugay)", "value": "Ipil"}
    ],
    "Region X - Northern Mindanao": [
        {"label": "Cagayan de Oro City (Misamis Oriental)", "value": "Cagayan de Oro"},
        {"label": "Iligan City (Lanao del Norte)", "value": "Iligan City"},
        {"label": "Malaybalay City (Bukidnon)", "value": "Malaybalay City"},
        {"label": "Oroquieta City (Misamis Occidental)", "value": "Oroquieta City"}
    ],
    "Region XI - Davao Region": [
        {"label": "Davao City (Davao del Sur)", "value": "Davao City"},
        {"label": "Tagum City (Davao del Norte)", "value": "Tagum City"},
        {"label": "Panabo City (Davao del Norte)", "value": "Panabo City"},
        {"label": "Mati City (Davao Oriental)", "value": "Mati City"}
    ],
    "Region XII - SOCCSKSARGEN": [
        {"label": "General Santos City (South Cotabato)", "value": "General Santos City"},
        {"label": "Koronadal City (South Cotabato)", "value": "Koronadal City"},
        {"label": "Kidapawan City (Cotabato)", "value": "Kidapawan City"},
        {"label": "Tacurong City (Sultan Kudarat)", "value": "Tacurong City"}
    ],
    "Region XIII - Caraga": [
        {"label": "Butuan City (Agusan del Norte)", "value": "Butuan City"},
        {"label": "Surigao City (Surigao del Norte)", "value": "Surigao City"},
        {"label": "Tandag City (Surigao del Sur)", "value": "Tandag City"},
        {"label": "Bayugan City (Agusan del Sur)", "value": "Bayugan City"}
    ],
    "NCR - National Capital Region": [
        {"label": "Manila", "value": "Manila"},
        {"label": "Quezon City", "value": "Quezon City"},
        {"label": "Makati City", "value": "Makati City"},
        {"label": "Taguig City", "value": "Taguig City"}
    ],
    "CAR - Cordillera Administrative Region": [
        {"label": "Baguio City (Benguet)", "value": "Baguio City"},
        {"label": "Tabuk City (Kalinga)", "value": "Tabuk City"},
        {"label": "Bontoc (Mountain Province)", "value": "Bontoc"},
        {"label": "La Trinidad (Benguet)", "value": "La Trinidad"}
    ],
    "BARMM - Bangsamoro Autonomous Region in Muslim Mindanao": [
        {"label": "Marawi City (Lanao del Sur)", "value": "Marawi City"},
        {"label": "Lamitan City (Basilan)", "value": "Lamitan City"},
        {"label": "Jolo (Sulu)", "value": "Jolo"},
        {"label": "Bongao (Tawi-Tawi)", "value": "Bongao"}
    ],
}

layout = html.Div([
    dcc.Location(id="cancel-redirect", refresh=True),

    dbc.Modal(
        [
            dbc.ModalHeader("Registration Successful"),
            dbc.ModalBody(id="success-modal-message"),
            dbc.ModalFooter(
                dbc.Button("Sign In", id="signin-button-modal", color="primary", href="/signin")
            ),
        ],
        id="success-modal",
        is_open=False,
    ),

    html.H1("Create an Account", style={'textAlign': 'center','marginBottom':'20px'}),
    html.P("Please fill out all required fields.", style={'textAlign': 'center','marginBottom':'40px'}),

    dbc.Form([
        # Row 1: Last Name, First Name, Middle Name, Suffix, Birthdate
        dbc.Row([
            dbc.Col([
                dbc.Label("Last Name", html_for="last-name"),
                dbc.Input(type="text", id="last-name", placeholder="Enter Last Name", required=True)
            ], width=2),

            dbc.Col([
                dbc.Label("First Name", html_for="first-name"),
                dbc.Input(type="text", id="first-name", placeholder="Enter First Name", required=True)
            ], width=2),

            dbc.Col([
                dbc.Label("Middle Name", html_for="middle-name"),
                dbc.Input(type="text", id="middle-name", placeholder="Enter Middle Name")
            ], width=2),

            dbc.Col([
                dbc.Label("Suffix (e.g., Jr., III)", html_for="suffix"),
                dbc.Input(type="text", id="suffix", placeholder="Enter Suffix")
            ], width=2),

            dbc.Col([
                dbc.Label("Birthdate", html_for="birthdate"),
                dbc.Input(type="date", id="birthdate", required=True)
            ], width=4),
        ], className="mb-3"),

        # Row 2: Province, City, Street
        dbc.Row([
            dbc.Col([
                dbc.Label("Province / Region", html_for="province"),
                dcc.Dropdown(
                    id="province",
                    options=[{"label": region, "value": region} for region in PH_PROVINCES.keys()],
                    placeholder="Select Province/Region",
                    clearable=False
                )
            ], width=4),

            dbc.Col([
                dbc.Label("City / Municipality", html_for="city"),
                dcc.Dropdown(
                    id="city",
                    placeholder="Select City",
                    clearable=False
                )
            ], width=4),

            dbc.Col([
                dbc.Label("Street / Lot / Bldg", html_for="street"),
                dbc.Input(type="text", id="street", placeholder="Enter street or lot no.", required=True)
            ], width=4),
        ], className="mb-3"),

        # Row 3: Contact Number, Email, Facebook, Instagram
        dbc.Row([
            dbc.Col([
                dbc.Label("Contact Number", html_for="contact-number"),
                dbc.Input(type="tel", id="contact-number", placeholder="Enter contact number", required=True)
            ], width=3),

            dbc.Col([
                dbc.Label("Email", html_for="email"),
                dbc.Input(type="email", id="email", placeholder="Enter email", required=True),
            ], width=3),

            dbc.Col([
                dbc.Label("Facebook Link", html_for="facebook"),
                dbc.Input(type="url", id="facebook", placeholder="Enter Facebook Link"),
            ], width=3),

            dbc.Col([
                dbc.Label("Instagram Link", html_for="instagram"),
                dbc.Input(type="url", id="instagram", placeholder="Enter Instagram Link"),
            ], width=3),
        ], className="mb-3"),

        # Row 4: Occupation, Dwelling Type, Dwelling Own, Pets Allowed
        dbc.Row([
            dbc.Col([
                dbc.Label("Occupation", html_for="occupation"),
                dbc.Input(type="text", id="occupation", placeholder="Enter Occupation", required=True)
            ], width=3),

            dbc.Col([
                dbc.Label("Dwelling Type", html_for="dwelling-type"),
                dbc.Input(type="text", id="dwelling-type", placeholder="e.g. Apartment, House", required=True)
            ], width=3),

            dbc.Col([
                dbc.Label("Do you own this dwelling?", html_for="dwelling-own"),
                dcc.Dropdown(
                    id="dwelling-own",
                    options=[
                        {"label": "Yes", "value": True},
                        {"label": "No", "value": False},
                    ],
                    value=True,
                    clearable=False
                )
            ], width=3),

            dbc.Col([
                dbc.Label("Are Pets Allowed?", html_for="pets-allowed"),
                dcc.Dropdown(
                    id="pets-allowed",
                    options=[
                        {"label": "Yes", "value": True},
                        {"label": "No", "value": False},
                    ],
                    value=True,
                    clearable=False
                )
            ], width=3),
        ], className="mb-3"),

        # Row 5: Account Type, Password
        dbc.Row([
            dbc.Col([
                dbc.Label("Account Type", html_for="account-type"),
                dcc.Dropdown(
                    id="account-type",
                    options=[
                        {"label": "User", "value": "user"},
                        {"label": "Admin", "value": "admin"},
                    ],
                    value="user",
                    clearable=False,
                )
            ], width=6),

            dbc.Col([
                dbc.Label("Password", html_for="password"),
                dbc.Input(type="password", id="password", placeholder="Enter password", required=True)
            ], width=6),
        ], className="mb-3"),

    ], style={"marginBottom": "30px"}),

    html.Div([
        dbc.Row([
            dbc.Col(
                dbc.Button("Cancel", id="cancel-button", color="secondary", style={'width': '100px'}),
                width="auto"
            ),
            dbc.Col(
                dbc.Button("Register", id="register-button", color="primary", style={'width': '100px'}),
                width="auto"
            )
        ], justify="end", style={'paddingTop': '20px'}),
    ], style={"textAlign": "right"}),

], style={
    "paddingTop": "50px",
    "paddingLeft": "150px",
    "paddingRight": "150px",
    "paddingBottom": "200px",
    "backgroundColor": "#FAF3EB"
})

# ----- CALLBACKS ----- #

@app.callback(
    Output("city", "options"),
    Input("province", "value")
)
def update_city_options(selected_region):
    """
    Dynamically updates the city dropdown based on the chosen region in PH_PROVINCES.
    """
    if not selected_region:
        raise PreventUpdate
    return PH_PROVINCES[selected_region]

@app.callback(
    Output("cancel-redirect", "href"),
    Input("cancel-button", "n_clicks"),
    [
        State("last-name", "value"),
        State("first-name", "value"),
        State("middle-name", "value"),
        State("suffix", "value"),
        State("birthdate", "value"),
        State("province", "value"),
        State("city", "value"),
        State("street", "value"),
        State("contact-number", "value"),
        State("email", "value"),
        State("facebook", "value"),
        State("instagram", "value"),
        State("occupation", "value"),
        State("dwelling-type", "value"),
        State("dwelling-own", "value"),
        State("pets-allowed", "value"),
        State("account-type", "value"),
        State("password", "value")
    ],
    prevent_initial_call=True
)
def clear_fields_and_redirect(cancel_click, *fields):
    """
    Clears form (by redirecting) when Cancel is clicked.
    """
    if not cancel_click:
        raise PreventUpdate
    return "/"

@app.callback(
    [Output("success-modal", "is_open"),
     Output("success-modal-message", "children")],
    Input("register-button", "n_clicks"),
    [
        State("last-name", "value"),
        State("first-name", "value"),
        State("middle-name", "value"),
        State("suffix", "value"),
        State("birthdate", "value"),
        State("province", "value"),
        State("city", "value"),
        State("street", "value"),
        State("contact-number", "value"),
        State("email", "value"),
        State("facebook", "value"),
        State("instagram", "value"),
        State("occupation", "value"),  # maps to incomeSource
        State("dwelling-type", "value"),
        State("dwelling-own", "value"),
        State("pets-allowed", "value"),
        State("account-type", "value"),
        State("password", "value"),
    ],
    prevent_initial_call=True
)
def register_user(register_click, last_name, first_name, middle_name, suffix, birthdate,
                  region, city, street,
                  contact_no, email, facebook, instagram,
                  occupation, dwelling_type, dwelling_own, pets_allowed,
                  account_type, password):
    """
    Inserts into DB on Register click, then shows success modal.
    """
    if not register_click:
        raise PreventUpdate

    required_fields = [
        last_name, first_name, birthdate,
        region, city, street,
        contact_no, email, occupation,
        dwelling_type, password, account_type
    ]
    if any(f is None or f.strip() == "" for f in required_fields):
        return True, dbc.Alert("Please fill in all required fields.", color="danger")

    insert_sql = """
        INSERT INTO Users (
            lastName, firstName, middleName, suffix,
            street, city, province, contactNo,
            emailAddress, facebookLink, instagramLink,
            birthDate, incomeSource, dwellingType, dwellingOwn, petsAllowed,
            password, accountType
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s,
                  %s, %s, %s, %s, %s, %s, %s, %s,
                  %s, %s)
    """

    values = [
        last_name, first_name, middle_name, suffix,
        street, city, region, contact_no,
        email, facebook, instagram,
        birthdate, occupation,  # maps to incomeSource
        dwelling_type, dwelling_own, pets_allowed,
        password, account_type
    ]

    try:
        modifyDB(insert_sql, values)
    except Exception as e:
        return True, dbc.Alert(f"Error inserting user: {str(e)}", color="danger")

    suffix_str = f" {suffix}" if suffix else ""
    full_name = f"{first_name} {last_name}{suffix_str}"
    success_message = html.Div([
        html.P(f"Successfully signed up as {full_name}!", style={"marginBottom": "0"})
    ])
    return True, success_message

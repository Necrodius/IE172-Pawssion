import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output
from urllib.parse import parse_qs
from app import app
from dbconnect import getDataFromDB

# Function to generate a dbc.Table from a dictionary
def create_table(data_dict, fixed_width="200px"):
    table_rows = [
        html.Tr([html.Th(key, style={"width": fixed_width}), html.Td(value if value else "N/A")])
        for key, value in data_dict.items()
    ]
    return dbc.Table([html.Tbody(table_rows)], bordered=True, striped=True, hover=True, responsive=True)

# Layout
layout = html.Div(
    [
        html.Div(id="admin-sidebar", style={"width": "250px", "flexShrink": 0}),
        html.Div(
            [
                dbc.Row(
                    [
                        dbc.Col(html.H2("Adoption Application Details", style={"color": "#dba514", "font-weight": "bold"}), width="auto"),
                        dbc.Col(
                            dbc.Button("Back", color="primary", href="/viewAdoptions", style={"width": "100px"}),
                            width="auto",
                            style={"textAlign": "right"},
                        ),
                    ],
                    className="mb-4",
                ),
                dbc.Row(
                    [
                        dbc.Col([html.H4("Adopter Personal Information"), html.Div(id="personal-info-table-apps")], width=6),
                        dbc.Col([html.H4("Chosen Pet Information"), html.Div(id="pet-info-table")], width=6),
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col([html.H4("Household Information"), html.Div(id="household-info-table")], width=6),
                        dbc.Col([html.H4("Adoption Motivation"), html.Div(id="motivation-info-table")], width=6),
                    ]
                ),
            ],
            className="customer-admin-menu",
        ),
    ]
)

# Callback to fetch and display dynamic data
@app.callback(
    [
        Output("personal-info-table-apps", "children"),
        Output("pet-info-table", "children"),
        Output("household-info-table", "children"),
        Output("motivation-info-table", "children"),
    ],
    Input("url", "search"),
)
def load_adoption_details(query_string):
    if not query_string:
        raise dash.exceptions.PreventUpdate

    # Parse 'id' from the URL
    query_params = parse_qs(query_string.lstrip("?"))
    app_id = query_params.get("id", [None])[0]

    if not app_id:
        raise dash.exceptions.PreventUpdate

    # SQL Query to fetch data for the specific applicationID
    query = """
        SELECT 
            u.lastName, u.firstName, u.middleName, u.suffix, u.street, u.city, u.province, u.contactNo, 
            u.emailAddress, u.facebookLink, u.instagramLink, u.birthDate, u.incomeSource, u.dwellingType, 
            u.dwellingOwn, u.petsAllowed,
            r.rescueName, r.category, r.gender, r.age, r.breed, r.medCondition, r.description,
            a.householdNo, a.householdSupport, a.ownershipExperience, a.vetCheck, a.petsCaredList, 
            a.petsCaredStatus, a.foundPawssion, a.whyAdopt
        FROM Application a
        JOIN Users u ON a.userID = u.userID
        JOIN Rescue r ON a.rescueID = r.rescueID
        WHERE a.applicationID = %s
    """
    columns = [
        "lastName", "firstName", "middleName", "suffix", "street", "city", "province", "contactNo", 
        "emailAddress", "facebookLink", "instagramLink", "birthDate", "incomeSource", "dwellingType", 
        "dwellingOwn", "petsAllowed", "rescueName", "category", "gender", "age", "breed", "medCondition", 
        "description", "householdNo", "householdSupport", "ownershipExperience", "vetCheck", "petsCaredList", 
        "petsCaredStatus", "foundPawssion", "whyAdopt"
    ]

    data = getDataFromDB(query, [app_id], columns)
    if data.empty:
        return [dbc.Alert("No data found for this application.", color="danger")]*4

    # Extract row data
    row = data.iloc[0]

    # Personal Information
    personal_info = {
        "Last Name": row["lastName"],
        "First Name": row["firstName"],
        "Middle Name": row["middleName"],
        "Suffix": row["suffix"],
        "Street": row["street"],
        "City": row["city"],
        "Province": row["province"],
        "Contact Number": row["contactNo"],
        "Email Address": row["emailAddress"],
        "Facebook Link": row["facebookLink"],
        "Instagram Link": row["instagramLink"],
        "Birth Date": row["birthDate"],
        "Income Source": row["incomeSource"],
    }

    # Pet Information
    pet_info = {
        "Rescue Name": row["rescueName"],
        "Category": row["category"],
        "Gender": row["gender"],
        "Age": row["age"],
        "Breed": row["breed"],
        "Medical Condition": row["medCondition"],
        "Description": row["description"],
    }

    # Household Information
    household_info = {
        "Number of Household Members": row["householdNo"],
        "Household Support": row["householdSupport"],
        "Dwelling Type": row["dwellingType"],
        "Dwelling Ownership": "Self-Owned" if row["dwellingOwn"] else "Rented",
        "Pets Allowed": "Yes" if row["petsAllowed"] else "No",
    }

    # Adoption Motivation
    motivation_info = {
        "Ownership Experience": row["ownershipExperience"],
        "Vet Check": "Yes" if row["vetCheck"] else "No",
        "Pets Cared List": row["petsCaredList"],
        "Pets Cared Status": row["petsCaredStatus"],
        "Found Pawssion": row["foundPawssion"],
        "Why Adopt": row["whyAdopt"],
    }

    return (
        create_table(personal_info),
        create_table(pet_info),
        create_table(household_info),
        create_table(motivation_info),
    )

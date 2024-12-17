import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State, ctx
from dbconnect import getDataFromDB, modifyDB
from app import app

# Layout
layout = html.Div(
    [
        # Page Title
        dbc.Row(
            dbc.Col(
                html.H1("Adoption Application Form", className="text-center mb-4", style={"color": "#2a9d8f"}),
                width=12,
            )
        ),

        # Application Form
        dbc.Form(
            [
                # Section 1: Household Information
                html.H4("Household Information", className="text-primary mb-3"),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Label("Household Size", html_for="household-no"),
                                dbc.Input(
                                    type="number",
                                    id="household-no",
                                    placeholder="Number of people",
                                    required=True,
                                    className="form-control"
                                ),
                            ],
                            width=6,
                        ),
                        dbc.Col(
                            [
                                dbc.Label("Household Support", html_for="household-support"),
                                dcc.Dropdown(
                                    id="household-support",
                                    options=[
                                        {"label": "Yes", "value": "Yes"},
                                        {"label": "No", "value": "No"},
                                        {"label": "Not Sure", "value": "Not Sure"},
                                    ],
                                    placeholder="Does your household support adopting?",
                                    clearable=False,
                                ),
                            ],
                            width=6,
                        ),
                    ],
                    className="mb-4",
                ),

                # Section 2: Rescue Selection
                html.H4("Select a Rescue", className="text-primary mb-3"),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dcc.Dropdown(
                                    id="rescue-dropdown",
                                    placeholder="Select a rescue to adopt",
                                    clearable=False,
                                ),
                            ],
                            width=12,
                        )
                    ],
                    className="mb-4",
                ),

                # Section 3: Pet Ownership Experience
                html.H4("Pet Ownership Experience", className="text-primary mb-3"),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Label("Experience with Pet Ownership"),
                                dbc.Textarea(
                                    id="ownership-experience",
                                    placeholder="Describe your experience with pet ownership",
                                    rows=3,
                                ),
                            ],
                            width=12,
                        ),
                    ],
                    className="mb-4",
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Label("Pets You've Cared For"),
                                dbc.Textarea(
                                    id="pets-cared-list",
                                    placeholder="List pets you've cared for",
                                    rows=3,
                                ),
                            ],
                            width=6,
                        ),
                        dbc.Col(
                            [
                                dbc.Label("What Happened to Those Pets?"),
                                dbc.Textarea(
                                    id="pets-cared-status",
                                    placeholder="Describe what happened",
                                    rows=3,
                                ),
                            ],
                            width=6,
                        ),
                    ],
                    className="mb-4",
                ),

                # Section 4: Additional Questions
                html.H4("Additional Information", className="text-primary mb-3"),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Label("Have You Consulted a Vet Before?"),
                                dcc.Dropdown(
                                    id="vet-check",
                                    options=[
                                        {"label": "Yes", "value": True},
                                        {"label": "No", "value": False},
                                    ],
                                    placeholder="Select an option",
                                    clearable=False,
                                ),
                            ],
                            width=6,
                        ),
                        dbc.Col(
                            [
                                dbc.Label("How Did You Find Pawssion Project?"),
                                dbc.Input(
                                    id="found-pawssion",
                                    placeholder="Social Media, Friends, Events, etc.",
                                ),
                            ],
                            width=6,
                        ),
                    ],
                    className="mb-4",
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Label("Why Do You Want to Adopt?"),
                                dbc.Textarea(
                                    id="why-adopt",
                                    placeholder="Explain why you want to adopt a rescue pet",
                                    rows=4,
                                ),
                            ],
                            width=12,
                        ),
                    ],
                    className="mb-4",
                ),

                # Section 5: Interview Schedule
                html.H4("Interview Schedule", className="text-primary mb-3"),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Label("Interview Date"),
                                dbc.Input(type="date", id="interview-date", required=True),
                            ],
                            width=6,
                        ),
                        dbc.Col(
                            [
                                dbc.Label("Interview Time"),
                                dbc.Input(type="time", id="interview-time", required=True),
                            ],
                            width=6,
                        ),
                    ],
                    className="mb-4",
                ),

                # Buttons
                dbc.Row(
                    [
                        dbc.Col(dbc.Button("Cancel", color="secondary", href="/", style={"width": "150px"})),
                        dbc.Col(dbc.Button("Submit", id="submit-application", color="success", style={"width": "150px"})),
                    ],
                    justify="end",
                ),
                
                html.Div(id="form-error-message", style={"textAlign": "center", "color": "red", "marginTop": "10px"}),
            ],
            style={
                "maxWidth": "900px",
                "margin": "auto",
                "backgroundColor": "#fff",
                "padding": "30px",
                "borderRadius": "10px",
                "boxShadow": "0 4px 8px rgba(0,0,0,0.1)",
            },
        ),

        # Success Modal
        dbc.Modal(
            [
                dbc.ModalHeader("Application Submitted Successfully!"),
                dbc.ModalBody("Thank you for your application. We will contact you soon for the next steps."),
                dbc.ModalFooter(dbc.Button("Close", id="close-success", href="/", color="success")),
            ],
            id="success-modal-application",
            is_open=False,
        ),
    ],
    style={"padding": "30px", "backgroundColor": "#f8f9fa"},
)

# Callbacks
@app.callback(
    Output("rescue-dropdown", "options"),
    Input("url", "pathname"),
)
def fetch_rescues(_):
    query = "SELECT rescueID, rescueName FROM Rescue"
    rescues = getDataFromDB(query, [], ["rescueID", "rescueName"])
    return [{"label": rescue["rescueName"], "value": rescue["rescueID"]} for rescue in rescues.to_dict("records")]


@app.callback(
    [Output("success-modal-application", "is_open"), Output("form-error-message", "children")],
    Input("submit-application", "n_clicks"),
    [
        State("household-no", "value"),
        State("household-support", "value"),
        State("rescue-dropdown", "value"),
        State("ownership-experience", "value"),
        State("pets-cared-list", "value"),
        State("pets-cared-status", "value"),
        State("vet-check", "value"),
        State("found-pawssion", "value"),
        State("why-adopt", "value"),
        State("interview-date", "value"),
        State("interview-time", "value"),
        State("user-session", "data"),
    ],
    prevent_initial_call=True,
)
def submit_application(
    n_clicks, household_no, household_support, rescue_id, ownership_exp, pets_list, pets_status, vet_check,
    found_pawssion, why_adopt, interview_date, interview_time, user_session
):
    if not user_session or "userID" not in user_session:
        return False, "You must be logged in to submit an application."

    user_id = user_session["userID"]

    if not rescue_id:
        return False, "You must select a rescue to adopt."

    query = """
        INSERT INTO Application (
            userID, householdNo, householdSupport, rescueID, ownershipExperience,
            petsCaredList, petsCaredStatus, vetCheck, foundPawssion, whyAdopt,
            interviewDate, interviewTime
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = [user_id, household_no, household_support, rescue_id, ownership_exp, pets_list, pets_status, vet_check,
              found_pawssion, why_adopt, interview_date, interview_time]

    try:
        modifyDB(query, values)
        return True, None
    except Exception as e:
        return False, f"Error: {e}"
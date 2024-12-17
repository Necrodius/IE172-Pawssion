import dash
import dash_bootstrap_components as dbc
from dash import html

from app import app

# Styling Variables
header_style = {"fontSize": "3rem", "fontWeight": "bold", "color": "#264653", "textAlign": "center", "marginBottom": "30px"}
accordion_header_style = {"fontSize": "1.2rem", "fontWeight": "bold", "color": "#2a9d8f"}
paragraph_style = {"fontSize": "1rem", "lineHeight": "1.8", "color": "#555", "textAlign": "justify"}

# Layout
layout = html.Div(
    style={"padding": "80px 50px", "backgroundColor": "#FAF3EB", "fontFamily": "Arial, sans-serif"},
    children=[
        html.H1("Frequently Asked Questions", style=header_style),

        # Accordion for FAQs
        dbc.Accordion(
            [
                dbc.AccordionItem(
                    title="Where are your shelters located?",
                    children=html.P(
                        "Our Shelters are located in Bacolod City, Negros Occidental, and San Jose del Monte, Bulacan.",
                        style=paragraph_style,
                    ),
                ),

                dbc.AccordionItem(
                    title="What are your Official Social Media Accounts?",
                    children=html.Ul(
                        [
                            html.Li("Instagram – @pawssionproject", style=paragraph_style),
                            html.Li("Facebook – facebook.com/PAWSsionProject", style=paragraph_style),
                            html.Li("YouTube – youtube.com/c/PawssionProject", style=paragraph_style),
                            html.Li("Twitter – @pawssionproject", style=paragraph_style),
                            html.Li("TikTok – @pawssionproject", style=paragraph_style),
                            html.Li("Lyka – @pawssionproject", style=paragraph_style),
                        ]
                    ),
                ),

                dbc.AccordionItem(
                    title="What is your Adoption Process?",
                    children=html.Ol(
                        [
                            html.Li(
                                "You may start by finding a list of our rescues at: Meet the Rescues",
                                style=paragraph_style,
                            ),
                            html.Li(
                                "Once you feel ready to welcome a new family member to your home, you may fill out our Adoption Form through the ADOPT function. An Adoption Coordinator will then contact you for an interview.",
                                style=paragraph_style,
                            ),
                            html.Li(
                                "Once you pass our screening process, you may schedule a shelter visit to meet our loving rescues and take home your new best friend the same day!",
                                style=paragraph_style,
                            ),
                        ]
                    ),
                ),

                dbc.AccordionItem(
                    title="What are the Requirements to adopt?",
                    children=[
                        html.P(
                            "We do not have specific requirements, just that you pass our detailed Adoption Screening Process. "
                            "Rest assured that all details you share with the team will be kept confidential and will only be used to assess your compatibility with our Rescues.",
                            style=paragraph_style,
                        ),
                        html.P(
                            "But all we really ask from potential adopters is a lifetime commitment to consider our rescues as part of the family. "
                            "This means ensuring their well-being at all times, and providing them with a loving environment for life.",
                            style=paragraph_style,
                        ),
                    ],
                ),

                dbc.AccordionItem(
                    title="Is there an Adoption Fee?",
                    children=html.P(
                        "Please note that starting Jan 2022, we will be implementing a PHP1,000 ADOPTION FEE to help with the upkeep of the shelter "
                        "and also to cover what we have spent for the rescues’ rehabilitation. We also want to make sure that our adopters have the capacity to meet the needs of our rescues, who we all treat as family.",
                        style=paragraph_style,
                    ),
                ),

                dbc.AccordionItem(
                    title="What name should I indicate upon transferring to your Bank Accounts?",
                    children=html.P(
                        "You may indicate “Pawssion Project Foundation Inc.” for our Union Bank account. For BPO and BPI, you may input 'Ma. Lourdes Perez.'",
                        style=paragraph_style,
                    ),
                ),

                dbc.AccordionItem(
                    title="Do you rescue?",
                    children=[
                        html.P(
                            "At this time, our rescue operations are on hold as we strive to improve shelter conditions, and continue with the rehabilitation of more than 500 rescues under our care.",
                            style=paragraph_style,
                        ),
                        html.P(
                            "However, we are more than willing to provide assistance as much as we can, considering there is already a concrete plan for the animal in need (i.e., who will shoulder the expenses, and where to bring the animal upon rescue and after being cleared at the vet). Kindly please provide us with details, so we may know how to assist you further.",
                            style=paragraph_style,
                        ),
                    ],
                ),

                dbc.AccordionItem(
                    title="How can I report an Animal Cruelty Case?",
                    children=[
                        html.P(
                            "For cases of animal abuse, please seek assistance from your barangay/PNP/NBI or call 911 to report the incident. "
                            "Secure evidence such as photos and videos and find witnesses willing to testify and file an official complaint to help move the case forward and ensure justice.",
                            style=paragraph_style,
                        ),
                        html.P(
                            "Pawssion Project is not a government agency and does not have the authority to persecute suspects. "
                            "Because animal cruelty and pet neglect are criminal offenses, they must be reported to the authorities.",
                            style=paragraph_style,
                        ),
                        html.A(
                            "More details from PAWS",
                            href="https://paws.org.ph/cruelty-pet-neglect/",
                            target="_blank",
                            style={"color": "#2a9d8f", "fontWeight": "bold", "textDecoration": "none"},
                        ),
                    ],
                ),

                dbc.AccordionItem(
                    title="Can I surrender my pets?",
                    children=html.P(
                        "We strongly discourage pet surrenders since pet abandonment and irresponsible pet ownership are the root causes of stray overpopulation. "
                        "Thousands of abandoned pets/strays are euthanized every single day. For this reason, we strongly encourage exerting all possible efforts "
                        "to keep your pets or rehome them to trusted individuals, since they truly should be regarded as part of the family. And family means nobody gets left behind.",
                        style=paragraph_style,
                    ),
                ),
            ],
            flush=True,  # Removes borders between items
        ),
    ],
)

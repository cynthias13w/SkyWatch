from dash import html, dash_table
from transform.schedules import Schedules

schedules = Schedules()

applayout = html.Div(
    children=[
        html.H1(
            children='List Data Get From Lufthansa API'
        ),
       html.Div(
            children=(
                html.H3('Schedules Data'), 
                dash_table.DataTable(
                            data=schedules.normalize_df(),
                            page_size=10,
                            style_cell={'padding': '7px', 'textAlign': 'center'},
                            style_header={
                                'background': 'black'
                            }
                )
            ),
        ),
    ]
)

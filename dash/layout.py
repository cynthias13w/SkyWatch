from dash import html, dash_table, dcc
from transform.schedules import Schedules

schedules = Schedules()

applayout = html.Div(
    children=[
        html.H1(
            children='SkyWatch',
            style={'color': 'skyblue'}
        ),
        html.Div(
            children=[
                html.Label('🛫 Departure:'),
                dcc.Input(
                    id='input-1',
                    type='text',
                    placeholder='Enter Airport Code'
                ),
                html.Label('🛬 Arrival:'),
                dcc.Input(
                    id='input-2',
                    type='text',
                    placeholder='Enter Airport Code'
                ),
                html.Label('🗓️ Date:'),
                dcc.Input(
                    id='input-2',
                    type='text',
                    placeholder='Enter Date'
                ),
        html.Div(
            children=[
                html.H3('Schedules'),
                dash_table.DataTable(
                    data=schedules.normalize_df(),
                    page_size=10,
                    style_cell={'padding': '7px', 'textAlign': 'center'},
                    style_header={'background': 'black'}
                )
            ],
        )
            ]
        )
    ]
)

from dash import html, dash_table, dcc, Input, Output, Dash
from transform.schedules import Schedules
from functions import generate_stats_card
import dash_bootstrap_components as dbc

app = Dash()
schedules = Schedules()
tab_style = {
    'idle':{
        'borderRadius': '10px',
        'padding': '0px',
        'marginInline': '5px',
        'display':'flex',
        'alignItems':'center',
        'justifyContent':'center',
        'fontWeight': 'bold',
        'backgroundColor': '#7393B3',
        'border':'none'
    },
    'active':{
        'borderRadius': '10px',
        'padding': '0px',
        'marginInline': '5px',
        'display':'flex',
        'alignItems':'center',
        'justifyContent':'center',
        'fontWeight': 'bold',
        'border':'none',
        'textDecoration': 'underline',
        'backgroundColor': '#7393B3'
    }
}

num_of_countries = 5
applayout = html.Div(
    style={'backgroundColor': 'white'},
    children=[
        html.H1(
            children='✈️ SkyWatch',
            style={'color': '#7393B3'}
        ),
        html.Div([
            dbc.Container([
                dbc.Row(
                    dbc.Col(
                        dcc.Tabs(
                            id='graph-tabs',
                            value='overview',
                            children=[
                                dcc.Tab(label='Overview', value='overview', style=tab_style['idle'], selected_style=tab_style['active']),
                                dcc.Tab(label='Search', value='search', style=tab_style['idle'], selected_style=tab_style['active']),
                                dcc.Tab(label='About', value='about', style=tab_style['idle'], selected_style=tab_style['active'])
                            ],
                            style={'marginTop': '15px', 'height': '50px'}
                        ),
                        width=6
                    )
                )
            ]),
            dbc.Row([
                dcc.Loading([
                    html.Div(id='tabs-content')
                ], type='default', color='#deb522')
            ])
        ])
    ]
)

@app.callback(
    Output('tabs-content', 'children'),
    [Input('graph-tabs', 'value')]
)
def update_tab(tab):
    if tab == 'overview':
        return html.Div([
            html.H3('Schedules',  style={'color': 'black'}),
            dash_table.DataTable(
                data=schedules.normalize_df(),
                page_size=10,
                style_cell={'padding': '7px', 'textAlign': 'center'},
                style_header={'background': '#7393B3'}
            )
        ])
    elif tab == 'search':
        return html.Div(style={'marginTop': '15px','height':'50px'},
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
                        id='input-3',  # Changed id from 'input-2' to 'input-3' to make it unique
                        type='text',
                        placeholder='Enter Date'
                    )]
                    )
    elif tab == 'about':
        return 'Coming soon'

from dash import html, dash_table, dcc, Input, Output, Dash, State
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
# Define the modal outside the callback
modal = dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle("Flight Search Results"), close_button=True),
        dbc.ModalBody(id='modal-body'),
    ],
    id="modal",
    size="lg",
)

# Define the layout
applayout = html.Div(
    style={'backgroundColor': 'white'},
    children=[
        html.H1(children='✈️ SkyWatch', style={'color': '#7393B3'}),
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
            html.H3('Schedules', style={'color': 'black'}),
            dash_table.DataTable(
                data=schedules.normalize_df(),
                page_size=10,
                style_cell={'padding': '7px', 'textAlign': 'center'},
                style_header={'background': '#7393B3'}
            )
        ])
    elif tab == 'search':
        search_layout = html.Div(
            style={'marginTop': '15px'},
            children=[
                html.Form([
                    html.Label('🛫 Departure:'),
                    dcc.Input(
                        id='input-departure',
                        type='text',
                        placeholder='Enter Airport Code',
                        autoComplete='off'
                    ),
                    html.Br(),
                    html.Label('🛬 Arrival:'),
                    dcc.Input(
                        id='input-arrival',
                        type='text',
                        placeholder='Enter Airport Code',
                        autoComplete='off'
                    ),
                    html.Br(),
                ]),
                dbc.Row(
                    [
                        dbc.Button("🔎 Find flights", id="submit-button", color="primary")
                    ],
                    style={'marginTop': '15px'}
                ),
                modal
            ]
        )
        return search_layout
    elif tab == 'about':
        return 'Coming soon'
# Define the callback for the button click
@app.callback(
    Output("modal", "is_open"),
    Output('modal-body', 'children'),
    [Input('submit-button', 'n_clicks')],
    [State('input-departure', 'value'),
     State('input-arrival', 'value')]
)
def update_output(n_clicks, departure, arrival):
    if n_clicks:
        search_result = html.Div([
            html.H3('Schedules', style={'color': 'black'}),
            dash_table.DataTable(
                data=schedules.search_df(departure, arrival),
                page_size=10,
                style_cell={'padding': '7px', 'textAlign': 'center'},
                style_header={'background': '#7393B3'}
            )
        ])
        return True, search_result
    return False

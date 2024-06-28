from scripts.trajectory_graph import TrajectoryGraph

import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
import json
from PIL import Image


class DashApp:
    def __init__(self) -> None:
        config = json.load(open('configs/config_path.json'))
        self.default = json.load(open(config['config-path']))
        self.source = self.default['source']
        self.updating = self.default['updating']
        self.url = self.default['url']
        self.file_path = self.default['file-path']
        self.columns = self.default['columns']
        self.draw_interval = self.default['draw-interval']
        self.trajectory = TrajectoryGraph()
        self.app_setup()
        print('App init')

    def app_setup(self) -> None:
        self.app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY],
                             meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'}])
        self.app.title = 'CRS Trajectory Viewer'
        self.app._favicon = 'favicon.png'
        self.app.layout = dbc.Container([dbc.Row([
            html.Div([
                dcc.Graph(id='trajectory-graph', figure=self.trajectory.get_figure(),
                          style={'height': '100%', 'width': '100%'})
            ], style={'height': '100vh', 'width': '80%', 'float': 'left'}),
            dcc.Interval(
                id='draw-interval-component',
                interval=self.draw_interval,
                n_intervals=0),
            html.Div([
                dbc.Col([
                        html.Img(src=Image.open('scripts/assets/crs_logo.png'), style={'width': '100%'})
                        ]),
                html.Div([
                    dbc.Col([
                        dbc.RadioItems(
                            id='data-source',
                            options=[
                                {'label': 'URL', 'value': 'url'},
                                {'label': 'File', 'value': 'file'}
                            ],
                            value=self.source,
                            inline=True,
                        ),
                        dbc.Checklist(
                            id='updating-checklist',
                            options=[
                                {'label': 'Updating', 'value': 'updating'}
                            ],
                            value=[self.updating],
                        ),
                        dbc.Button('Restart Draw', id='restart-btn', n_clicks=0,
                                   style={'display': 'inline-block', 'margin-left': '10px'}
                                   ),
                    ], style={'display': 'flex', 'align-items': 'center'}),
                    dbc.Col(id='url-field', style={'display': 'block'}, children=[
                        dbc.Input(id='url-input', type='text', placeholder='Enter URL', value=self.url)
                    ]),
                    dbc.Col(id='file-field', style={'display': 'none'}, children=[
                        dbc.Input(id='file-input', type='text', placeholder='Enter local file path', value=self.file_path)
                    ]),
                    dbc.Col([
                        dbc.DropdownMenu([
                            dbc.Col(id='lon-field', children=[
                                dbc.Label('Longitude:'),
                                dbc.Input(id='lon-input', type='text', placeholder='Longitude column name', value=str(self.columns.get('lon', "")))
                            ]),
                            dbc.Col(id='lat-field', children=[
                                dbc.Label('Latitude:'),
                                dbc.Input(id='lat-input', type='text', placeholder='Latitude column name', value=str(self.columns.get('lat', "")))
                            ]),
                            dbc.Col(id='alt-field', children=[
                                dbc.Label('Altitude:'),
                                dbc.Input(id='alt-input', type='text', placeholder='Altitude column name', value=str(self.columns.get('alt', "")))
                            ]),
                            dbc.Col(id='acc-field', children=[
                                dbc.Label('Acceleration:'),
                                dbc.Input(id='acc-input', type='text', placeholder='Acceleration column name', value=str(self.columns.get('acc', "")))
                            ]),
                            dbc.Col(id='rot-field', children=[
                                dbc.Label('Rotation:'),
                                dbc.Input(id='rot-input', type='text', placeholder='Rotation column name', value=str(self.columns.get('rot', "")))
                            ]),
                            dbc.Col(id='euler-h-field', children=[
                                dbc.Label('Euler-h:'),
                                dbc.Input(id='euler-h-input', type='text', placeholder='Euler H column name', value=str(self.columns.get('euler_h', "")))
                            ]),
                            dbc.Col(id='euler-p-field', children=[
                                dbc.Label('Euler-p:'),
                                dbc.Input(id='euler-p-input', type='text', placeholder='Euler P column name', value=str(self.columns.get('euler_p', "")))
                            ]),
                            dbc.Col(id='euler-r-field', children=[
                                dbc.Label('Euler-r:'),
                                dbc.Input(id='euler-r-input', type='text', placeholder='Euler R column name', value=str(self.columns.get('euler_r', "")))
                            ]),
                            dbc.Col(id='state-field', children=[
                                dbc.Label('State:'),
                                dbc.Input(id='state-input', type='text', placeholder='State column name', value=str(self.columns.get('state', "")))
                            ]),
                            dbc.Col(id='timestamp-field', children=[
                                dbc.Label('Timestamp:'),
                                dbc.Input(id='timestamp-input', type='text', placeholder='Timestamp column name', value=str(self.columns.get('timestamp', "")))
                            ]),
                        ], label='Data Column Names'),
                        dbc.DropdownMenu([
                            dbc.Col([
                                dbc.Label('Draw interval (ms)'),
                                dbc.Input(id='draw-interval-input', type='number', value=self.draw_interval)
                            ]),
                        ], label='Interval'),
                    ], style={'display': 'flex', 'align-items': 'center'}),
                ]),
            ], style={'float': 'right', 'width': '20%'}),
            html.Div(id='dummy-receives', style={'display': 'none'}),
        ])], fluid=True, className='dbc dbc-ag-grid')

    def run(self):
        self.app.run()

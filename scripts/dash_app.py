from scripts.trajectory_graph import TrajectoryGraph

import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
import json
from PIL import Image


class DashApp:
    def __init__(self) -> None:
        config = json.load(open('config_path.json'))
        self.default = json.load(open(config['config-path']))
        self.source = self.default['source']
        self.updating = self.default['updating']
        self.url = self.default['url']
        self.file_path = self.default['file-path']
        self.columns = self.default['columns']
        self.data_interval = self.default['data-interval']
        self.draw_interval = self.default['draw-interval']
        self.trajectory = TrajectoryGraph()
        self.app_setup()
        print('App init')

    def app_setup(self) -> None:
        self.app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY],
                             meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1.0'}])
        self.app.title = 'CRS Trajectory Viewer'
        self.app._favicon='favicon.png'
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
                            dbc.Col(id='timestamp-field', children=[
                                dbc.Label('Timestamp:'),
                                dbc.Input(id='timestamp-input', type='text', placeholder='Timestamp column name', value=self.columns.get('timestamp', None))
                            ]),
                            dbc.Col(id='state-field', children=[
                                dbc.Label('State:'),
                                dbc.Input(id='state-input', type='text', placeholder='State column name', value=self.columns.get('state', None))
                            ]),
                            dbc.Col(id='payload-field', children=[
                                dbc.Label('Payload:'),
                                dbc.Input(id='payload-input', type='text', placeholder='Payload column name', value=self.columns.get('payload', None))
                            ]),
                            dbc.Col(id='parachute-field', children=[
                                dbc.Label('Parachute:'),
                                dbc.Input(id='parachute-input', type='text', placeholder='Parachute column name', value=self.columns.get('parachute', None))
                            ]),
                            dbc.Col(id='lon-field', children=[
                                dbc.Label('Longitude:'),
                                dbc.Input(id='lon-input', type='text', placeholder='Longitude column name', value=self.columns.get('lon', None))
                            ]),
                            dbc.Col(id='lat-field', children=[
                                dbc.Label('Latitude:'),
                                dbc.Input(id='lat-input', type='text', placeholder='Latitude column name', value=self.columns.get('lat', None))
                            ]),
                            dbc.Col(id='alt-field', children=[
                                dbc.Label('Altitude:'),
                                dbc.Input(id='alt-input', type='text', placeholder='Altitude column name', value=self.columns.get('alt', None))
                            ]),
                            dbc.Col(id='acc-x-field', children=[
                                dbc.Label('Acceleration X:'),
                                dbc.Input(id='acc-x-input', type='text', placeholder='Acceleration X column name', value=self.columns.get('acc_x', None))
                            ]),
                            dbc.Col(id='acc-y-field', children=[
                                dbc.Label('Acceleration Y:'),
                                dbc.Input(id='acc-y-input', type='text', placeholder='Acceleration Y column name', value=self.columns.get('acc_y', None))
                            ]),
                            dbc.Col(id='acc-z-field', children=[
                                dbc.Label('Acceleration Z:'),
                                dbc.Input(id='acc-z-input', type='text', placeholder='Acceleration Z column name', value=self.columns.get('acc_z', None))
                            ]),
                            dbc.Col(id='rot-x-field', children=[
                                dbc.Label('Rotation X:'),
                                dbc.Input(id='rot-x-input', type='text', placeholder='Rotation X column name', value=self.columns.get('rot_x', None))
                            ]),
                            dbc.Col(id='rot-y-field', children=[
                                dbc.Label('Rotation Y:'),
                                dbc.Input(id='rot-y-input', type='text', placeholder='Rotation Y column name', value=self.columns.get('rot_y', None))
                            ]),
                            dbc.Col(id='rot-z-field', children=[
                                dbc.Label('Rotation Z:'),
                                dbc.Input(id='rot-z-input', type='text', placeholder='Rotation Z column name', value=self.columns.get('rot_z', None))
                            ]),
                            dbc.Col(id='mag-x-field', children=[
                                dbc.Label('Magnetometer X:'),
                                dbc.Input(id='mag-x-input', type='text', placeholder='Magnetometer X column name', value=self.columns.get('mag_x', None))
                            ]),
                            dbc.Col(id='mag-y-field', children=[
                                dbc.Label('Magnetometer Y:'),
                                dbc.Input(id='mag-y-input', type='text', placeholder='Magnetometer Y column name', value=self.columns.get('mag_y', None))
                            ]),
                            dbc.Col(id='mag-z-field', children=[
                                dbc.Label('Magnetometer Z:'),
                                dbc.Input(id='mag-z-input', type='text', placeholder='Magnetometer Z column name', value=self.columns.get('mag_z', None))
                            ]),
                        ], label='Data Column Names'),
                        dbc.DropdownMenu([
                            dbc.Col([
                                dbc.Label('Draw interval (ms)'),
                                dbc.Input(id='draw-interval-input', type='number', value=self.draw_interval)
                            ]),
                            dbc.Col([
                                dbc.Label('Data interval (ms)'),
                                dbc.Input(id='data-interval-input', type='number', value=self.data_interval)
                            ]),
                        ], label='Intervals'),
                    ], style={'display': 'flex', 'align-items': 'center'}),
                ]),
            ], style={'float': 'right', 'width': '20%'}),
            html.Div(id='dummy-receives', style={'display': 'none'}),
        ])], fluid=True, className='dbc dbc-ag-grid')

    def run(self):
        self.app.run()

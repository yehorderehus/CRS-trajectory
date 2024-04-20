from scripts.app_functions import AppFunctions

import dash
from dash.dependencies import Input, Output


class DashCallbacks(AppFunctions):
    def __init__(self) -> None:
        super().__init__()

        @self.app.callback(
            Output('dummy-receives', 'children'),
            Input('lon-input', 'value'),
            Input('lat-input', 'value'),
            Input('alt-input', 'value'),
            Input('acc-x-input', 'value'),
            Input('acc-y-input', 'value'),
            Input('acc-z-input', 'value'),
            Input('rot-x-input', 'value'),
            Input('rot-y-input', 'value'),
            Input('rot-z-input', 'value'),
            Input('mag-x-input', 'value'),
            Input('mag-y-input', 'value'),
            Input('mag-z-input', 'value'),
            Input('parachute-input', 'value'),
            Input('payload-input', 'value'),
            Input('state-input', 'value'),
            Input('timestamp-input', 'value'),
            Input('url-input', 'value'),
            Input('file-input', 'value')
        )
        def update_receive_params(lon, lat, alt,
                                  acc_x, acc_y, acc_z,
                                  rot_x, rot_y, rot_z,
                                  mag_x, mag_y, mag_z,
                                  parachute, payload, state, timestamp,
                                  url, file_path) -> None:
            if url != self.url or file_path != self.file_path:
                self.clear_graph()

            self.columns = {
                'lon': lon,
                'lat': lat,
                'alt': alt,
                'acc_x': acc_x,
                'acc_y': acc_y,
                'acc_z': acc_z,
                'rot_x': rot_x,
                'rot_y': rot_y,
                'rot_z': rot_z,
                'mag_x': mag_x,
                'mag_y': mag_y,
                'mag_z': mag_z,
                'parachute': parachute,
                'payload': payload,
                'state': state,
                'timestamp': timestamp
            }
            self.url = url
            self.file_path = file_path

            self.fetcher.update_source(self.url, columns=self.columns)
            self.reader.update_source(self.file_path, columns=self.columns)
            self.reader.reset_data()

            return None

        @self.app.callback(
            Output('trajectory-graph', 'figure'),
            Input('updating-checklist', 'value'),
            Input('draw-interval-component', 'n_intervals')
        )
        def refresh_graph(updating, interval) -> dict:
            if not self.trajectory_data.empty:
                self.trajectory.update_graph(points=self.trajectory_data)
                self.init_trajectory_data()  # Clear current to avoid duplicates
            if 'updating' in updating:
                return self.trajectory.get_figure()
            return dash.no_update
            # TODO possibly: add "No data" message

        @self.app.callback(
            Output('draw-interval-component', 'interval'),
            Input('draw-interval-input', 'value')
        )
        def update_draw_interval(value) -> int:
            self.draw_interval = value
            return value

        @self.app.callback(
            Output('restart-btn', 'n_clicks'),
            Output('url-field', 'style'),
            Output('file-field', 'style'),
            Input('updating-checklist', 'value'),
            Input('data-source', 'value'),
            Input('data-interval-input', 'value'),
            Input('restart-btn', 'n_clicks')
        )
        def control_data(updating, source, interval, restart_clicks) -> tuple:
            if source != self.source or restart_clicks:
                self.clear_graph()

            self.updating = updating
            self.source = source
            self.data_interval = interval

            url_style = {'display': 'block'} if source == 'url' else {'display': 'none'}
            file_style = {'display': 'block'} if source == 'file' else {'display': 'none'}

            return 0, url_style, file_style

from scripts.app_functions import AppFunctions

import dash
from dash.dependencies import Input, Output


class DashCallbacks(AppFunctions):
    def __init__(self) -> None:
        super().__init__()

        @self.app.callback(
            Output('restart-btn', 'n_clicks'),
            Output('url-field', 'style'),
            Output('file-field', 'style'),
            Output('draw-interval-component', 'interval'),
            Input('data-source', 'value'),
            Input('updating-checklist', 'value'),
            Input('restart-btn', 'n_clicks'),
            Input('lon-input', 'value'),
            Input('lat-input', 'value'),
            Input('alt-input', 'value'),
            Input('acc-input', 'value'),
            Input('rot-input', 'value'),
            Input('euler-h-input', 'value'),
            Input('euler-p-input', 'value'),
            Input('euler-r-input', 'value'),
            Input('state-input', 'value'),
            Input('timestamp-input', 'value'),
            Input('url-input', 'value'),
            Input('file-input', 'value'),
            Input('draw-interval-input', 'value')
        )
        def update_params(source, updating, restart_clicks,
                          lon, lat, alt,
                          acc, rot, euler_h, euler_p, euler_r,
                          state, timestamp,
                          url, file_path,
                          interval) -> tuple:

            self.updating = updating

            columns = {
                'lon': lon,
                'lat': lat,
                'alt': alt,
                'acc': acc,
                'rot': rot,
                'euler_h': euler_h,
                'euler_p': euler_p,
                'euler_r': euler_r,
                'state': state,
                'timestamp': timestamp
            }

            if columns != self.columns:
                self.fetcher.update_source(self.url, self.columns)
                self.reader.update_source(self.file_path, self.columns)

            if source != self.source or restart_clicks or \
                    url != self.url or file_path != self.file_path \
                    or columns != self.columns:
                self.clear_graph()

            self.columns = columns
            self.source = source
            self.url = url
            self.file_path = file_path

            url_style = {'display': 'block'} if source == 'url' else {'display': 'none'}
            file_style = {'display': 'block'} if source == 'file' else {'display': 'none'}

            return 0, url_style, file_style, interval

        @self.app.callback(
            Output('trajectory-graph', 'figure'),
            Input('draw-interval-component', 'n_intervals')
        )
        def refresh_graph(interval) -> dict:
            if not self.trajectory_data.empty:
                self.trajectory.update_graph(points=self.trajectory_data)
                self.init_trajectory_data()  # Clear current to avoid duplicates

            if not 'updating' in self.updating:
                return dash.no_update

            return self.trajectory.figure

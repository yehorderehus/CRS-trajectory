import plotly.express as px
import pandas as pd
from PIL import Image
import threading
import time


class TrajectoryGraph:
    def __init__(self):
        self.init_figure()
        self.init_mission_image()

    def init_figure(self) -> None:
        init_data = pd.DataFrame({'DEV_X': [0], 'DEV_Y': [0], 'ALT': [0]})
        self.figure = px.scatter_3d(init_data,
                                    x='DEV_X', y='DEV_Y', z='ALT', title='Trajectory Visualization', template='plotly_dark',
                                    color='ALT', color_continuous_scale=px.colors.sequential.Plasma)
        self.figure.update_layout(scene=dict(
            xaxis_title='Deviation X (m)',
            yaxis_title='Deviation Y (m)',
            zaxis_title='Altitude (m)',
            xaxis=dict(
                tickformat='.1f',
                zeroline=False,
            ),
            yaxis=dict(
                tickformat='.1f',
                zeroline=False,
            ),
            zaxis=dict(
                tickformat='.1f',
                zeroline=False,
            ),
            aspectmode='manual',
            aspectratio=dict(x=1, y=1, z=1.5),
            camera=dict(eye=dict(x=1, y=3, z=1)),
            uirevision=True))

    def init_mission_image(self) -> None:
        self.figure.update_layout(images=[
            dict(
                source=Image.open('scripts/assets/sherpa.png'),
                xref='paper',
                yref='paper',
                x=0,
                y=1,
                sizex=0.25,
                sizey=0.25,
                layer='above',
                opacity=0.8,
                name='mission_image'
            )]
        )

    def show_new_state(self, state: int) -> None:
        self.init_mission_image()  # Use it to remove the previous state image
        self.figure.add_layout_image(
            dict(
                source=Image.open(f'scripts/assets/state_{state}.png'),
                xref='paper',
                yref='paper',
                x=0.4,
                y=1,
                sizex=0.25,
                sizey=0.25,
                layer='above',
                opacity=0.8,
            )
        )
        self.time_state_changed = time.time()
        threading.Thread(target=self.schedule_init_mission_image).start()  # mission 'update_layout(images=' will reset the state image

    def schedule_init_mission_image(self) -> None:
        delay = 2  # seconds
        time.sleep(delay)
        self.init_mission_image()

    def update_graph(self, points: pd.DataFrame) -> None:
        if points.empty:
            return

        self.figure.add_trace(px.scatter_3d(points, x='DEV_X', y='DEV_Y', z='ALT', color='ALT', color_continuous_scale=px.colors.sequential.Viridis).data[0])

    def get_figure(self) -> px.scatter_3d:
        return self.figure

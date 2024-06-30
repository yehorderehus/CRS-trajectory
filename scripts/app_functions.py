from scripts.dash_app import DashApp
from scripts.data_fetcher import DataFetcher
from scripts.data_reader import DataReader
from scripts.data_configuration import DataConfiguration

import asyncio
import pandas as pd
from typing import Union


class AppFunctions(DashApp):
    def __init__(self) -> None:
        super().__init__()

        self.state = None
        self.default_interval = 0.05  # In seconds
        self.data_interval = self.default_interval

        self.fetcher = DataFetcher()
        self.fetcher.update_source(self.url, self.columns)
        self.reader = DataReader()
        self.reader.update_source(self.file_path, self.columns)
        self.configuration = DataConfiguration()

        self.init_trajectory_data()

    def init_trajectory_data(self):
        self.trajectory_data = pd.DataFrame(columns=['DEV_X', 'DEV_Y', 'ALT'])

    def manage_data(self, new_data: Union[pd.DataFrame, None]) -> None:
        last_data = None

        if new_data is not None:
            if last_data is None or last_data is not None and not new_data.equals(last_data):
                print(new_data)

                state, interval, trajectory_data = self.configuration.configure_data(new_data)
                if state != self.state and state is not None:
                    self.trajectory.show_state(state)
                self.state = state
                if interval is not None:
                    self.data_interval = interval
                    print(f'Data interval is {self.data_interval:.2f} seconds.')
                else:
                    self.data_interval = self.default_interval
                    print(f'Data interval is the default {self.data_interval:.2f} seconds.')

                if trajectory_data is not None:
                    frames = [frame for frame in [self.trajectory_data, trajectory_data] if not frame.empty]
                    if frames:
                        self.trajectory_data = pd.concat(frames)

            last_data = new_data

    async def get_data_asynchronously(self) -> None:
        while True:
            if 'updating' in self.updating:
                if self.source == 'url':
                    new_data = await self.fetcher.fetch_data()
                if self.source == 'file':
                    new_data = await self.reader.read_data()

                self.manage_data(new_data)

                await asyncio.sleep(self.data_interval)

    def clear_graph(self) -> None:
        if self.source == 'file':
            self.reader.init_readed()
        self.configuration.init_data_trackers()
        self.init_trajectory_data()
        self.trajectory.init_figure()
        self.trajectory.init_images()

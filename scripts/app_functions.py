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
        self.fetcher = DataFetcher()
        self.fetcher.update_source(self.url, self.columns)
        self.reader = DataReader()
        self.reader.update_source(self.file_path, self.columns)
        self.configuration = DataConfiguration()

        self.init_trajectory_data()
        self.init_state()

    def init_trajectory_data(self):
        self.trajectory_data = pd.DataFrame(columns=['DEV_X', 'DEV_Y', 'ALT'])

    def init_state(self):
        self.state = None

    def manage_state(self, new_data: pd.DataFrame) -> None:
        state = int(new_data['state'].iloc[0])
        if state != self.state:
            self.trajectory.show_new_state(state)
        self.state = state

    def manage_data(self, new_data: Union[pd.DataFrame, None]) -> None:
        last_data = None
        if new_data is not None:
            if last_data is None or last_data is not None and not new_data.equals(last_data):
                self.manage_state(new_data)
                print(new_data)  # If needed
                trajectory_data = self.configuration.configure_data(new_data)
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

                if self.data_interval > 0 and isinstance(self.data_interval, int):
                    await asyncio.sleep(self.data_interval / 1000)
                else:
                    await asyncio.sleep(1)

    def clear_graph(self) -> None:
        if self.source == 'file':
            self.reader.reset_data()
        self.configuration.init_data_trackers()
        self.init_trajectory_data()
        self.init_state()
        self.trajectory.init_figure()

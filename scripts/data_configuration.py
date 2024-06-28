from scripts.logging_config import logger

import pandas as pd
from typing import Union
from geopy.distance import geodesic


class DataConfiguration:
    def __init__(self) -> None:
        self.required_cols = ['lon', 'lat', 'alt', 'state', 'timestamp']
        self.init_data_trackers()

    def init_data_trackers(self) -> None:
        self.timestamp = None
        self.init_lon = None
        self.init_lat = None

    def configure_data(self, data: pd.DataFrame) -> Union[float, float, pd.DataFrame]:
        if not isinstance(data, pd.DataFrame) or data.empty or data.shape[0] > 1:
            logger.error('DataConfiguration: "data" must be a non-empty DataFrame with only one row.')
            return None, None, None

        if not all(
            col in data.columns and
            data[col].iloc[0] and
            not (data[col].iloc[0] == 0)
            for col in self.required_cols
        ):
            logger.error('DataConfiguration: "data" must contain all required columns with non-zero values.')
            return None, None, None

        data_copy = data[self.required_cols].copy()

        timestamp = data_copy['timestamp'].iloc[0]
        if self.timestamp is not None and 0 < timestamp - self.timestamp <= 60000:
            data_interval = (timestamp - self.timestamp) / 1000
        else:
            data_interval = None
        self.timestamp = timestamp

        state = data_copy['state'].iloc[0]
        if not 0 <= state <= 9:
            logger.error('DataConfiguration: "state" must be a number between 0 and 9.')
            return None, data_interval, None

        if state not in [4, 5, 6, 7, 9]:
            # No need for an error here
            return state, data_interval, None

        if not self.init_lon or not self.init_lat:
            self.init_lon = data_copy['lon'].iloc[0]
            self.init_lat = data_copy['lat'].iloc[0]

        data_copy['dev_x'] = geodesic((self.init_lat, 0), (data_copy['lat'].iloc[0], 0)).meters
        data_copy['dev_y'] = geodesic((0, self.init_lon), (0, data_copy['lon'].iloc[0])).meters

        configured_data = pd.DataFrame()
        configured_data.loc[0, 'DEV_X'] = data_copy['dev_x'].iloc[0]
        configured_data.loc[0, 'DEV_Y'] = data_copy['dev_y'].iloc[0]
        configured_data.loc[0, 'ALT'] = data_copy['alt'].iloc[0]

        return state, data_interval, configured_data

import pandas as pd
from typing import Union
from geopy.distance import geodesic
import random


class DataConfiguration:
    def __init__(self) -> None:
        self.required_set_gps = ['lon', 'lat', 'alt', 'state']
        self.required_set_SIM = ['alt', 'state', 'timestamp']

        self.init_data_trackers()

    def init_data_trackers(self) -> None:
        self.init_lon = None
        self.init_lat = None

        self.last_timestamp = None
        self.last_dev_x = 0
        self.last_dev_y = 0

    def configure_data(self, data: pd.DataFrame) -> Union[pd.DataFrame, None]:
        if data is None and data.shape[0] > 1:
            print('DataConfiguration wrong parameter')
            # Do not change, tested
            return None

        points = pd.DataFrame()

        def alt_check(ext_data: pd.DataFrame) -> bool:
            return ext_data['alt'].iloc[0] >= 0

        def state_check(ext_data: pd.DataFrame) -> bool:
            return ext_data['state'].iloc[0] in [3, 4, 5]

        def update_points(ext_data: pd.DataFrame) -> None:
            points.loc[0, 'DEV_X'] = ext_data['dev_x'].iloc[0]
            points.loc[0, 'DEV_Y'] = ext_data['dev_y'].iloc[0]
            points.loc[0, 'ALT'] = ext_data['alt'].iloc[0]

        if all(
            col in data.columns and
            data[col].iloc[0] and
            not (data[col].iloc[0] == 0) and not (data[col].iloc[0] == '0')
            for col in self.required_set_gps
        ):
            scenario_data = data[self.required_set_gps].copy()
            scenario_data = scenario_data.apply(pd.to_numeric, errors='coerce')

            if not alt_check(scenario_data):
                return None
            if not state_check(scenario_data):
                return None

            if not self.init_lon or not self.init_lat:
                self.init_lon = scenario_data['lon'].iloc[0]
                self.init_lat = scenario_data['lat'].iloc[0]

            scenario_data['dev_x'] = geodesic((self.init_lat, 0), (scenario_data['lat'].iloc[0], 0)).meters
            scenario_data['dev_y'] = geodesic((0, self.init_lon), (0, scenario_data['lon'].iloc[0])).meters

            update_points(scenario_data)

        elif all(  # TODO use Calman filter ? , write the algorithm
            col in data.columns and
            data[col].iloc[0] and
            not (data[col].iloc[0] == 0) and not (data[col].iloc[0] == '0')
            for col in self.required_set_SIM
        ):
            scenario_data = data[self.required_set_SIM].copy()
            scenario_data = scenario_data.apply(pd.to_numeric, errors='coerce')

            if not alt_check(scenario_data):
                self.last_timestamp = scenario_data['timestamp'].iloc[0]
                return None
            if not state_check(scenario_data):
                self.last_timestamp = scenario_data['timestamp'].iloc[0]
                return None

            if not self.last_timestamp or scenario_data['timestamp'].iloc[0] < self.last_timestamp:
                self.last_timestamp = scenario_data['timestamp'].iloc[0]
                return None

            def generate_coeffs():
                # Simulation SIM coefficients (deviation in meters per second)
                X_3 = random.uniform(2.1, 2.4)
                Y_3 = random.uniform(0.4, 0.7)
                X_4 = random.uniform(0.7, 0.9)
                Y_4 = random.uniform(0.1, 0.3)
                X_5 = random.uniform(0.3, 0.4)
                Y_5 = random.uniform(0.04, 0.1)

                return X_3, Y_3, X_4, Y_4, X_5, Y_5

            X_3, Y_3, X_4, Y_4, X_5, Y_5 = generate_coeffs()

            state_mapping = {
                3: (X_3, Y_3),
                4: (X_4, Y_4),
                5: (X_5, Y_5)
            }

            X, Y = state_mapping[scenario_data['state'].iloc[0]]

            scenario_data['dev_x'] = self.last_dev_x + X * (scenario_data['timestamp'].iloc[0] - self.last_timestamp)
            scenario_data['dev_y'] = self.last_dev_y + Y * (scenario_data['timestamp'].iloc[0] - self.last_timestamp)

            self.last_timestamp = scenario_data['timestamp'].iloc[0]
            self.last_dev_x = scenario_data['dev_x'].iloc[0]
            self.last_dev_y = scenario_data['dev_y'].iloc[0]

            update_points(scenario_data)

        if points.empty:
            return None

        return points

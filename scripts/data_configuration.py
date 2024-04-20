import pandas as pd
from typing import Union
from geopy.distance import geodesic


class DataConfiguration:
    def __init__(self) -> None:
        self.required_set_gps = ['lon', 'lat', 'alt', 'state']
        self.required_set_acc_alt = ['alt', 'state', 'timestamp', 'acc_x', 'acc_y', 'rot_x', 'rot_y', 'rot_z']

        self.init_data_trackers()

    def init_data_trackers(self) -> None:
        self.init_lon = None
        self.init_lat = None

        self.last_timestamp = None  # For further use in acc_alt algorithm

    def configure_data(self, data: pd.DataFrame) -> Union[pd.DataFrame, None]:
        if data is None and data.shape[0] > 1:
            print('DataConfiguration wrong parameter')
            return None

        points = pd.DataFrame()

        def alt_check(ext_data: pd.DataFrame) -> None:
            if ext_data['alt'].iloc[0] < 0:
                return None

        def state_check(ext_data: pd.DataFrame) -> None:
            if ext_data['state'].iloc[0] not in [3, 4, 5]:
                return None

        def update_points(ext_data: pd.DataFrame) -> None:
            points.loc[0, 'DEV_X'] = geodesic((self.init_lat, 0), (ext_data['lat'].iloc[0], 0)).meters
            points.loc[0, 'DEV_Y'] = geodesic((0, self.init_lon), (0, ext_data['lon'].iloc[0])).meters
            points.loc[0, 'ALT'] = ext_data['alt'].iloc[0]

        if all(
            col in data.columns and
            data[col].iloc[0] and
            not (data[col].iloc[0] == 0) and not (data[col].iloc[0] == '0')
            for col in self.required_set_gps
        ):
            gps_data = data[self.required_set_gps].copy()
            gps_data = gps_data.apply(pd.to_numeric, errors='coerce')

            alt_check(gps_data)
            state_check(gps_data)

            if not self.init_lon or not self.init_lat:
                self.init_lon = gps_data['lon'].iloc[0]
                self.init_lat = gps_data['lat'].iloc[0]

            update_points(gps_data)

            if data['timestamp'].iloc[0]:
                self.last_timestamp = data['timestamp'].iloc[0]

        elif all(  # TODO use Calman filter ? , write the algorithm
            col in data.columns and
            not data[col].iloc[0] and
            not (data[col].iloc[0] == 0) or (data[col].iloc[0] == '0')
            for col in self.required_set_acc_alt
        ):
            acc_alt_data = data[self.required_set_acc_alt].copy()
            acc_alt_data = acc_alt_data.apply(pd.to_numeric, errors='coerce')

            alt_check(acc_alt_data)
            state_check(acc_alt_data)

            # Write...

        if points.empty:
            return None

        return points


"""The missile knows where it is at all times.
It knows this because it knows where it isn't.
By subtracting where it is from where it isn't,
Or where it isn't from where it is (whichever is
Greater), it obtains a difference, or deviation.
The guidance subsystem uses deviations to generate corrective
Commands to drive the missile from a position where it is to a
Position where it isn't,
And arriving at a position where it wasn't, it now is.
Consequently, the position where it is,
Is now the position that it wasn't,
And it follows that the position that
It was, is now the position that it isn't.
In the event that the position that it is in is not the position that
It wasn't, the system has acquired a variation,
The variation being the difference between
Where the missile is, and where it wasn't.
If variation is considered to be a
Significant factor, it too may be corrected by the GEA.
However, the missile must also know where it was.
The missile guidance computer scenario works as follows.
Because a variation has modified some of the information
The missile has obtained, it is not sure just where it is.
However, it is sure where it isn't,
Within reason, and it knows where it was.
It now subtracts where it should be from where it wasn't,
Or vice-versa, and by differentiating this from the algebraic sum of
Where it shouldn't be, and where it was,
It is able to obtain the deviation
And its variation, which is called error."""

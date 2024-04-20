# Please note
Currently it is in development, so there is missing accuracy and no clear instructions / data and features to show. The main purpose of this code is to demonstrate it.

## Notes How to use
- This program is made for visualizing paths from Czech Rocket Society's rocket flights. Configuration stays up to date with the latest flight parameters
- ***data_configuration*** is the main file for setting up the trajectory points calculation. Check it before every new flight!
- Set Data interval to 1 ms for real-time data retrieval, other values make sense for simulating delayed data retrieval from file
- Set Draw interval based on your preferences for the graph update (default 100 ms)
- Working efficiency is around 10 Hz for both data retrieval and drawing
- Unchecked "Updating" pauses the data retrieval and figure update
- Do not put a lot of data; the best approach is to use data from start to land
- Program works with two sets of data columns:
    - 1. Using **GPS**: latitude, longitude, altitude, state, timestamp (optional, not in use yet)
    - 2. Calculating position via **Acc-Alt**: *will be implemented in the future*
- *data/example_dict.json* and *data/example_list.json* are the examples of how the JSON fromat should look like
- ***data*** folder may contain rocket flight data in JSON (list of dicts or single dict) and CSV format
- ***configs*** folder may contain config files for the program
- In ***config_path.json*** you have to set the path to the config file which will be used for the program (default values for input fields)**
- For environment setup and running the program see [use.md](use.md)
- For bugs and development see [dev.md](dev.md)

### Input columns format, every can be *int* or *float* or *string*
- **Latitude**, range -90 to 90
- **Longitude**, range -180 to 180
- **Altitude**, number in meters
- **State**, from 0 to 8
- Optional: **Timestamp**, in time format

Further columns may be implemented.
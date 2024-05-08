<img src="scripts\assets\crs_logo.png" alt="CRS Logo" style="height: 120px;">

# Notes How to use
**This program is designed to visualize paths from the Czech Rocket Society's rocket flights.**

## Configuration
- **scripts/data_configuration** is the primary file for setting up trajectory point calculation. Ensure it stays updated with the latest flight parameters.
- **configs** folder contains configs with predefined parameters for each rocket flight.
- In **config_path.json** set the path to the config file which will be used.

## Data
- From the **server** the program can fetch data in **JSON** format.
- **data** folder contains rocket flight data. File-read data can be either in **JSON** or **CSV** format.
- Avoid using a lot of data; the best approach is to utilize data from start to landing.

## Addition to the data
- **2023_finals_1 uses actual GPS data but states from that time have changed, so it ends midflight.**
- **2024_demo1** uses actual altitude data but simulated deviation.

## Intervals
- Set **Data interval** to 1 ms for real-time data retrieval. Other values make sense for simulating delayed data retrieval from a file.
- Adjust **Draw interval** based on your preferences for the figure update speed (default is 100 ms).

## General
- Working efficiency is around 10 Hz for both data retrieval and figure updates.
- Unchecked "Updating" pauses the data retrieval and figure updates.
- *write_data* in **scripts/data_fetcher.py** writes fetched data into the file. You can comment out ***await self.write_data()*** if you don't want to save the data.
- ***print(new_data)*** in **scripts/app_functions.py** prints every new data and also can be commented out.

## Input columns format
Each column can be *int* or *float* or *string*

- **Latitude**: Range -90 to 90.
- **Longitude**: Range -180 to 180.
- **Altitude**: Number in meters.
- **State**: Values from 0 to 8.
- **Timestamp**: Time format.

Altitude and state are mandatory, followed by longitude and latitude or timestamp. If no GPS data is available, deviation is poorly simulated. Other input columns are not in use.

## Reads
- For environment setup and running the program, refer to [setup.md](setup.md).
- For bugs and development see [dev.md](dev.md).

## Preview
<img src="scripts\assets\preview.png" alt="Preview Screenshot">
<img src="scripts\assets\crs_logo.png" alt="CRS Logo" style="height: 120px;">

# Notes How to use
**This program is used to visualize the flight trajectories of the Czech Rocket Society's rockets**.

**You can start by running the program and seeing the rocket's trajectory from the 2024 finale flight.**

## Configuration
- [config_path.json](configs/config_path.json) contains the path to the config file which will be used.
- [configs](configs) folder contains configs with predefined parameters for each flight with next naming convention:
    - **source**: str **"url"** *or* **"file"**
    - **updating**: str **"updating"** *or* **""**
    - **url**: str
    - **file-path**: str
    - **draw-interval**: int *(in ms)*
    - **columns**: str *(in case of nested data, use dot notation)*

## Data
- The program can fetch data from the server in **JSON** format.
- Data in the file can be either in **JSON** or **CSV** format.
- JSON has to be **list of dicts** in case of reading from the file and **dict** in case of fetching from the server.
- [2024_finale_public.csv](data/2024_finale_public.csv) is an example, some of the information in it has been modified.

## Input columns format
Each column can be *int* or *float* or *string*. Acceleration, Rotation and Euler coefs are currently not in use.
- **Latitude**: Range -90 to 90.
- **Longitude**: Range -180 to 180.
- **Altitude**: Number in meters.
- **Acceleration**: Number in m/s^2.
- **Rotation**: Number in degrees.
- **Euler h, Euler p, Euler r**: Numbers in degrees.
- **State**: Number from 0 to 9.
- **Timestamp**: Time format.

## Links
- For environment setup and running the program, refer to [setup.md](setup.md).
- For bugs and development see [dev.md](dev.md).

## Preview
<img src="scripts\assets\preview.png" alt="Preview Screenshot">

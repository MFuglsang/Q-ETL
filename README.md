# Q-ETL 

A Python framework to create ETL processes using QGIS as the engine.

## Basic example

This is an example of how to load an input file, reproject the data to WGS84 (EPSG:4326) and write the output to a GeoJSON file.  

```python
reader = Input_Reader
layer = reader.geojson("testdata/kommuner.geojson")

worker = Worker
reprojectedLayer = worker.reproject(layer, "EPSG:4326")

writer = Output_writer
writer.file(reprojectedLayer, "C:/temp/kommuner_4326.geojson", "GeoJson")
```

To run the job, simply call the <YourProject>.cmd file (as described in [Step 3](https://github.com/MFuglsang/QGIS_ETL/wiki/Getting-started#step-3---the-python-project-file) and [Step 4](https://github.com/MFuglsang/QGIS_ETL/wiki/Getting-started#step-4---the-project-cmd-file) in the [_Getting started_](https://github.com/MFuglsang/QGIS_ETL/wiki/Getting-started) guide), and the job will execute. The translation log is placed in the log directory as specified in the configuration

## Quickstart
Checkout the _Getting started_ guide on the Wiki page [here](https://github.com/MFuglsang/Q-ETL/wiki/Getting-started).

## Download
Download the latest release [here](https://github.com/MFuglsang/Q-ETL/releases).

If you want to contact the Q-ETL team, feel free to open a discussion or an issue.

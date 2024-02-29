![Demo Animation](../ressources/images/logo.png?raw=true)
## - ETL build on the QGIS Engine, using python.
 
## Requirements 
This concept requires a QGIS installation on the computer that executes the jobs.
It requires the file python-qgis.bat, which normally can be
located in one of these folders :

**_<OSGeo4W_ROOT>\bin_** or **_<QGIS_ROOT>\bin_**

If you are usig a dev- or ltr version, the filename is different eg: _python-qgis-ltr.bat_

## Initial configurataion

In order to configure the application, a few steps is required.

In the root of the project, settings_template.json must be copied to settings.json and filled out.
Needed configuration elements :

Qgs_PrefixPath : The folder where QGIS is installed.\
QGIS_Plugin_Path : The QGIS pligin folder.\
Logdir : A folder for storing logfiles generated by jobs.\
TempFolder : A folder for temporary data generated by jobs.\

Furthermore, database connections can be esatblished here. The connections are named, so multiple connections can co-exist.
When a job starts, the configuration is validatet - if elments are missing/incorrect, the job will fail.

After the configuration is set up, the first job can be created.
Here, two boilerplate files are required : 

    * boilerplate.cmd in the root folder
    * boilerplate.py in the python folder.

Make a copy of these two files, and rename them to <YourProject> .cmd/.py

Open the <YourProject>.cmd file. Modify both the path to the QGIS python instance, and the path for the <YourProject>.py file.

Now, open the <YourProject>.py file. There is not much in it but two imports. The rest is hidden behind the scenes.

## Basic example

A simple example model loading an input file, reprojection it to 4326, and writing the output looks like :
```
reader = Input_Reader
layer = reader.geojson("testdata/kommuner.geojson")

worker = Worker
reprojectedLayer = worker.reproject(layer, "EPSG:4326")

writer = Output_writer
writer.file(reprojectedLayer, "C:/temp/kommuner_4326.geojson", "GeoJson")
```

To run the job, simply call the <YourProject>.cmd file, and the job will execute. The translation log is placed in the log directory as specified in the configuration


## Running jobs

When the ETL job is ready, all that is required is to run the <YourProject>.cmd file.
While the job runs, a log file is created for the job run - in the log folder specified in the configuration.py file.



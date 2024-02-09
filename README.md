# QGIS as ETL tool using Python
 
## Requirements 
This concept requires a QGIS installation on the computer that executes the jobs.
It requires the file python-qgis.bat, which normally can be
located in one of these folders :

**_<OSGeo4W_ROOT>\bin_** or **_<QGIS_ROOT>\bin_**

If you are usig a dev- or ltr version, the filename is different eg: _python-qgis-ltr.bat_

## Initial configurataion

In order to configure the application, a few steps is required.

in python/config/configuration.py, the different parameters for the jobs can be configured - database connections, QGIS locations etc.
This config is shared between all jobs, but multiple name connections to database can exist at the same time.
When a job starts, the configuration is validatet - if elments are missing/incorrect, the job will fail.

After the configuration is set up, the first job can be created.
Here, two boilerplate files are required : 

    * boilerplate.cmd in the root folder
    * biolerplate.py in the python folder.

Make a copy of these two files, and rename them to <YourProject> .cmd/.py

Open the <YourProject>.cmd file. Modify both the path to the QGIS python instance, and the path for the <YourProject>.py file.

Now, open the <YourProject>.py file. Most of this is boilerplate, that should be left intact. Navigate to the 'SCRIPT PART' section - here your python code for your model resides.

A simple example model loading an input file, reprojection it to 4326, and writing the output looks like :
```
layer = readGeojson("testdata/kommuner.geojson", settings)
reprojectedLayer = reprojectV2(layer, "EPSG:4326", settings)
writeOutputfile(wfslayer, "C:/temp/kommuner_4326.geojson", "GeoJson", settings)
```

To run the job, simply call the <YourProject>.cmd file, and the job will execute. The translation log is placed in the log directory as specified in the configuration


## Boilerplates





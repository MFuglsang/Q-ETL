from qgis.core import QgsApplication

QgsApplication.setPrefixPath("<PATH TO QGIS FOLDER>", True)
qgs = QgsApplication([], False)
qgs.initQgis()

## Loading stuff on the running QGIS...
sys.path.append("python/transformers")
sys.path.append("python/readers")
sys.path.append("python/writers")
from geometry import reproject
from inputreaders import readShapefile
from outputwriters import writeShapefile

## Code goes here...

qgs.exitQgis()



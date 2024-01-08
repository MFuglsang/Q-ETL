from qgis.core import QgsVectorFileWriter
print("Outputwriters imported")

def writeOutputfile(layer, path, format):
    QgsVectorFileWriter.writeAsVectorFormat(layer, path, "utf-8", layer.crs(), format)
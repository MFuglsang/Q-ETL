# **GENERAL WORKERS** 

## **renameTableField**

## **fieldCalculator**

## **deleteColumns**

## **addAutoIncrementalField**

## **extractByExpression**
**QGIS processing algorithem : native:extractbyexpression **

Parameters for transformer: \
    1. Input layer,  Type:[vector: any] (reference to a Qgsvectorlayer. The layer must already be loaded into the script.)\
    2. Expression, Type:[expression] (Text string as created in the expression builder in QGIS.)\

Example usage:\
```
outputLayer = extractByExpression(layer=inputLayer, expression='$area > 1000000', settings=settings)

```
Link to QGIS documentation:  https://docs.qgis.org/en/docs/user_manual/processing_algs/qgis/vectorselection.html#id29







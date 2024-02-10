# **GENERAL WORKERS** 

## **renameTableField**

## **fieldCalculator**

## **deleteColumns**

## **addAutoIncrementalField**
**QGIS processing algorithem : native:addautoincrementalfield **

Adds a new integer field to a vector layer, with a sequential value for each feature.\
This field can be used as a unique ID for features in the layer. The new attribute is not added to the input layer but a new layer is generated instead.\

The initial starting value for the incremental series can be specified.\

Parameters for worker: \
    1. Input layer,  Type:[vector: any] (reference to a Qgsvectorlayer. The layer must already be loaded into the script.)\
    2. Fieldname, Type:[text]\
    3. Start Type:[integer] (The start value for the incremental field)

Example usage:\
```
outputLayer = addAutoIncrementalField(layer=inputLayer, fieldname='fid', start=1 settings=settings)

```
Link to QGIS documentation:  https://docs.qgis.org/3.28/en/docs/user_manual/processing_algs/qgis/vectortable.html#id38


## **extractByExpression**
**QGIS processing algorithem : native:extractbyexpression **

Creates a selection in a vector layer.\
The criteria for selecting features is based on a QGIS expression. For more information about expressions see https://docs.qgis.org/3.28/en/docs/user_manual/expressions/expression.html#id5 \

Parameters for worker: \
    1. Input layer,  Type:[vector: any] (reference to a Qgsvectorlayer. The layer must already be loaded into the script.)\
    2. Expression, Type:[expression] (Text string as created in the expression builder in QGIS.)\

Example usage:\
```
outputLayer = extractByExpression(layer=inputLayer, expression='$area > 1000000', settings=settings)

```
Link to QGIS documentation:  https://docs.qgis.org/en/docs/user_manual/processing_algs/qgis/vectorselection.html#id29







# **ATTRIBUTE WORKERS** 

## **renameTableField**
**QGIS processing algorithem : native:renametablefield **

Renames an existing field from a vector layer.

The original layer is not modified. A new layer is generated where the attribute table contains the renamed field.

Parameters for worker: \
    1. Input layer,  Type:[vector: any] (reference to a Qgsvectorlayer. The layer must already be loaded into the script.)\
    2. field, Type:[tablefield: any]\
    3. newname, Type:[text]\

Example usage:
```
outputLayer = general.addAutoIncrementalField(layer=inputLayer, field'fid', newname='ogc_fid' settings=settings)
```
Link to QGIS documentation:  https://docs.qgis.org/3.28/en/docs/user_manual/processing_algs/qgis/vectortable.html#id48


## **fieldCalculator**

**QGIS processing algorithem : native:fieldcalculator **

Scripting the field calcualtor (see [Expressions](https://docs.qgis.org/3.28/en/docs/user_manual/expressions/expression.html#id5)). You can use all the supported expressions and functions.

A new layer is created with the result of the field calculator.

Parameters for worker: \
    1. Input layer,  Type:[vector: any] (reference to a Qgsvectorlayer. The layer must already be loaded into the script.)\
    2. fieldname, Type:[string]\
    3. fieldtype, Type:[enumeration] (Default: 0) 0 — Float, 1 — Integer, 2 — String, 3 — Date \
    4. fieldlength, Type:[number] (Default: 10)
    5. fieldprecision, Type:[number] (Default: 3) 
    6. formula, Type:[expression]

Example usage:
```
outputLayer = general.fieldcalculator(layer=inputlayer, fieldname='value', fieldtype=1 , fieldlength=10, fieldprecision=3, formula ='fid + 1', settings=settings)
```
Link to QGIS documentation: https://docs.qgis.org/3.28/en/docs/user_manual/processing_algs/qgis/vectortable.html#id46 


## **deleteColumns**

**QGIS processing algorithem : native:deletecolumn **

Takes a vector layer and generates a new one that has the same features but without the selected columns.

Parameters for worker: \
    1. Input layer,  Type:[vector: any] (reference to a Qgsvectorlayer. The layer must already be loaded into the script.)\
    2. Columns, Type:[tablefield: any] [list]\

Example usage:
```
outputLayer = general.addAutoIncrementalField(layer=inputLayer, columns=['fid', 'ogc_fid'], settings=settings)
```
Link to QGIS documentation:  https://docs.qgis.org/3.28/en/docs/user_manual/processing_algs/qgis/vectortable.html#id43


## **addAutoIncrementalField**
**QGIS processing algorithem : native:addautoincrementalfield **

Adds a new integer field to a vector layer, with a sequential value for each feature.\
This field can be used as a unique ID for features in the layer. The new attribute is not added to the input layer but a new layer is generated instead.

The initial starting value for the incremental series can be specified.

Parameters for worker: \
    1. Input layer,  Type:[vector: any] (reference to a Qgsvectorlayer. The layer must already be loaded into the script.)\
    2. Fieldname, Type:[text]\
    3. Start Type:[integer] (The start value for the incremental field)

Example usage:
```
outputLayer = general.addAutoIncrementalField(layer=inputLayer, fieldname='fid', start=1, settings=settings
```
Link to QGIS documentation:  https://docs.qgis.org/3.28/en/docs/user_manual/processing_algs/qgis/vectortable.html#id38


## **extractByExpression**
**QGIS processing algorithem : native:extractbyexpression **

Creates a selection in a vector layer.\
The criteria for selecting features is based on a QGIS expression. For more information about expressions see https://docs.qgis.org/3.28/en/docs/user_manual/expressions/expression.html#id5 

Parameters for worker: \
    1. Input layer,  Type:[vector: any] (reference to a Qgsvectorlayer. The layer must already be loaded into the script.)\
    2. Expression, Type:[expression] (Text string as created in the expression builder in QGIS.)

Example usage:
```
outputLayer = general.extractByExpression(layer=inputLayer, expression='$area > 1000000', settings=settings)
```
Link to QGIS documentation:  https://docs.qgis.org/en/docs/user_manual/processing_algs/qgis/vectorselection.html#id29







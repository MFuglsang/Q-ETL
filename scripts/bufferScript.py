"""
Model exported as python.
Name : BufferModel
Group : 
With QGIS : 33401
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterNumber
from qgis.core import QgsProcessingParameterVectorLayer
from qgis.core import QgsProcessingParameterFeatureSink
import processing


class Buffermodel(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        self.addParameter(QgsProcessingParameterNumber('bufferdist', 'BufferDist', type=QgsProcessingParameterNumber.Integer, minValue=0, defaultValue=100))
        self.addParameter(QgsProcessingParameterVectorLayer('input', 'Input', defaultValue=None))
        self.addParameter(QgsProcessingParameterFeatureSink('Output', 'Output', type=QgsProcessing.TypeVectorPolygon, createByDefault=True, supportsAppend=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(1, model_feedback)
        results = {}
        outputs = {}

        # Buffer
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': parameters['bufferdist'],
            'END_CAP_STYLE': 0,  # Rund
            'INPUT': parameters['input'],
            'JOIN_STYLE': 0,  # Rund
            'MITER_LIMIT': 2,
            'SEGMENTS': 4,
            'OUTPUT': parameters['Output']
        }
        outputs['Buffer'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Output'] = outputs['Buffer']['OUTPUT']
        return results

    def name(self):
        return 'BufferModel'

    def displayName(self):
        return 'BufferModel'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Buffermodel()

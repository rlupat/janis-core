import argparse

import os
import logging
import json
import uuid
import sys
import atexit
from signal import *
import time
import yaml
from cerberus import Validator
import json
from pprint import pprint

from pipeline_definition.types.schema import schema

from pipeline_definition.types.type_registry import get_input_factory
from pipeline_definition.types.type_registry import get_step_factory

from pipeline_definition.types.input_type import InputFactory

class PdxException(Exception):
    pass

class PDX:

    def __dumpYaml(self, doc ):
        # Diagnostic - what have we got?
        print("YAML DOC [\n")
        print(yaml.dump(doc))
        print("\n] END YAML DOC \n")

    def __dumpSchema(self, schema ):
        print("PDX SCHEMA [\n")
        #print(schema)
        print(json.dumps(schema, indent=4))
        print("\n] END PDX SCHEMA\n")


    def validateSchema(self, yamlDoc ):
        self.__dumpYaml( yamlDoc )

        sch = schema()
        self.__dumpSchema( sch )

        v = Validator(sch)

        validationSuccess = v.validate(yamlDoc)

        if not validationSuccess:
            msg = "ERROR! Pipeline definition document validation failed."
            print( msg )
            if v.errors is not None:
                raise ValueError( msg, v.errors )


    def buildInputs(self, inputs ):

        inputSet = list()

        for id, meta in inputs.items():
            inputType = next(iter(meta.keys()))
            inputMeta = next(iter(meta.values()))
            print("Processing INPUT: ",id, " - ", inputType)

            inpFactory = get_input_factory( inputType )
            if ( inpFactory is None ):
                raise ValueError("No factory registered for input: " + inputType )

            inputObj = inpFactory.buildFrom( dict([ (id,meta) ]) )

            inputSet.append(inputObj)

            print("\n")

        return inputSet

    def buildOutputs(self, outputs ):
        return None

    def buildSteps(self, steps):

        pipelineSteps = list()

        for step in steps:
            id = None
            stepType = None
            stepMeta = None


            if ( isinstance( step, str) ):
                id = step
                stepType = id
                stepMeta = dict([('type', id)])
            elif ( isinstance( step, dict) ):
                tMeta = next( iter(step.values()) )
                typeMeta = tMeta.get("type")
                if typeMeta is None:
                    id = next( iter(step.keys()) )
                    stepType = id
                    stepMeta = dict([('type', step)])
                else:
                    id = next(iter(step.keys()))
                    stepType = next( iter(typeMeta.keys()) )
                    stepMeta = tMeta

            print("Processing STEP: ",id, " - ", stepType)

            stepFactory = get_step_factory( stepType )
            if ( stepFactory is None ):
                 raise ValueError("No factory registered for step: " + stepType )

            stepObj = stepFactory.buildFrom( dict([ (id, stepMeta) ]) )

            pipelineSteps.append( stepObj )

            print("\n")

        return pipelineSteps

    def translatePipeline( self, pipelineSteps, globalInputSet, globalOutputSet ):


        #create a graph of steps in pipeline
        #every step has a context available to it


        return "TX DOC"


    def translateYamlDoc(self, yamlDoc):

        #Create a in memory instances for all the inputs, steps and outputs

        inputs = yamlDoc.get("inputs")
        steps = yamlDoc.get("steps")
        outputs = yamlDoc.get("outputs")

        if inputs is None:
            raise ValueError("No input?")

        if outputs is None:
            #raise ValueError("No output?")
            pass

        globalInputSet = self.buildInputs(inputs)
        globalOutputSet = self.buildOutputs(outputs)
        pipelineSteps = self.buildSteps(steps )

        #Now translate the workflow steps
        txDoc = self.translatePipeline( pipelineSteps, globalInputSet, globalOutputSet )

        return txDoc

    def translate(self, pdfile, outfile=None, overwriteOutfile=False ):
        pdfilePath = os.path.abspath(pdfile)
        print("Using PD file: " + pdfilePath)

        #Check if the file to translate exists
        if not os.path.isfile(pdfilePath):
            raise ValueError("PD file does not exists.")

        #The output file name, if not explicitly specified, a convention is used
        if outfile is None:
            outfile = pdfile + ".pdx"
        outfilePath = os.path.abspath(outfile)
        print("Using Output file: " + outfilePath)

        #If the output file path already exists as directory?
        if os.path.isdir(outfilePath):
            raise ValueError("Directoiry already exists with the name of outfile.")

        #Otherwise can we overwrite?
        if overwriteOutfile is False:
            if os.path.isfile(outfilePath) :
                raise ValueError("Outfile already exists.")

        #All good so lets starts the translation
        with open(pdfile, 'r') as ifile:
            # Validate YAML syntax
            doc = yaml.load(ifile)

            # Do schema validation
            self.validateSchema( doc )

            #Doc is OK, lets translate
            tDoc = self.translateYamlDoc( doc )
            print("Output: ", tDoc)

            # Save it
            with open( outfilePath, "w" ) as ofile:
                ofile.write( tDoc )


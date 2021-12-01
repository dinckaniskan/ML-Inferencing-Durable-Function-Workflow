"""
"""

import logging
import json

import azure.functions as func
import azure.durable_functions as df

def geocode_orchestrator_function(context: df.DurableOrchestrationContext):
    input_data = context.get_input()

    image_url = yield context.call_activity('classify_prep_image', input_data)
    result = yield context.call_activity('classify_predict', image_url)
    
    return [result]
    
main = df.Orchestrator.create(geocode_orchestrator_function)
